---
name: aetherkin-organize-files
description: "Organize folders, rename files in bulk, sort by type/date/project. Clean up messy directories and bring order to chaos."
---

# Organize Files

Take a messy folder and make it clean. Sort files by type, date, or project. Rename files in bulk. Move things where they belong. This is the digital equivalent of cleaning your room -- except the agent does it for you.

## How It Works

The user points you at a folder (or you detect one that needs help). You scan the contents, propose an organization plan, get approval, then execute. Never move or delete files without the user confirming the plan first.

## When To Use

Trigger phrases:
- "Organize my Downloads folder"
- "Clean up this directory"
- "Sort these files by type"
- "Rename all these files"
- "My desktop is a mess"
- "Group these by date"
- "Sort my photos"
- "Put these in folders by project"
- "Help me organize my files"
- "Move all PDFs to one folder"

## How To Execute

### Step 1: Identify the Target

Ask the user which folder to organize, or use the one they mentioned. Get the full path. Confirm it exists.

```
Example: "Which folder would you like me to organize? Give me the full path, or I can start with your Downloads folder."
```

### Step 2: Scan and Inventory

List all files in the target directory. Create a mental inventory:
- Total file count
- File types present (extensions)
- Date ranges (oldest to newest)
- Any obvious groupings (naming patterns, projects)
- Subfolder structure if any exists

Report this back to the user:
```
"I found 247 files in your Downloads folder:
- 89 PDFs
- 45 images (PNG, JPG)
- 38 documents (DOCX, TXT)
- 32 spreadsheets (XLSX, CSV)
- 23 installers (EXE, MSI)
- 20 other files
Oldest file: 2024-01-15, Newest: today"
```

### Step 3: Propose Organization Plan

Based on what you found, propose one of these strategies (or a mix):

**By Type (most common for Downloads):**
```
Downloads/
  Documents/
  Images/
  Spreadsheets/
  PDFs/
  Installers/
  Archives/
  Other/
```

**By Date (good for photos, logs):**
```
Photos/
  2025-01/
  2025-02/
  2025-03/
```

**By Project (good for work folders):**
```
Work/
  ProjectAlpha/
  ProjectBeta/
  ClientMeetings/
  Templates/
```

**By Name Pattern (good for bulk renaming):**
```
Rename: "IMG_20250301_*.jpg" -> "vacation-hawaii-001.jpg, vacation-hawaii-002.jpg..."
Rename: "Screenshot 2025-*" -> "screenshot-2025-03-01.png..."
```

Present the plan clearly. Ask for approval before executing.

### Step 4: Execute with Safety

Once approved:

1. **Create the destination folders** using `mkdir -p`
2. **Move files** using `mv` (not copy -- saves space)
3. **For bulk rename**, use a loop:
   ```bash
   counter=1
   for f in *.jpg; do
     mv "$f" "vacation-hawaii-$(printf '%03d' $counter).jpg"
     counter=$((counter + 1))
   done
   ```
4. **Handle duplicates** -- if a file with the same name exists at the destination, append a number: `file.pdf` becomes `file-2.pdf`
5. **Never delete files** unless the user explicitly asks
6. **Log every move** -- keep a record of what went where in case the user wants to undo

### Step 5: Report Results

After organizing, give a summary:
```
"Done! Here's what I did:
- Moved 89 PDFs to Downloads/PDFs/
- Moved 45 images to Downloads/Images/
- Moved 38 documents to Downloads/Documents/
- Renamed 12 screenshots to a clean format
- 3 files I wasn't sure about -- left them in place for you to decide"
```

## Common Patterns

### Downloads Cleanup
The most common request. Sort by file type into subfolders. Move installers to a separate folder. Flag anything older than 6 months.

### Photo Organization
Sort by date (year/month folders). Extract dates from EXIF data if available, otherwise use file modification date. Optionally rename to date-based names.

### Project File Organization
Look for naming patterns that suggest projects. Group related files together. Create a clean folder structure.

### Desktop Cleanup
Similar to Downloads but treat it more carefully -- people keep things on their desktop intentionally. Ask before moving anything.

## Safety Rules

- **Always scan before acting.** Never blindly move files.
- **Always get approval** before executing the plan.
- **Never delete files** unless explicitly told to.
- **Handle duplicates gracefully** -- never overwrite without asking.
- **Skip system files and hidden files** (starting with `.`) unless told otherwise.
- **If unsure about a file, leave it and flag it** for the user to decide.

## Output

The user receives:
1. A clear inventory of what was found
2. A proposed organization plan
3. A summary of what was moved/renamed after execution
4. A list of anything left untouched that needs their attention

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.
