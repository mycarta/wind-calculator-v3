# Panel/Binder Migration Project Instructions for Claude

## Critical Context

This is a **Panel app from 2020-2021** that works locally but **no longer deploys on Binder**. Panel deployment patterns have changed significantly since then.

## Your Task

Update this project so the app deploys successfully on mybinder.org while maintaining local functionality.

## Required Changes (in order)

### 1. Update `environment.yml`

Add the `pyviz` channel and `jupyter-panel-proxy` package:

```yaml
channels:
  - conda-forge
  - pyviz          # ← ADD THIS

dependencies:
  # ... existing dependencies ...
  - jupyter-panel-proxy   # ← ADD THIS (essential for Binder)
```

### 2. Update the Notebook

Find where the Panel app is defined (usually a `pn.Column`, `pn.Row`, `pn.Template`, etc.) and add `.servable()`:

```python
# After the app definition, add:
app.servable()  # or app_panel.servable(), whatever the variable is called
```

**Keep any existing `pn.serve(app)` calls** — they're still needed for local development. Just add `.servable()` as well.

### 3. Check for API Changes

Panel has evolved. Watch for:
- `style=` → `styles=` (Panel 1.0+)
- Widget parameter changes
- Deprecated methods

Fix any deprecation warnings or errors.

### 4. Update README with Binder Badge

```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/OWNER/REPO/BRANCH?urlpath=/panel/NOTEBOOK_NAME)
```

**Note:** `NOTEBOOK_NAME` is without the `.ipynb` extension.

### 5. Remove Obsolete Files (if present)

These are usually NOT needed with modern jupyter-panel-proxy:
- `postBuild`
- `jupyter_panel_config.py`
- `start`

Only keep them if they do something specific beyond Panel setup.

## Testing Checklist

1. **Local test:** Run notebook, verify app works
2. **Push to GitHub**
3. **Binder test:** Click badge, wait for build (2-5 min first time)
4. **Verify:** All widgets interactive, no JS errors

## When Uncertain

- Check current Panel docs: https://panel.holoviz.org/how_to/deployment/binder.html
- If the app structure is complex, ask the user for clarification
- Preserve existing functionality — don't refactor unless necessary

## Do NOT

- Change the app's logic or calculations (unless broken)
- Remove features that work
- Invent new functionality
- Change file names without asking
