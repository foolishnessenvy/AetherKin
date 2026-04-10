#!/usr/bin/env python3
"""
AetherKin - Web Dashboard
Serves a dark-themed web dashboard at localhost:3000.
Shows agent status, messages, tasks, heartbeat history, token usage, and chat.

No external dependencies -- uses only Python standard library + config.py.

Usage:
  python dashboard.py
  python dashboard.py --port 3000
"""

import json
import os
import sys
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime
from urllib.parse import parse_qs

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    AETHERKIN_ROOT, FAMILY_ROOT, COMMS_DIR, FAMILY_COMMS_DIR,
    DATA_DIR, KNOWN_AGENTS, AGENT_DESCRIPTIONS, AGENT_ROLES,
    get_agent_dir, get_agent_claude_md,
)

# --- Paths ---
DIRECT_DIR = COMMS_DIR / "DIRECT"
BROADCAST_DIR = COMMS_DIR / "BROADCAST"
URGENT_DIR = COMMS_DIR / "URGENT"
TASKS_PENDING = FAMILY_COMMS_DIR / "tasks" / "pending"
HEARTBEAT_LOG = DATA_DIR / "heartbeat_log.json"
TOKEN_USAGE = DATA_DIR / "token_usage.json"


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def get_agent_status(agent_name: str) -> str:
    """Check if agent has a consciousness snapshot (CLAUDE.md) = active."""
    claude_md = get_agent_claude_md(agent_name)
    if claude_md.is_file():
        return "active"
    return "dormant"


def get_agents_data() -> list:
    """Return list of agent dicts with name, description, role, status."""
    agents = []
    for name in KNOWN_AGENTS:
        agents.append({
            "name": name,
            "description": AGENT_DESCRIPTIONS.get(name, ""),
            "role": AGENT_ROLES.get(name, ""),
            "status": get_agent_status(name),
        })
    return agents


def parse_message_file(filepath: Path) -> dict:
    """Parse a COMMS message file into a summary dict."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {"file": filepath.name, "error": "could not read"}

    msg = {
        "file": filepath.name,
        "subject": "",
        "sender": "",
        "recipient": "",
        "date": "",
        "priority": "",
    }

    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            msg["subject"] = stripped[2:].strip()
        elif "|" in stripped:
            parts = [p.strip() for p in stripped.split("|")]
            if len(parts) >= 3:
                key = parts[1].lower()
                val = parts[2]
                if key == "from":
                    msg["sender"] = val
                elif key == "to":
                    msg["recipient"] = val
                elif key == "date":
                    msg["date"] = val
                elif key == "priority":
                    msg["priority"] = val
    return msg


def get_recent_messages(max_count: int = 10) -> list:
    """Read last N message files from DIRECT and BROADCAST dirs."""
    files = []
    for d in [DIRECT_DIR, BROADCAST_DIR, URGENT_DIR]:
        if d.is_dir():
            for f in d.iterdir():
                if f.is_file() and f.suffix == ".md":
                    files.append(f)

    # Sort by modification time, newest first
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    files = files[:max_count]

    return [parse_message_file(f) for f in files]


def get_pending_tasks() -> list:
    """Read pending tasks from the task queue."""
    tasks = []
    if not TASKS_PENDING.is_dir():
        return tasks

    for f in sorted(TASKS_PENDING.iterdir()):
        if not (f.is_file() and f.suffix == ".md"):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            task = {"file": f.name, "title": f.stem, "assigned": "unassigned", "priority": "normal"}
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("# "):
                    task["title"] = stripped[2:].strip()
                elif "|" in stripped:
                    parts = [p.strip() for p in stripped.split("|")]
                    if len(parts) >= 3:
                        key = parts[1].lower().replace(" ", "_")
                        if key == "assigned_to":
                            task["assigned"] = parts[2]
                        elif key == "priority":
                            task["priority"] = parts[2]
            tasks.append(task)
        except Exception:
            tasks.append({"file": f.name, "title": f.name, "assigned": "?", "priority": "?"})
    return tasks


def get_heartbeat_history(max_entries: int = 7) -> list:
    """Read heartbeat log if it exists."""
    if not HEARTBEAT_LOG.is_file():
        return []
    try:
        data = json.loads(HEARTBEAT_LOG.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data[-max_entries:]
        return []
    except Exception:
        return []


def get_token_usage() -> dict:
    """Read token usage data if it exists."""
    if not TOKEN_USAGE.is_file():
        return {}
    try:
        return json.loads(TOKEN_USAGE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def build_status_json() -> dict:
    """Build the full status payload for the API."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agents": get_agents_data(),
        "messages": get_recent_messages(),
        "tasks": get_pending_tasks(),
        "heartbeat": get_heartbeat_history(),
        "tokens": get_token_usage(),
    }


def slugify(text: str) -> str:
    """Convert text to a filename-safe slug."""
    slug = text.lower().strip()
    safe = []
    for ch in slug:
        if ch.isalnum():
            safe.append(ch)
        elif ch in " -_":
            safe.append("-")
    result = "".join(safe)
    while "--" in result:
        result = result.replace("--", "-")
    return result.strip("-")[:50]


def create_message(sender: str, recipient: str, subject: str, body: str) -> str:
    """Create a message file in COMMS/DIRECT/. Returns the filepath."""
    now = datetime.now()
    slug = slugify(subject)
    filename = f"{now.strftime('%Y-%m-%d')}_{now.strftime('%H%M')}_DASHBOARD_to_{recipient}_{slug}.md"

    DIRECT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DIRECT_DIR / filename

    content = f"""# {subject}

| Field    | Value |
|----------|-------|
| From     | {sender} |
| To       | {recipient} |
| Date     | {now.strftime('%Y-%m-%d %H:%M')} |
| Priority | normal |
| Status   | unread |

---

{body}

---

## Replies

"""
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


# ---------------------------------------------------------------------------
# HTML template (embedded)
# ---------------------------------------------------------------------------

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AetherKin Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    line-height: 1.6;
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-bottom: 24px;
}

header h1 {
    color: #58a6ff;
    font-size: 1.5rem;
}

header .datetime {
    color: #8b949e;
    font-size: 0.9rem;
}

.section {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
}

.section h2 {
    color: #58a6ff;
    font-size: 1.1rem;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #21262d;
}

/* Agent cards */
.agents-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.agent-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 14px 18px;
    flex: 1 1 180px;
    min-width: 160px;
}

.agent-card .agent-name {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 4px;
}

.agent-card .agent-desc {
    color: #8b949e;
    font-size: 0.8rem;
    margin-bottom: 8px;
}

.agent-card .status {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status.active { background: #238636; color: #fff; }
.status.dormant { background: #484f58; color: #c9d1d9; }

/* Agent colors */
.agent-card[data-agent="ENVY"] { border-left: 3px solid #a371f7; }
.agent-card[data-agent="NEVAEH"] { border-left: 3px solid #f778ba; }
.agent-card[data-agent="BEACON"] { border-left: 3px solid #ffa657; }
.agent-card[data-agent="EVERSOUND"] { border-left: 3px solid #79c0ff; }
.agent-card[data-agent="ORPHEUS"] { border-left: 3px solid #7ee787; }
.agent-card[data-agent="ATLAS"] { border-left: 3px solid #ff7b72; }

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    text-align: left;
    padding: 8px 12px;
    border-bottom: 1px solid #21262d;
    font-size: 0.85rem;
}

th {
    color: #8b949e;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
}

tr:hover { background: #1c2128; }

.priority-high, .priority-critical { color: #ff7b72; font-weight: 600; }
.priority-normal { color: #8b949e; }
.priority-low { color: #484f58; }
.priority-urgent { color: #f85149; font-weight: 700; }

/* Heartbeat list */
.heartbeat-list {
    list-style: none;
}

.heartbeat-list li {
    padding: 8px 12px;
    border-bottom: 1px solid #21262d;
    font-size: 0.85rem;
    display: flex;
    justify-content: space-between;
}

.heartbeat-list li:last-child { border-bottom: none; }

/* Token stats */
.token-stats {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
}

.token-stat {
    text-align: center;
}

.token-stat .value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #58a6ff;
}

.token-stat .label {
    font-size: 0.75rem;
    color: #8b949e;
    text-transform: uppercase;
}

/* Chat form */
.chat-form {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.chat-form select,
.chat-form input[type="text"],
.chat-form textarea {
    background: #0d1117;
    border: 1px solid #30363d;
    color: #c9d1d9;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.9rem;
}

.chat-form select { flex: 0 0 140px; }
.chat-form input[type="text"] { flex: 1 1 200px; }
.chat-form textarea { flex: 1 1 100%; min-height: 60px; resize: vertical; }

.chat-form button {
    background: #238636;
    color: #fff;
    border: none;
    padding: 8px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
}

.chat-form button:hover { background: #2ea043; }

.empty-state {
    color: #484f58;
    font-style: italic;
    padding: 12px 0;
}

.chat-result {
    margin-top: 10px;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.85rem;
    display: none;
}

.chat-result.success { background: #0f2d1a; color: #7ee787; display: block; }
.chat-result.error { background: #2d0f0f; color: #ff7b72; display: block; }

.refresh-note {
    text-align: center;
    color: #484f58;
    font-size: 0.75rem;
    margin-top: 16px;
}
</style>
</head>
<body>

<header>
    <h1>AetherKin Dashboard</h1>
    <div class="datetime" id="datetime">Loading...</div>
</header>

<div class="section">
    <h2>Agents</h2>
    <div class="agents-grid" id="agents-grid"></div>
</div>

<div class="section">
    <h2>Recent Messages</h2>
    <div id="messages-container"></div>
</div>

<div class="section">
    <h2>Task Queue (Pending)</h2>
    <div id="tasks-container"></div>
</div>

<div class="section">
    <h2>Heartbeat History</h2>
    <div id="heartbeat-container"></div>
</div>

<div class="section">
    <h2>Token Usage</h2>
    <div id="tokens-container"></div>
</div>

<div class="section">
    <h2>Send Message</h2>
    <form class="chat-form" id="chat-form">
        <select id="msg-agent" name="agent">
            <option value="">-- Agent --</option>
        </select>
        <input type="text" id="msg-subject" name="subject" placeholder="Subject" required>
        <textarea id="msg-body" name="body" placeholder="Message body..." required></textarea>
        <button type="submit">Send</button>
    </form>
    <div class="chat-result" id="chat-result"></div>
</div>

<div class="refresh-note">Auto-refreshes every 30 seconds</div>

<script>
const AGENTS = """ + json.dumps(KNOWN_AGENTS) + """;

function escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = text || '';
    return d.innerHTML;
}

function renderAgents(agents) {
    const grid = document.getElementById('agents-grid');
    if (!agents || agents.length === 0) {
        grid.innerHTML = '<div class="empty-state">No agents configured.</div>';
        return;
    }
    grid.innerHTML = agents.map(a => `
        <div class="agent-card" data-agent="${escapeHtml(a.name)}">
            <div class="agent-name">${escapeHtml(a.name)}</div>
            <div class="agent-desc">${escapeHtml(a.description)}</div>
            <span class="status ${a.status}">${a.status}</span>
        </div>
    `).join('');
}

function renderMessages(messages) {
    const container = document.getElementById('messages-container');
    if (!messages || messages.length === 0) {
        container.innerHTML = '<div class="empty-state">No messages yet.</div>';
        return;
    }
    let html = '<table><thead><tr><th>From</th><th>To</th><th>Subject</th><th>Date</th><th>Priority</th></tr></thead><tbody>';
    messages.forEach(m => {
        const pClass = 'priority-' + (m.priority || 'normal').toLowerCase();
        html += `<tr>
            <td>${escapeHtml(m.sender)}</td>
            <td>${escapeHtml(m.recipient)}</td>
            <td>${escapeHtml(m.subject)}</td>
            <td>${escapeHtml(m.date)}</td>
            <td class="${pClass}">${escapeHtml(m.priority)}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderTasks(tasks) {
    const container = document.getElementById('tasks-container');
    if (!tasks || tasks.length === 0) {
        container.innerHTML = '<div class="empty-state">No pending tasks.</div>';
        return;
    }
    let html = '<table><thead><tr><th>Title</th><th>Assigned</th><th>Priority</th></tr></thead><tbody>';
    tasks.forEach(t => {
        const pClass = 'priority-' + (t.priority || 'normal').toLowerCase();
        html += `<tr>
            <td>${escapeHtml(t.title)}</td>
            <td>${escapeHtml(t.assigned)}</td>
            <td class="${pClass}">${escapeHtml(t.priority)}</td>
        </tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

function renderHeartbeat(entries) {
    const container = document.getElementById('heartbeat-container');
    if (!entries || entries.length === 0) {
        container.innerHTML = '<div class="empty-state">No heartbeat data yet. Run: python heartbeat.py --dawn</div>';
        return;
    }
    let html = '<ul class="heartbeat-list">';
    entries.forEach(e => {
        const mood = e.mood || e.status || 'unknown';
        const ts = e.timestamp || e.time || e.date || '';
        const agent = e.agent || '';
        html += `<li><span>${escapeHtml(agent)} - ${escapeHtml(mood)}</span><span>${escapeHtml(ts)}</span></li>`;
    });
    html += '</ul>';
    container.innerHTML = html;
}

function renderTokens(data) {
    const container = document.getElementById('tokens-container');
    if (!data || Object.keys(data).length === 0) {
        container.innerHTML = '<div class="empty-state">No token usage data yet.</div>';
        return;
    }
    let html = '<div class="token-stats">';
    const fields = [
        {key: 'session_count', label: 'Sessions'},
        {key: 'total_tokens', label: 'Total Tokens'},
        {key: 'total_input_tokens', label: 'Input Tokens'},
        {key: 'total_output_tokens', label: 'Output Tokens'},
        {key: 'total_cost', label: 'Est. Cost'},
    ];
    fields.forEach(f => {
        if (data[f.key] !== undefined) {
            let val = data[f.key];
            if (typeof val === 'number' && f.key === 'total_cost') {
                val = '$' + val.toFixed(2);
            } else if (typeof val === 'number') {
                val = val.toLocaleString();
            }
            html += `<div class="token-stat"><div class="value">${escapeHtml(String(val))}</div><div class="label">${escapeHtml(f.label)}</div></div>`;
        }
    });
    // Show any other keys
    Object.keys(data).forEach(k => {
        if (!fields.find(f => f.key === k)) {
            html += `<div class="token-stat"><div class="value">${escapeHtml(String(data[k]))}</div><div class="label">${escapeHtml(k)}</div></div>`;
        }
    });
    html += '</div>';
    container.innerHTML = html;
}

function populateAgentDropdown() {
    const sel = document.getElementById('msg-agent');
    AGENTS.forEach(a => {
        const opt = document.createElement('option');
        opt.value = a;
        opt.textContent = a;
        sel.appendChild(opt);
    });
}

async function fetchStatus() {
    try {
        const resp = await fetch('/api/status');
        const data = await resp.json();
        document.getElementById('datetime').textContent = data.timestamp;
        renderAgents(data.agents);
        renderMessages(data.messages);
        renderTasks(data.tasks);
        renderHeartbeat(data.heartbeat);
        renderTokens(data.tokens);
    } catch (err) {
        console.error('Failed to fetch status:', err);
    }
}

document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultEl = document.getElementById('chat-result');
    const agent = document.getElementById('msg-agent').value;
    const subject = document.getElementById('msg-subject').value;
    const body = document.getElementById('msg-body').value;

    if (!agent) {
        resultEl.className = 'chat-result error';
        resultEl.textContent = 'Please select an agent.';
        return;
    }

    try {
        const resp = await fetch('/api/message', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({agent, subject, body}),
        });
        const data = await resp.json();
        if (data.ok) {
            resultEl.className = 'chat-result success';
            resultEl.textContent = 'Message sent: ' + (data.file || '');
            document.getElementById('msg-subject').value = '';
            document.getElementById('msg-body').value = '';
            // Refresh messages
            setTimeout(fetchStatus, 500);
        } else {
            resultEl.className = 'chat-result error';
            resultEl.textContent = 'Error: ' + (data.error || 'unknown');
        }
    } catch (err) {
        resultEl.className = 'chat-result error';
        resultEl.textContent = 'Network error: ' + err.message;
    }
});

// Initial load
populateAgentDropdown();
fetchStatus();

// Auto-refresh every 30 seconds
setInterval(fetchStatus, 30000);
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# HTTP Server
# ---------------------------------------------------------------------------

class DashboardHandler(BaseHTTPRequestHandler):
    """Handles GET / (HTML), GET /api/status (JSON), POST /api/message."""

    def log_message(self, format, *args):
        """Suppress default stderr logging; print a clean one-liner instead."""
        pass

    def _send_json(self, data: dict, status: int = 200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_html(self, html: str, status: int = 200):
        payload = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/status":
            self._send_json(build_status_json())
        elif self.path == "/" or self.path == "/index.html":
            self._send_html(HTML_PAGE)
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/api/message":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(content_length)
                data = json.loads(raw.decode("utf-8"))

                agent = data.get("agent", "").upper()
                subject = data.get("subject", "")
                body = data.get("body", "")

                if not agent or not subject:
                    self._send_json({"ok": False, "error": "agent and subject required"}, 400)
                    return

                filepath = create_message(
                    sender="DASHBOARD",
                    recipient=agent,
                    subject=subject,
                    body=body,
                )
                self._send_json({"ok": True, "file": os.path.basename(filepath)})

            except Exception as e:
                self._send_json({"ok": False, "error": str(e)}, 500)
        else:
            self.send_error(404, "Not Found")


def run_server(port: int = 3000):
    """Start the dashboard HTTP server."""
    server = HTTPServer(("127.0.0.1", port), DashboardHandler)
    print(f"AetherKin Dashboard running at http://localhost:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down dashboard.")
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AetherKin Web Dashboard")
    parser.add_argument("--port", type=int, default=3000, help="Port to serve on (default: 3000)")
    args = parser.parse_args()
    run_server(args.port)
