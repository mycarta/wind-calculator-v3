# Wind Calculator: VSCode Project Setup Checklist

**Date:** January 21, 2026  
**Purpose:** Step-by-step guide to set up the project and hand off to Claude in VSCode  
**Estimated time:** 20-30 minutes

---

## Before You Start

**You need:**
- [ ] Conda or Miniconda installed
- [ ] VSCode installed
- [ ] Git installed
- [ ] Access to the files from this Claude.ai session
- [ ] Your existing `Panel_app_pkg.ipynb` from the original project

**Platform notes:**
- Commands shown are for Mac/Linux terminal
- Windows users: Use Anaconda Prompt (not regular CMD) and adjust paths (use `\` instead of `/`)

---

## Phase 1: Gather Files

### 1.1 Create a staging folder

**Mac/Linux:**
```bash
mkdir -p ~/Desktop/wind-handoff
```

**Windows (in Anaconda Prompt):**
```cmd
mkdir %USERPROFILE%\Desktop\wind-handoff
```

### 1.2 Download from Claude.ai Session

In Claude.ai, download these files to your staging folder:

| File | Status | Required? |
|------|--------|-----------|
| `wind_calculations.py` | Finalized | ✅ Yes |
| `environment.yml` | Finalized | ✅ Yes |
| `wind_calculator_handoff_updated.md` | Main briefing | ✅ Yes |
| `project_executive_summary.md` | Quick reference | Recommended |
| `session_summary_2026-01-21.md` | Session record | Optional |

**How to download:** Click on the file attachment in Claude's response → Download

- [ ] Downloaded `wind_calculations.py`
- [ ] Downloaded `environment.yml`
- [ ] Downloaded `wind_calculator_handoff_updated.md`
- [ ] Downloaded `project_executive_summary.md`

### 1.3 Locate from your existing project

Find these in your existing project folder (wherever you had the original wind calculator):

| File | Purpose | Required? |
|------|---------|-----------|
| `Panel_app_pkg.ipynb` | Reference Panel app design | ✅ Yes |
| `wind_power_intuition.md` | Physics explanation | Recommended |
| `Ginsberg.pdf` | Source pages 56-62 | Optional |

- [ ] Located `Panel_app_pkg.ipynb`
- [ ] Located `wind_power_intuition.md` (if available)

### 1.4 Verify all essential files are in staging folder

```bash
ls ~/Desktop/wind-handoff/
```

**Must see at minimum:**
```
wind_calculations.py
environment.yml
wind_calculator_handoff_updated.md
Panel_app_pkg.ipynb
```

- [ ] All 4 essential files present

---

## Phase 2: Create Project Directory

### 2.1 Decide where to put the project

Choose a location for your project. Common options:
- `~/Projects/wind-calculator` (Mac/Linux)
- `%USERPROFILE%\Projects\wind-calculator` (Windows)
- Or wherever you keep your Python projects

### 2.2 Create the project folder

**Mac/Linux:**
```bash
mkdir -p ~/Projects/wind-calculator
cd ~/Projects/wind-calculator
pwd  # Verify you're in the right place
```

**Windows (Anaconda Prompt):**
```cmd
mkdir %USERPROFILE%\Projects\wind-calculator
cd %USERPROFILE%\Projects\wind-calculator
cd  # Verify you're in the right place
```

- [ ] Project folder created
- [ ] Currently in project folder

### 2.3 Initialize git repository

```bash
git init
```

**Expected output:**
```
Initialized empty Git repository in /Users/yourname/Projects/wind-calculator/.git/
```

- [ ] Git initialized

### 2.4 Copy essential files from staging folder

**Mac/Linux:**
```bash
# Core files (to project root)
cp ~/Desktop/wind-handoff/wind_calculations.py .
cp ~/Desktop/wind-handoff/environment.yml .
cp ~/Desktop/wind-handoff/Panel_app_pkg.ipynb .
```

**Windows:**
```cmd
copy %USERPROFILE%\Desktop\wind-handoff\wind_calculations.py .
copy %USERPROFILE%\Desktop\wind-handoff\environment.yml .
copy %USERPROFILE%\Desktop\wind-handoff\Panel_app_pkg.ipynb .
```

- [ ] `wind_calculations.py` copied
- [ ] `environment.yml` copied
- [ ] `Panel_app_pkg.ipynb` copied

### 2.5 Create docs folder and copy documentation

**Mac/Linux:**
```bash
mkdir docs
cp ~/Desktop/wind-handoff/wind_calculator_handoff_updated.md docs/
cp ~/Desktop/wind-handoff/project_executive_summary.md docs/  # if you have it
cp ~/Desktop/wind-handoff/wind_power_intuition.md docs/       # if you have it
```

**Windows:**
```cmd
mkdir docs
copy %USERPROFILE%\Desktop\wind-handoff\wind_calculator_handoff_updated.md docs\
copy %USERPROFILE%\Desktop\wind-handoff\project_executive_summary.md docs\
```

- [ ] `docs/` folder created
- [ ] Handoff document in `docs/`

### 2.6 Create tests folder

```bash
mkdir tests
touch tests/__init__.py    # Mac/Linux
# Windows: type nul > tests\__init__.py
```

- [ ] `tests/` folder created
- [ ] `tests/__init__.py` created

### 2.7 Verify project structure

**Mac/Linux:**
```bash
find . -type f -not -path './.git/*' | head -20
```

**Or simpler:**
```bash
ls -la
ls docs/
ls tests/
```

**Expected structure:**
```
wind-calculator/
├── environment.yml           # Conda environment spec
├── wind_calculations.py      # Core calculation module
├── Panel_app_pkg.ipynb       # Reference Panel app
├── docs/
│   ├── wind_calculator_handoff_updated.md  # Main briefing
│   └── project_executive_summary.md        # Quick reference (optional)
└── tests/
    └── __init__.py
```

- [ ] Structure matches expected layout

---

## Phase 3: Set Up Conda Environment

### 3.1 Verify conda is available

```bash
conda --version
```

**Expected:** `conda 23.x.x` or `conda 24.x.x`

**If you get "command not found":**

*Mac/Linux:*
```bash
# Try sourcing conda
source ~/anaconda3/etc/profile.d/conda.sh
# or for Miniconda:
source ~/miniconda3/etc/profile.d/conda.sh
```

*Windows:*
- Make sure you're using **Anaconda Prompt**, not regular Command Prompt
- Search for "Anaconda Prompt" in Start menu

- [ ] `conda --version` works

### 3.2 Create the environment

```bash
# Make sure you're in the project folder
cd ~/Projects/wind-calculator   # adjust path as needed

# Create environment from yml file
conda env create -f environment.yml
```

**This will take 2-5 minutes.** You'll see packages being downloaded and installed.

**Expected final output:**
```
Preparing transaction: done
Verifying transaction: done
Executing transaction: done
#
# To activate this environment, use
#
#     $ conda activate wind-panel-app
```

**If you get errors:**

| Error | Solution |
|-------|----------|
| "environment already exists" | Run: `conda env remove -n wind-panel-app` then try again |
| "channel not found" | Add channel: `conda config --add channels conda-forge` |
| "ResolvePackageNotFound" | Check `environment.yml` was copied correctly |

- [ ] Environment created successfully

### 3.3 Activate the environment

```bash
conda activate wind-panel-app
```

**Your terminal prompt should change** to show the environment name:

```
Before: user@machine:~/Projects/wind-calculator$
After:  (wind-panel-app) user@machine:~/Projects/wind-calculator$
```

**If activation fails:**
```bash
# Initialize conda for your shell (do this once)
conda init bash   # or: conda init zsh (Mac), conda init powershell (Windows)
# Then restart your terminal and try again
```

- [ ] Environment activated (shows `(wind-panel-app)` in prompt)

### 3.4 Verify Python version

```bash
python --version
```

**Expected:** `Python 3.12.x`

- [ ] Python 3.12.x confirmed

### 3.5 Verify key packages

Run each command and check the output:

```bash
python -c "import panel; print(f'Panel: {panel.__version__}')"
```
**Expected:** `Panel: 1.4.4`

```bash
python -c "import bokeh; print(f'Bokeh: {bokeh.__version__}')"
```
**Expected:** `Bokeh: 3.4.1`

```bash
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
```
**Expected:** `NumPy: 1.26.x`

```bash
python -c "import jupyter_bokeh; print('jupyter_bokeh OK')"
```
**Expected:** `jupyter_bokeh OK`

- [ ] Panel 1.4.4
- [ ] Bokeh 3.4.1
- [ ] NumPy 1.26.x
- [ ] jupyter_bokeh OK

### 3.6 Verify wind_calculations imports correctly

```bash
python -c "import wind_calculations as wc; print('Import OK')"
```

**Expected:** `Import OK`

**If you get "ModuleNotFoundError":**
- Check you're in the project folder: `pwd` (should show `.../wind-calculator`)
- Check file exists: `ls wind_calculations.py`

- [ ] Import successful

### 3.7 Run Ginsberg validation test

This is the critical test — if this passes, your setup is correct.

```bash
python << 'EOF'
import wind_calculations as wc

# Ginsberg worked example inputs (from his book, pp. 60-62)
D = 50       # m (rotor diameter)
v = 4.47     # m/s (mean wind speed)
rho = 1.225  # kg/m³ (sea level air density)
eta = 0.20   # 20% overall efficiency

# Calculate each step
pd = wc.annual_power_density(v, rho)
power = wc.power_kw(pd, D)
aep_nd = wc.annual_energy_output(power)
aep_d = wc.derated_annual_energy_output(power, eta)

# Display results
print("=" * 50)
print("GINSBERG VALIDATION TEST")
print("=" * 50)
print(f"Power density:      {pd:>8} W/m²    (expected: 104)")
print(f"Mean power:         {power:>8} kW      (expected: 204)")
print(f"AEP (non-derated):  {aep_nd:>8} MWh/yr  (expected: 1787)")
print(f"AEP (20% eff):      {aep_d:>8} MWh/yr  (expected: 357)")
print("=" * 50)

# Automated assertions
try:
    assert pd == 104, f"Power density mismatch: got {pd}, expected 104"
    assert power == 204, f"Power mismatch: got {power}, expected 204"
    assert aep_nd == 1787, f"AEP non-derated mismatch: got {aep_nd}, expected 1787"
    assert aep_d == 357, f"AEP derated mismatch: got {aep_d}, expected 357"
    print("✅ ALL VALIDATIONS PASSED!")
    print("Your wind_calculations.py is correctly installed.")
except AssertionError as e:
    print(f"❌ VALIDATION FAILED: {e}")
    print("Check that you copied the correct wind_calculations.py file.")
EOF
```

**Expected output:**
```
==================================================
GINSBERG VALIDATION TEST
==================================================
Power density:       104.0 W/m²    (expected: 104)
Mean power:          204.0 kW      (expected: 204)
AEP (non-derated):  1787.0 MWh/yr  (expected: 1787)
AEP (20% eff):       357.0 MWh/yr  (expected: 357)
==================================================
✅ ALL VALIDATIONS PASSED!
Your wind_calculations.py is correctly installed.
```

**If validation fails:**
- Re-download `wind_calculations.py` from Claude.ai session
- Check it has `EPF_RAYLEIGH = 1.91` near the top
- Check it has `HOURS_PER_YEAR = 8760`

- [ ] All four values match expected
- [ ] "ALL VALIDATIONS PASSED!" message shown

---

## Phase 4: Initial Git Commit

### 4.1 Create .gitignore file

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Environment
.env
.venv/
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.pytest_cache/
EOF
```

- [ ] `.gitignore` created

### 4.2 Check what will be committed

```bash
git status
```

**Should show these as "Untracked files":**
```
.gitignore
Panel_app_pkg.ipynb
environment.yml
wind_calculations.py
docs/
tests/
```

### 4.3 Stage all files

```bash
git add .
git status
```

**Should now show files as "Changes to be committed"**

- [ ] Files staged

### 4.4 Make initial commit

```bash
git commit -m "Initial commit: wind calculator project setup

- wind_calculations.py: Core calculation module (validated against Ginsberg)
- environment.yml: Conda environment specification (wind-panel-app)
- Panel_app_pkg.ipynb: Reference Panel app design
- docs/: Handoff documentation for project continuation
- tests/: Test directory structure

Methodology: Ginsberg (2019) Swept Area Method
Data source: von Krauland et al. (2023) as proxy for Scotian Shelf"
```

**Expected output:**
```
[main (root-commit) xxxxxxx] Initial commit: wind calculator project setup
 X files changed, XXX insertions(+)
 create mode 100644 .gitignore
 create mode 100644 Panel_app_pkg.ipynb
 ...
```

- [ ] Initial commit made

### 4.5 (Optional) Connect to GitHub

If you want to push to your existing GitHub repo:

```bash
git remote add origin https://github.com/mycarta/wind-calculator.git
git branch -M main
git push -u origin main
```

Or if you have GitHub CLI:
```bash
gh repo create wind-calculator --private --source=. --push
```

- [ ] (Optional) Pushed to GitHub

---

## Phase 5: Set Up VSCode

### 5.1 Open project in VSCode

**From terminal (recommended):**
```bash
code .
```

**Or manually:**
1. Open VSCode
2. File → Open Folder
3. Navigate to `~/Projects/wind-calculator` (or your project path)
4. Click "Open"

- [ ] Project opened in VSCode

### 5.2 Select Python interpreter

**Important:** VSCode needs to know which Python environment to use.

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type: `Python: Select Interpreter`
3. Press Enter
4. Look for `wind-panel-app` in the list
   - It should show something like: `Python 3.12.x ('wind-panel-app': conda)`
5. Click to select it

**If you don't see `wind-panel-app`:**
- Click "Enter interpreter path..."
- Browse to: `~/anaconda3/envs/wind-panel-app/bin/python` (Mac/Linux)
- Or: `C:\Users\YourName\anaconda3\envs\wind-panel-app\python.exe` (Windows)

**Verify:** Look at the bottom status bar in VSCode. It should show `wind-panel-app`.

- [ ] Correct interpreter selected

### 5.3 Verify VSCode terminal uses correct environment

1. Open terminal in VSCode: `` Ctrl+` `` (backtick) or View → Terminal
2. The prompt should show `(wind-panel-app)`
3. If not, type: `conda activate wind-panel-app`

**Quick verification:**
```bash
which python    # Mac/Linux
where python    # Windows
```
Should show path containing `wind-panel-app`.

```bash
python -c "import wind_calculations as wc; print('OK')"
```
Should print `OK`.

- [ ] VSCode terminal uses correct environment

### 5.4 Install recommended VSCode extensions

If not already installed, install these extensions:

1. **Python** (by Microsoft) — Essential for Python development
2. **Jupyter** (by Microsoft) — For working with notebooks
3. **GitHub Copilot** — If you have access and plan to use Copilot for Claude

To install: Click Extensions icon (or `Cmd+Shift+X`) → Search → Install

- [ ] Python extension installed
- [ ] Jupyter extension installed
- [ ] (Optional) GitHub Copilot installed

### 5.5 (Optional) Configure workspace settings

Create `.vscode/settings.json` for project-specific settings:

```bash
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "${workspaceFolder}/../anaconda3/envs/wind-panel-app/bin/python",
    "jupyter.notebookFileRoot": "${workspaceFolder}",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/.ipynb_checkpoints": true
    }
}
EOF
```

**Note:** Adjust the `python.defaultInterpreterPath` to match your conda installation location.

- [ ] (Optional) Workspace settings configured

---

## Phase 6: Prepare Custom Instructions for Claude

### 6.1 Create CLAUDE_INSTRUCTIONS.md file

This file serves as a reference for Claude (and you) about project constraints:

```bash
cat > CLAUDE_INSTRUCTIONS.md << 'EOF'
# Wind Calculator Project Instructions for Claude

## Critical Constraints

### Data Integrity
- **Do not invent data.** All wind speeds, air densities, and parameters come from either:
  - Ginsberg (2019) — EPF, efficiency values, methodology
  - von Krauland et al. (2023) — wind speeds, air density, spacing factor
- If you need a value that isn't in the lookup tables, **ask first**.
- Do not invent claims about wind energy, the Scotian Shelf, or offshore wind methodology.

### Methodology
- **Follow Ginsberg (2019) exactly** for the Swept Area Method
- Implementation must match his worked example:
  - D = 50m, v = 4.47 m/s, ρ = 1.225 kg/m³
  - → 104 W/m², 204 kW, 357 MWh/year at 20% efficiency
- The validation test must always pass

### Technical Guidelines
- **Environment name:** `wind-panel-app` (not `wind-calculator`)
- **`spacing_factor` has no default:** This is intentional — user must choose via UI slider
- **EPF = 1.91** is fixed (Rayleigh distribution) — don't make user-configurable
- **Binder deployment:** Consult CURRENT docs at https://panel.holoviz.org/how_to/deployment/binder.html (2020-2021 patterns are outdated)

## When Uncertain
- Ask before proceeding if unsure about:
  - Physics or methodology questions
  - Whether a claim needs fact-checking
  - Implementation choices affecting calculation accuracy
- Reference handoff document sections when explaining work

## Key Files
| File | Purpose |
|------|---------|
| `docs/wind_calculator_handoff_updated.md` | **READ FIRST** — Main briefing document |
| `wind_calculations.py` | Core calculation module (finalized, validated) |
| `Panel_app_pkg.ipynb` | Reference design for Panel app |
| `environment.yml` | Conda environment (finalized) |

## Code Style
- Use NumPy-style docstrings (established in wind_calculations.py)
- Include Formula and Source sections in docstrings
- Validate against Ginsberg's worked example when making calculation changes
EOF
```

- [ ] `CLAUDE_INSTRUCTIONS.md` created

### 6.2 Verify the file was created

```bash
cat CLAUDE_INSTRUCTIONS.md | head -20
```

Should show the beginning of the instructions file.

- [ ] File content verified

---

## Phase 7: Start Claude Session in VSCode

### 7.1 Open key files in VSCode tabs

Open these files in separate tabs (so Claude has context):

1. Click on `docs/wind_calculator_handoff_updated.md` in the file explorer
2. Click on `wind_calculations.py`
3. Click on `Panel_app_pkg.ipynb`
4. Click on `CLAUDE_INSTRUCTIONS.md`

**Why:** When you open Claude/Copilot chat, it can see the files you have open as context.

- [ ] Handoff document open
- [ ] wind_calculations.py open
- [ ] Panel notebook open
- [ ] Instructions file open

### 7.2 Open Claude/Copilot chat

**If using GitHub Copilot Chat:**
- Click the chat icon in the sidebar, or
- Press `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Shift+I` (Mac)

**If using Claude extension:**
- Open the Claude panel from the sidebar

- [ ] Chat interface open

### 7.3 Send the starting prompt

Copy and paste this entire prompt:

```
I'm handing off an offshore wind calculator project for you to continue developing.

**Please start by reading these files in order:**
1. `CLAUDE_INSTRUCTIONS.md` — Project constraints and guidelines
2. `docs/wind_calculator_handoff_updated.md` — Main briefing document (comprehensive)

The handoff document contains:
- Section 0: Project setup (already done — I've created the env and validated calculations)
- Sections 1-2: Project overview and methodology (Ginsberg 2019 Swept Area Method)
- Section 3: Current implementation details
- Section 4: Required changes (including Binder deployment fix)
- Sections 5-8: File-by-file tasks, testing, code templates, references

**What's already done:**
- ✅ `wind_calculations.py` — Core calculation module (finalized, validated)
- ✅ `environment.yml` — Conda environment (working, activated)
- ✅ Ginsberg validation test passes (104 W/m², 204 kW, 357 MWh/year)
- ✅ Project structure set up with docs/ and tests/ directories

**Critical constraints (from CLAUDE_INSTRUCTIONS.md):**
- Do not invent data or claims not already fact-checked
- Follow Ginsberg (2019) exactly for methodology
- Consult CURRENT Panel docs for Binder (not 2020-2021 patterns)
- EPF = 1.91 is fixed; spacing_factor has no default (intentional)

**Your first tasks:**
1. Confirm you've read both instruction files
2. Summarize your understanding of the project and primary tasks
3. Ask any clarifying questions before starting work

Please confirm you understand the project before we proceed.
```

- [ ] Starting prompt sent

### 7.4 Wait for Claude to respond

**Claude should:**
1. ✅ Confirm it read the handoff and instructions
2. ✅ Summarize understanding of the project
3. ✅ Summarize the primary tasks from Section 4
4. ✅ Ask any clarifying questions
5. ✅ Propose next steps or ask which task to start with

**If Claude's summary seems wrong:**
- Correct any misunderstandings immediately
- Point to specific sections in the handoff document
- Ask it to re-read if needed

- [ ] Claude confirmed understanding
- [ ] Summary is accurate
- [ ] Ready to proceed with first task

### 7.5 Guide the first task

After Claude confirms understanding, direct it to a specific task:

**Recommended first task:**
```
Great, let's start with creating the Panel notebook. 

Please review Section 3.3 of the handoff document which describes the UI design, 
then create a new Panel_app.ipynb that:
1. Imports wind_calculations as wc
2. Implements the single turbine section
3. Implements the site section  
4. Uses the @pn.depends decorator for reactivity

Start with the imports and widget definitions, then show me what you have 
before building the full layout.
```

**Or for Binder deployment (if that's more urgent):**
```
Let's focus on fixing Binder deployment first.

Please:
1. Read Section 4.4 of the handoff document
2. Research the CURRENT Panel Binder documentation at https://panel.holoviz.org/how_to/deployment/binder.html
3. Propose a plan for restructuring the notebook for dual local/Binder deployment

Don't make changes yet — just show me your proposed approach first.
```

- [ ] First task assigned
- [ ] Working on project!

---

## Quick Reference

### Essential Commands

| Action | Command |
|--------|---------|
| Activate environment | `conda activate wind-panel-app` |
| Deactivate environment | `conda deactivate` |
| Verify import | `python -c "import wind_calculations as wc; print('OK')"` |
| Run tests (once created) | `python -m pytest -v` |
| Launch Jupyter notebook | `jupyter notebook Panel_app_pkg.ipynb` |
| Check Python version | `python --version` |
| List conda environments | `conda env list` |

### Ginsberg Validation Numbers

These are the "known good" values from Ginsberg (2019), pp. 60-62:

| Parameter | Expected Value |
|-----------|----------------|
| Power density | 104 W/m² |
| Mean power | 204 kW |
| AEP (non-derated) | 1,787 MWh/year |
| AEP (20% efficiency) | 357 MWh/year |

**Inputs:** D=50m, v=4.47 m/s, ρ=1.225 kg/m³, EPF=1.91, η=0.20

### Key Constants in wind_calculations.py

```python
HOURS_PER_YEAR = 8760
EPF_RAYLEIGH = 1.91      # Energy Pattern Factor for Rayleigh (Weibull k=2)
BETZ_LIMIT = 0.593       # Theoretical maximum (59.3%)
DEFAULT_EFFICIENCY = 0.20 # Ginsberg's conservative value
```

### Key Files Summary

| File | Purpose | Modify? |
|------|---------|---------|
| `wind_calculations.py` | Core calculations | ❌ No (finalized) |
| `environment.yml` | Conda environment | ❌ No (finalized) |
| `Panel_app_pkg.ipynb` | Panel app | ✅ Yes (to be enhanced) |
| `docs/wind_calculator_handoff_updated.md` | Main briefing | 📖 Reference |
| `CLAUDE_INSTRUCTIONS.md` | Claude constraints | 📖 Reference |

---

## Troubleshooting

### Conda Issues

**"conda: command not found"**
```bash
# Mac/Linux: Initialize conda for your shell
source ~/anaconda3/etc/profile.d/conda.sh  # or miniconda3
conda init bash  # or zsh

# Then restart your terminal
```

**"CondaHTTPError" or network issues**
```bash
# Check your internet connection, then:
conda config --set ssl_verify false  # temporary workaround
conda env create -f environment.yml
conda config --set ssl_verify true   # restore
```

**"environment already exists"**
```bash
# Remove and recreate
conda env remove -n wind-panel-app
conda env create -f environment.yml
```

**Environment not showing in list**
```bash
conda env list  # Check what's available
# If wind-panel-app not listed, create it:
conda env create -f environment.yml
```

### Python/Import Issues

**"ModuleNotFoundError: No module named 'wind_calculations'"**
- Check you're in the project directory: `pwd`
- Check the file exists: `ls wind_calculations.py`
- Check environment is activated: should see `(wind-panel-app)` in prompt

**"ModuleNotFoundError: No module named 'panel'"**
- Environment not activated. Run: `conda activate wind-panel-app`
- Or wrong Python being used. Check: `which python`

**Validation test fails (wrong numbers)**
1. Re-download `wind_calculations.py` from Claude.ai session
2. Check file has these constants near the top:
   - `EPF_RAYLEIGH = 1.91`
   - `HOURS_PER_YEAR = 8760`
3. Check `annual_power_density()` uses `energy_pattern_factor` parameter

### VSCode Issues

**Wrong Python interpreter selected**
1. `Cmd+Shift+P` → "Python: Select Interpreter"
2. Choose `wind-panel-app`
3. If not listed, enter path manually:
   - Mac/Linux: `~/anaconda3/envs/wind-panel-app/bin/python`
   - Windows: `C:\Users\YourName\anaconda3\envs\wind-panel-app\python.exe`

**Terminal doesn't show (wind-panel-app)**
```bash
# In VSCode terminal:
conda activate wind-panel-app
```

**Jupyter notebook won't open**
```bash
# Check jupyter is installed
python -c "import jupyter; print('OK')"

# If not, install it
conda install -n wind-panel-app notebook
```

### Panel App Issues

**"Panel app won't display"**
- Check `jupyter_bokeh` is installed: `python -c "import jupyter_bokeh; print('OK')"`
- If not: `conda install -c conda-forge jupyter_bokeh`

**"TypeError" when running app**
- Check `spacing_factor` is being passed explicitly (no default)
- Check efficiency is being converted from percent to decimal (20 → 0.20)

### Git Issues

**"fatal: not a git repository"**
- Run `git init` in project folder

**"Permission denied" on push**
- Check your GitHub authentication
- Try: `git remote set-url origin https://github.com/mycarta/wind-calculator.git`

---

## Final Checklist

Before starting Claude session, verify:

- [ ] **Phase 1:** All files downloaded and located
- [ ] **Phase 2:** Project structure created correctly
- [ ] **Phase 3:** Conda environment working
  - [ ] `conda activate wind-panel-app` works
  - [ ] All package imports work
  - [ ] Ginsberg validation passes (104, 204, 1787, 357)
- [ ] **Phase 4:** Initial git commit made
- [ ] **Phase 5:** VSCode configured
  - [ ] Correct interpreter selected
  - [ ] Terminal uses `wind-panel-app` environment
- [ ] **Phase 6:** `CLAUDE_INSTRUCTIONS.md` created
- [ ] **Phase 7:** Ready to start Claude session
  - [ ] Key files open in tabs
  - [ ] Starting prompt ready to paste

**You're ready to hand off to Claude! 🎉**

---

## What to Do If You Get Stuck

1. **Re-read the relevant section** of this checklist
2. **Check the troubleshooting section** above
3. **Search the error message** — conda and Python errors are well-documented online
4. **Ask Claude** (in a separate chat if needed) for help with the specific error
5. **Restart from scratch** if needed — Phase 3 is safe to redo

---

*Checklist created: January 21, 2026*  
*For: Wind Calculator VSCode/Claude Handoff*

