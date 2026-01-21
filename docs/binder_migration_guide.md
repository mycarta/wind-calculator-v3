# Updating Old Panel/Binder Deployments (2020-2021 → 2025+)

**Context:** This guide is for updating Panel apps that were built in 2020-2021 and work locally but no longer deploy on Binder. Panel deployment patterns have changed significantly.

---

## Quick Diagnosis Checklist

### 1. Check the `environment.yml`

**Old pattern (broken):**
```yaml
dependencies:
  - panel
  - bokeh
  - notebook
```

**New pattern (working):**
```yaml
channels:
  - conda-forge
  - pyviz        # Required for jupyter-panel-proxy
  
dependencies:
  - panel
  - bokeh
  - jupyter-panel-proxy   # ← THIS IS THE KEY ADDITION
  - notebook
```

**The `jupyter-panel-proxy` package is essential** — it enables Panel to work with mybinder.org's JupyterHub proxy.

---

### 2. Check the Notebook Structure

**Old pattern (broken on Binder):**
```python
# Just uses pn.serve() at the end
app = pn.Column(...)
pn.serve(app)  # Works locally, fails on Binder
```

**New pattern (works both locally and on Binder):**
```python
# Define the app
app = pn.Column(...)

# Make servable for Binder (jupyter-panel-proxy uses this)
app.servable()

# Optionally keep pn.serve() in a separate cell for local development
# pn.serve(app)  # Run this cell only for local testing
```

**Key insight:** `app.servable()` registers the app with Panel's server. The `jupyter-panel-proxy` then serves it through Binder's proxy.

---

### 3. Check the Binder URL Pattern

**Old patterns (may be broken):**
```
?urlpath=lab/tree/notebook.ipynb
?filepath=notebook.ipynb
```

**Current pattern:**
```
https://mybinder.org/v2/gh/OWNER/REPO/BRANCH?urlpath=/panel/NOTEBOOK_NAME
```

Example:
```
https://mybinder.org/v2/gh/mycarta/wind-calculator-v3/main?urlpath=/panel/Panel_app_pkg
```

**Note:** `NOTEBOOK_NAME` is the notebook filename **without** the `.ipynb` extension.

---

### 4. Check for Deprecated Configuration Files

**Files that may need removal or update:**

| File | Old Usage | Current Status |
|------|-----------|----------------|
| `postBuild` | Enable server extensions | Usually NOT needed with jupyter-panel-proxy |
| `jupyter_panel_config.py` | Server config | Usually NOT needed |
| `start` | Custom startup | Usually NOT needed |
| `apt.txt` | System packages | Still valid if needed |

**With `jupyter-panel-proxy` in environment.yml, you typically don't need `postBuild` scripts.**

---

### 5. Check Panel Version Compatibility

**Potential issues:**
- Panel API changes between versions
- `styles` vs `style` parameter (Panel 1.0+ uses `styles`)
- Widget parameter names may have changed

**Recommendation:** Check the Panel changelog for breaking changes between your old version and current version.

---

## Migration Steps

### Step 1: Update `environment.yml`
```yaml
channels:
  - conda-forge
  - pyviz
  
dependencies:
  - python=3.12          # Or your preferred version
  - panel>=1.0           # Modern Panel
  - bokeh
  - jupyter-panel-proxy  # Essential for Binder
  - notebook
  - ipykernel
  # ... your other dependencies
```

### Step 2: Update Notebook
Add `.servable()` call at the end of your app definition:
```python
# Your existing app code
app = pn.Column(
    pn.pane.Markdown("# My App"),
    # ... widgets and content
)

# Add this line for Binder compatibility
app.servable()
```

### Step 3: Update README Badge
```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/OWNER/REPO/BRANCH?urlpath=/panel/NOTEBOOK_NAME)
```

### Step 4: Remove Obsolete Files
Delete if present (usually not needed now):
- `postBuild` (unless you have other setup needs)
- `jupyter_panel_config.py`
- `start`

### Step 5: Test
1. Push to GitHub
2. Click Binder badge
3. Wait for build (first build takes 2-5 minutes)
4. Verify app loads and widgets work

---

## Troubleshooting

### "404 Not Found" on Binder
- Check the `urlpath` matches your notebook name exactly (case-sensitive, no `.ipynb`)
- Ensure `jupyter-panel-proxy` is in environment.yml

### App loads but widgets don't work
- Check for Panel API changes (especially `styles` vs `style`)
- Verify all dependencies are in environment.yml

### Build fails
- Check environment.yml syntax (YAML is whitespace-sensitive)
- Ensure channels include `pyviz` or `conda-forge`
- Check for package version conflicts

### Blank page
- Ensure `app.servable()` is called
- Check browser console for JavaScript errors

---

## Key Resources

- **Current Panel Binder docs:** https://panel.holoviz.org/how_to/deployment/binder.html
- **Example repo (working):** https://github.com/pyviz-demos/clifford
- **mybinder.org docs:** https://mybinder.readthedocs.io/

---

## Summary: The Minimal Fix

For most 2020-2021 Panel apps, the fix is:

1. **Add to environment.yml:** `jupyter-panel-proxy` (with `pyviz` channel)
2. **Add to notebook:** `app.servable()` after app definition
3. **Use URL:** `?urlpath=/panel/NotebookName`

That's often all you need!

---

*Created: January 2026*
*Based on successful migration of wind-calculator project*
