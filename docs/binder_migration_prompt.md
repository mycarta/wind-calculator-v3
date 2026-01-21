# Prompt for Claude: Update Old Panel/Binder App

Copy and paste this into a new Claude chat:

---

## Prompt

I have a Panel app from 2020-2021 that works locally but no longer deploys on Binder. Panel deployment patterns have changed.

**Please start by reading:** `CLAUDE_INSTRUCTIONS.md` (or `CLAUDE_INSTRUCTIONS_BINDER_MIGRATION.md` if present)

**The key changes needed are:**
1. Add `jupyter-panel-proxy` to environment.yml (with `pyviz` channel)
2. Add `app.servable()` to the notebook after the app definition
3. Update the Binder URL to use `?urlpath=/panel/NotebookName`
4. Fix any deprecated Panel API calls (e.g., `style=` → `styles=`)

**Files to examine:**
- `environment.yml` — check channels and dependencies
- The main notebook (`.ipynb`) — find app definition, add .servable()
- `README.md` — update Binder badge URL

**Please:**
1. Read the instruction file first
2. Examine the notebook to understand the app structure
3. Make the minimal changes needed for Binder deployment
4. Test locally if possible, then push for Binder testing

Let me know if you have questions before starting.

---

## Alternative Short Version

"This Panel app worked on Binder in 2020 but doesn't now. Read CLAUDE_INSTRUCTIONS.md and update it for modern Panel/Binder deployment. Key fix: add `jupyter-panel-proxy` to environment.yml and `app.servable()` to the notebook."
