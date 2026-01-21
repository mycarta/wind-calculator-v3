# Prompt for Claude: Update Old Panel/Binder App

**Updated:** January 2026 — Use JupyterLab approach (most reliable)

Copy and paste this into a new Claude chat:

---

## Prompt

I have a Panel app from 2020-2021 that works locally but no longer deploys on Binder. Panel deployment patterns have changed.

**Please start by reading:** `CLAUDE_INSTRUCTIONS_BINDER_MIGRATION.md` (or `CLAUDE_INSTRUCTIONS.md` if that's not present)

**The key changes needed are:**
1. Add `jupyter-panel-proxy` to environment.yml (with `pyviz` channel)
2. Add `app.servable()` to the notebook after the app definition
3. Comment out any `pn.serve(app)` calls (keep for local dev reference)
4. Update the Binder URL to use `?urlpath=lab/tree/NotebookName.ipynb` (JupyterLab approach)
5. Add step-by-step "Run All Cells" instructions to README
6. Fix any deprecated Panel API calls (e.g., `style=` → `styles=`)

**Important:** The direct Panel serve URL (`?urlpath=/panel/NotebookName`) often times out. Use the JupyterLab approach instead — users run cells manually but it's reliable.

**Files to examine:**
- `environment.yml` — check channels and dependencies
- The main notebook (`.ipynb`) — find app definition, add .servable(), comment out pn.serve()
- `README.md` — update Binder badge URL and add user instructions

**Please:**
1. Read the instruction file first
2. Examine the notebook to understand the app structure
3. Make the minimal changes needed for Binder deployment
4. Keep pn.serve() commented out for local dev reference
5. Push for Binder testing with JupyterLab URL

Let me know if you have questions before starting.

---

## Alternative Short Version

"This Panel app worked on Binder in 2020 but doesn't now. Read CLAUDE_INSTRUCTIONS_BINDER_MIGRATION.md and update it for modern Panel/Binder deployment. Key fixes: add `jupyter-panel-proxy` to environment.yml, add `app.servable()` to the notebook, use JupyterLab URL (`?urlpath=lab/tree/Notebook.ipynb`) with 'Run All Cells' instructions in README."
