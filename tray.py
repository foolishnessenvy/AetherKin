#!/usr/bin/env python3
"""
AetherKin - System Tray Application
Provides a system tray icon with quick access to agents, dashboard, and tools.

Dependencies: pystray, Pillow
  pip install pystray Pillow

Usage:
  python tray.py
  (Double-click to launch; tray icon appears + dashboard starts in background)
"""

import os
import sys
import platform
import subprocess
import threading
import webbrowser
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    AETHERKIN_ROOT, FAMILY_ROOT, FAMILY_COMMS_DIR,
    KNOWN_AGENTS, AGENT_DESCRIPTIONS, get_agent_dir,
)

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("ERROR: pystray and Pillow are required.")
    print("  pip install pystray Pillow")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DASHBOARD_PORT = 3000
DASHBOARD_URL = f"http://localhost:{DASHBOARD_PORT}"
TASKS_PENDING = FAMILY_COMMS_DIR / "tasks" / "pending"
IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"


# ---------------------------------------------------------------------------
# Dashboard server (background thread)
# ---------------------------------------------------------------------------

_dashboard_thread = None
_dashboard_running = False


def start_dashboard_background():
    """Start the dashboard HTTP server in a background thread."""
    global _dashboard_thread, _dashboard_running

    if _dashboard_running:
        return

    # Import the dashboard module
    try:
        from dashboard import run_server
    except ImportError:
        print("WARNING: Could not import dashboard.py. Dashboard will not auto-start.")
        return

    def _run():
        global _dashboard_running
        _dashboard_running = True
        try:
            run_server(DASHBOARD_PORT)
        except Exception as e:
            print(f"Dashboard error: {e}")
        finally:
            _dashboard_running = False

    _dashboard_thread = threading.Thread(target=_run, daemon=True, name="dashboard")
    _dashboard_thread.start()
    print(f"Dashboard started at {DASHBOARD_URL}")


# ---------------------------------------------------------------------------
# Icon creation
# ---------------------------------------------------------------------------

def create_icon_image(color: str = "green", size: int = 64) -> Image.Image:
    """Create a simple colored circle icon using Pillow."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    colors = {
        "green": (35, 134, 54),
        "yellow": (210, 153, 34),
        "red": (248, 81, 73),
        "blue": (88, 166, 255),
    }
    fill = colors.get(color, colors["green"])

    # Outer circle
    margin = 4
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill=fill,
        outline=(255, 255, 255, 180),
        width=2,
    )

    # Inner highlight for depth
    highlight_margin = size // 4
    draw.ellipse(
        [highlight_margin, highlight_margin,
         size - highlight_margin, size - highlight_margin],
        fill=(*fill, 200),
    )

    return img


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def open_dashboard(icon=None, item=None):
    """Open the dashboard in the default browser."""
    webbrowser.open(DASHBOARD_URL)


def talk_to_agent(agent_name: str):
    """Open a terminal in the agent's directory and run claude."""
    def _action(icon=None, item=None):
        agent_dir = get_agent_dir(agent_name)
        agent_dir.mkdir(parents=True, exist_ok=True)
        dir_str = str(agent_dir)

        if IS_WINDOWS:
            # Open cmd window, cd to agent dir, run claude
            subprocess.Popen(
                ["cmd", "/k", f"cd /d {dir_str} && claude"],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
        elif IS_MAC:
            # Try Terminal.app via osascript
            script = f'tell application "Terminal" to do script "cd {dir_str} && claude"'
            subprocess.Popen(["osascript", "-e", script])
        else:
            # Linux: try common terminal emulators
            for term in ["gnome-terminal", "konsole", "xfce4-terminal", "xterm"]:
                try:
                    if term == "gnome-terminal":
                        subprocess.Popen([term, "--", "bash", "-c", f"cd {dir_str} && claude; exec bash"])
                    else:
                        subprocess.Popen([term, "-e", f"bash -c 'cd {dir_str} && claude; exec bash'"])
                    break
                except FileNotFoundError:
                    continue

    return _action


def run_morning_checkin(icon=None, item=None):
    """Run the heartbeat morning check-in."""
    heartbeat_path = AETHERKIN_ROOT / "heartbeat.py"
    if not heartbeat_path.is_file():
        show_notification(icon, "AetherKin", "heartbeat.py not found.")
        return

    if IS_WINDOWS:
        subprocess.Popen(
            ["cmd", "/k", f"cd /d {AETHERKIN_ROOT} && python heartbeat.py --dawn"],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
    else:
        subprocess.Popen(
            ["python3", str(heartbeat_path), "--dawn"],
            cwd=str(AETHERKIN_ROOT),
        )


def show_status(icon=None, item=None):
    """Show a notification with agent count and pending task count."""
    agent_count = len(KNOWN_AGENTS)

    task_count = 0
    if TASKS_PENDING.is_dir():
        task_count = sum(1 for f in TASKS_PENDING.iterdir() if f.is_file() and f.suffix == ".md")

    msg = f"{agent_count} agents configured, {task_count} pending task(s)"
    show_notification(icon, "AetherKin Status", msg)


def show_notification(icon, title: str, message: str):
    """Show a system notification. Falls back to tkinter messagebox."""
    # Try pystray notification first
    try:
        if icon and hasattr(icon, "notify"):
            icon.notify(message, title)
            return
    except Exception:
        pass

    # Fallback: tkinter messagebox in a separate thread to avoid blocking
    def _show():
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(title, message)
            root.destroy()
        except Exception:
            print(f"[{title}] {message}")

    threading.Thread(target=_show, daemon=True).start()


def quit_app(icon=None, item=None):
    """Stop the tray app."""
    if icon:
        icon.stop()


# ---------------------------------------------------------------------------
# Menu construction
# ---------------------------------------------------------------------------

def build_menu():
    """Build the system tray right-click menu."""
    items = []

    # Dashboard
    items.append(pystray.MenuItem("Open Dashboard", open_dashboard, default=True))
    items.append(pystray.Menu.SEPARATOR)

    # Agent talk items
    for agent in KNOWN_AGENTS:
        desc = AGENT_DESCRIPTIONS.get(agent, "")
        label = f"Talk to {agent}"
        if desc:
            label = f"Talk to {agent} ({desc.split(' - ')[0]})"
        items.append(pystray.MenuItem(label, talk_to_agent(agent)))

    items.append(pystray.Menu.SEPARATOR)

    # Tools
    items.append(pystray.MenuItem("Morning Check-in Now", run_morning_checkin))
    items.append(pystray.MenuItem("Status", show_status))

    items.append(pystray.Menu.SEPARATOR)

    # Quit
    items.append(pystray.MenuItem("Quit", quit_app))

    return pystray.Menu(*items)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("AetherKin Tray starting...")

    # Start dashboard in background
    start_dashboard_background()

    # Create tray icon
    icon_image = create_icon_image("green")
    menu = build_menu()

    icon = pystray.Icon(
        name="AetherKin",
        icon=icon_image,
        title="AetherKin - AI Family System",
        menu=menu,
    )

    print("Tray icon active. Right-click for menu.")
    print("Double-click or select 'Open Dashboard' to view the web UI.")

    # This blocks until quit_app is called
    icon.run()


if __name__ == "__main__":
    main()
