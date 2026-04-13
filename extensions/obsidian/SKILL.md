---
name: llm-wiki-obsidian
description: "Extension for llm-wiki: use an Obsidian vault as the wiki directory. The llm-wiki structure is Obsidian-native — wikilinks, graph view, and Dataview work out of the box."
version: 1.0.0
metadata:
  category: workflow
  agent_type: general-purpose
  requires: llm-wiki
---

# Obsidian Extension for llm-wiki

The llm-wiki directory structure is Obsidian-compatible by design — `[[wikilinks]]`,
YAML frontmatter, and folder layout all work without any conversion or plugins.
This extension covers the setup and optional headless sync for server environments.

## When to Use

- You want to browse and edit the wiki in Obsidian while the agent writes to it
- You want Graph View to visualize the knowledge network
- You want to use Dataview queries to filter pages by tag or date
- You're running the agent on a server and want changes to appear on your laptop

## Basic Setup (Desktop)

```powershell
# Point LLM_WIKI_PATH at an existing Obsidian vault
$env:LLM_WIKI_PATH = "C:\Users\you\Documents\MyVault"

# Or create the wiki inside an existing vault subfolder
$env:LLM_WIKI_PATH = "C:\Users\you\Documents\MyVault\wiki"
```

That's all. The wiki skill's file structure is already Obsidian-native:
- `[[wikilinks]]` render as clickable links in Obsidian
- YAML frontmatter powers Dataview queries
- Graph View shows the knowledge network
- `raw/assets/` holds images referenced with `![[image.png]]`

**Recommended Obsidian settings:**
- Templates folder: point to `templates/` in the wiki directory
- New attachments: `raw/assets/`
- Wikilinks: enabled (default)

## Useful Dataview Queries

With the [Dataview plugin](https://github.com/blacksmithgu/obsidian-dataview) installed:

```dataview
-- All entity pages, sorted by last updated
TABLE updated, tags FROM "entities"
SORT updated DESC

-- Concept pages tagged with "alignment"
LIST FROM "concepts"
WHERE contains(tags, "alignment")

-- Pages with contradictions flagged
TABLE contradictions FROM "entities" OR "concepts"
WHERE contradictions

-- Recently ingested sources
TABLE created FROM "raw/articles"
SORT created DESC
LIMIT 10
```

## Headless Sync (Server / CI Environments)

If the agent runs on a server without a display, use `obsidian-headless` to sync
the wiki to your Obsidian Sync account so it appears on your desktop automatically.

**Prerequisites:**
- Obsidian account with an active Sync subscription
- Node.js 22+

```bash
# Install
npm install -g obsidian-headless

# Authenticate
ob login --email your@email.com --password 'your-password'

# Create a remote vault for the wiki
ob sync-create-remote --name "My LLM Wiki"

# Connect the local wiki directory
cd "$LLM_WIKI_PATH"
ob sync-setup --vault "<vault-id-from-previous-command>"

# One-time sync
ob sync

# Continuous sync (foreground — use systemd/launchd for background)
ob sync --continuous
```

**Background sync with systemd (Linux):**

```ini
# ~/.config/systemd/user/llm-wiki-sync.service
[Unit]
Description=LLM Wiki Obsidian Sync
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ob sync --continuous
WorkingDirectory=%h/wiki
Environment=LLM_WIKI_PATH=%h/wiki
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now llm-wiki-sync
sudo loginctl enable-linger $USER   # survive logout
```

## Without Obsidian Sync

For simple setups, commit the wiki to a private git repository:

```powershell
# In the wiki directory
git init
git add .
git commit -m "Initial wiki"

# Pull on other machines to get updates
git pull
```

This gives you version history for free.

## Tips

- Don't install Dataview as a required dependency — the wiki works fine without it
- The agent writes files using standard file tools, not Obsidian's API — no special setup needed
- If you use Obsidian's built-in Templates plugin, the templates/ folder works for both
- Graph View is most useful after 20+ pages are linked — don't judge it on a small wiki
