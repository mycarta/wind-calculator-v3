# Wind Calculator Project: Comprehensive Handoff Document

**Date:** January 20, 2026 (Updated: January 21, 2026)  
**From:** Claude (Anthropic)  
**To:** VSCode + GitHub Copilot (Claude Sonnet) environment  
**Repository:** https://github.com/mycarta/wind-calculator

---

## Executive Summary

This document provides a complete handoff for continuing development of the offshore wind calculator project. The calculator implements Ginsberg's (2019) Swept Area Method using Northeast Atlantic US data (von Krauland et al., 2023) as a proxy for Scotian Shelf (Nova Scotia) offshore wind conditions.

**Current Status:**
- Working Panel app with reactive UI
- Correct implementation of Ginsberg's methodology
- Uses EPF = 1.91 (Rayleigh distribution correction)
- Employs conservative efficiency range (20-30%)
- Includes comprehensive test suite
- **Known issue:** Binder deployment not working (local deployment works fine)

**Primary Tasks Ahead:**
1. Update README.md with new structure
2. Enhance app UI with additional context
3. Add documentation tooltips
4. **Fix Binder deployment** — restructure notebook for dual local/Binder deployment using current Panel best practices
5. Optional: implement spacing-efficiency coupling
6. Optional: minor code quality improvements (see Section 4.5)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Core Physics and Methodology](#2-core-physics-and-methodology)
3. [Current Implementation Details](#3-current-implementation-details)
4. [Required Changes](#4-required-changes)
5. [File-by-File Action Items](#5-file-by-file-action-items)
6. [Testing Strategy](#6-testing-strategy)
7. [Code Snippets and Templates](#7-code-snippets-and-templates)
8. [References and Resources](#8-references-and-resources)

---

## 1. Project Overview

### 1.1 Purpose

Interactive web-based calculator for offshore wind farm planning, specifically adapted for Scotian Shelf (Nova Scotia) conditions using the best available published analogue data (Northeast Atlantic US).

### 1.2 Technology Stack

- **Backend:** Python 3.12
- **Calculations:** Custom `wind_calculations.py` module
- **UI:** Panel (HoloViews/Bokeh-based)
- **Deployment:** Jupyter notebook → Panel server (local works; Binder needs fix)
- **Testing:** pytest with property-based tests (Hypothesis)

### 1.3 Key Design Decisions

1. **Follows Ginsberg (2019) exactly** — uses his terminology, formulas, and conservative values
2. **Uses NE Atlantic US data as proxy** — von Krauland et al. (2023) provides closest published offshore wind resource data
3. **Conservative planning focus** — 20-30% efficiency range, tight spacing (5.98D)
4. **Educational tool** — emphasizes transparency of assumptions and limitations

---

## 2. Core Physics and Methodology

### 2.1 The Fundamental Power Equation

**Wind power available in swept area:**

```
P = ½ρAv³
```

Where:
- P = power (W)
- ρ = air density (kg/m³)
- A = swept area = πD²/4 (m²)
- v = wind velocity (m/s)

**Critical insight:** Power scales as v³ (cubic). This means:
- 2× wind speed → 8× power
- 10% error in wind speed → ~33% error in power estimate

**Why v³?** The velocity does "double duty":
1. Determines delivery rate (mass flow: ρAv)
2. Determines energy content (kinetic energy: ½mv²)

Result: v appears three times (v × v²).

### 2.2 Energy Pattern Factor (EPF)

**The Problem:**

You cannot use average wind speed directly in the power equation:

```
⟨P⟩ ≠ ½ρA⟨v⟩³
```

Because v³ is nonlinear (convex), Jensen's inequality tells us:

```
⟨v³⟩ > ⟨v⟩³
```

**The Solution: EPF**

For a Rayleigh wind distribution (Weibull shape parameter k=2), the ratio is:

```
EPF = ⟨v³⟩ / ⟨v⟩³ ≈ 1.91
```

**Therefore, the correct formula for mean power is:**

```
P̄ₐ = ½ρ · EPF · v̄³     [W/m²]
```

Where:
- P̄ₐ = mean power density
- v̄ = average wind speed
- EPF = 1.91 (for Rayleigh/k=2)

**Source:** Ginsberg (2019), pp. 56-59. He calls this the "Energy Pattern Factor" and explicitly uses EPF = 1.91 for Rayleigh distributions.

### 2.3 Overall Conversion Efficiency

**Ginsberg's "Overall Conversion Efficiency" = 20%**

This single parameter accounts for ALL losses from theoretical wind kinetic energy to delivered electrical energy:

1. **Betz limit & real Cp:** Maximum theoretical = 59.3%, real turbines ≈ 40-45%
2. **Availability:** Turbine operational time ≈ 95-97%
3. **Wake losses:** Downstream turbines in wind shadow ≈ 5-15% (depends on spacing)
4. **Electrical losses:** Transformers, cables, converters ≈ 2-3%
5. **Power curve effects:** Cut-in (v < ~3-4 m/s), rated wind speed capping, cut-out (v > ~25 m/s)

**Net result:** 0.593 × 0.40 × 0.95 × 0.90 × 0.97 ≈ 0.195 ≈ **20%**

**Calculator implementation:** Allows 20-30% range for flexibility, but Ginsberg recommends 20% for conservative planning.

### 2.4 Complete Calculation Chain

```
1. Swept Area
   A = πD²/4

2. Mean Power Density (EPF-adjusted)
   P̄ₐ = ½ρ · EPF · v̄³

3. Mean Power (single turbine)
   P̄ = P̄ₐ · A

4. Annual Energy (non-derated)
   AEP_nd = P̄ × 8,760 hours

5. Annual Energy (derated)
   AEP_d = η × AEP_nd

6. Site Totals
   Multiply by N turbines (from available area ÷ spacing)
```

### 2.5 Ginsberg Worked Example (Validation)

**Inputs:**
- D = 50 m
- v̄ = 4.47 m/s
- ρ = 1.225 kg/m³ (sea level)
- EPF = 1.91
- η = 0.20 (20%)

**Calculation:**

```
A = π(50)²/4 = 1,963.5 m²

P̄ₐ = 0.5 × 1.225 × 1.91 × (4.47)³
   = 0.5 × 1.225 × 1.91 × 89.31
   = 104 W/m²

P̄ = 104 × 1,963.5 = 204,204 W = 204 kW

AEP_nd = 204 × 8,760 / 1,000 = 1,787 MWh/year

AEP_d = 0.20 × 1,787 = 357 MWh/year
```

**This is included as a unit test in the repository.**

---

## 3. Current Implementation Details

### 3.1 Repository Structure

```
wind-calculator/
├── Panel_app_pkg.ipynb          # Main application notebook
├── wind_calculations.py          # Core calculation functions
├── README.md                     # Documentation (NEEDS UPDATE)
├── environment.yml               # Conda environment spec
├── tests/
│   └── test_wind_calculations.py # Test suite
├── docs/                         # Additional documentation
└── .vscode/                      # VSCode settings
```

### 3.2 wind_calculations.py Module

**Key Functions:**

```python
# Lookup tables (from von Krauland et al. 2023)
air_density_lookup = {
    100: <value>,  # kg/m³ at 100m hub height
    150: <value>,
    200: 0.990,
    250: <value>
}

wind_speed_lookup = {
    100: <value>,  # m/s average at 100m
    150: <value>,
    200: <value>,
    250: <value>
}

# Core functions
def swept_area(diameter):
    """Calculate swept area (m²) from rotor diameter (m)"""
    return np.pi * (diameter/2)**2

def annual_power_density(wind_speed, air_density, epf=1.91):
    """Calculate mean power density (W/m²)
    
    Args:
        wind_speed: average wind speed (m/s)
        air_density: kg/m³
        epf: Energy Pattern Factor (default 1.91 for Rayleigh)
    
    Returns:
        Power density in W/m²
    """
    return 0.5 * air_density * epf * wind_speed**3

def power_kw(power_density, diameter):
    """Calculate mean power (kW) for turbine"""
    area = swept_area(diameter)
    return (power_density * area) / 1000

def annual_energy_output(power_kw):
    """Non-derated annual energy (MWh/year)"""
    return power_kw * 8760 / 1000

def derated_annual_energy_output(power_kw, efficiency):
    """Derated annual energy (MWh/year)
    
    Args:
        power_kw: mean power (kW)
        efficiency: overall conversion efficiency (0.20-0.30)
    """
    return efficiency * annual_energy_output(power_kw)

def possible_turbine_installations(available_area_km2, diameter, spacing_factor):
    """Calculate number of turbines that fit on site
    
    Args:
        available_area_km2: site area (km²)
        diameter: rotor diameter (m)
        spacing_factor: center-to-center spacing as multiple of D
    
    Returns:
        Integer number of turbines
    """
    spacing_m = diameter * spacing_factor
    spacing_km = spacing_m / 1000
    area_per_turbine_km2 = spacing_km ** 2
    return int(available_area_km2 / area_per_turbine_km2)
```

### 3.3 Panel App Structure (Panel_app_pkg.ipynb)

**Current UI Elements:**

1. **Single Turbine Section:**
   - Rotor diameter dropdown (100, 150, 200, 250 m)
   - Displays: air density, wind speed (from lookup tables)
   - Power unit selector (kW, MW, GW)
   - Energy unit selector (MWh/year, GWh/year, TWh/year)
   - Efficiency slider (20-30%)
   - Outputs: swept area, power density, mean power, AEP (non-derated and derated)

2. **Site Section:**
   - Available area slider (100-1000 km², step 50)
   - Spacing factor slider (3.0-9.0, default 5.98)
   - Displays: turbine count, spacing (m), total power, total AEP

3. **Info Icons:**
   - Tooltips on hover for explanations

**Current Calculation Flow:**

```python
@pn.depends(rotor_diameter, available_area, spacing_factor, efficiency, power_unit, energy_unit)
def results_panel(...):
    # 1. Get lookup values
    air_density = wc.air_density_lookup[rotor_diameter]
    wind_speed = wc.wind_speed_lookup[rotor_diameter]
    
    # 2. Calculate single turbine
    pd = wc.annual_power_density(wind_speed, air_density)
    area = wc.swept_area(rotor_diameter)
    pk = wc.power_kw(pd, rotor_diameter)
    energy_nd = wc.annual_energy_output(pk)
    energy_d = wc.derated_annual_energy_output(pk, efficiency/100)
    
    # 3. Calculate site
    turbines = wc.possible_turbine_installations(area_km2, rotor_diameter, spacing_factor)
    site_power = pk * turbines
    site_energy_nd = energy_nd * turbines
    site_energy_d = energy_d * turbines
    
    # 4. Scale to selected units and format
    # 5. Return formatted pn.Column with all outputs
```

### 3.4 Current Test Coverage

**test_wind_calculations.py includes:**

1. Known values test (Ginsberg worked example)
2. Swept area calculation
3. Power density calculation
4. Energy calculations
5. Turbine installation count
6. Property-based tests (if Hypothesis installed)

**Example test:**

```python
def test_annual_power_density_known_values():
    """Ginsberg worked example: v=4.47 m/s, ρ=1.225, EPF=1.91"""
    result = wc.annual_power_density(4.47, 1.225, epf=1.91)
    assert abs(result - 104) < 1  # ~104 W/m²
```

### 3.5 Current Deployment Status

**What works:**
- Local deployment via `pn.serve(app_panel)` in Jupyter notebook
- App launches in browser at `http://localhost:<port>`

**What doesn't work:**
- Binder deployment (attempted ~2020-2021, methods now outdated)
- The current notebook structure uses `pn.serve()` which is appropriate for local use but not for Binder

**Root cause:**
- Panel deployment patterns have changed significantly since 2020-2021
- Binder requires specific configuration (e.g., `jupyter_panel_config.py` or `postBuild` scripts)
- The notebook needs restructuring to support both local and Binder deployment modes

---

## 4. Required Changes

### 4.1 README.md Complete Rewrite

**Current issues:**
- Doesn't clearly separate Ginsberg methodology validation from operational use
- Doesn't explain EPF well enough
- Doesn't clarify that NE Atlantic US is proxy for Scotian Shelf
- Doesn't explain what "efficiency" means

**New structure needed:**
1. Overview
2. Methodology (Ginsberg Swept Area Method)
3. Ginsberg Worked Example (validation)
4. Regional Application (NE Atlantic US → Scotian Shelf proxy)
5. Data sources and lookup tables
6. Default parameters with full explanations
7. Calculations and formulas
8. Assumptions and limitations (detailed)
9. Running tests
10. AI/HI statement (keep as-is)
11. References

**See Section 7.1 for complete new README text.**

### 4.2 Panel App Enhancements

**Add to UI (priority order):**

1. **Source attribution** (top of app):
   ```python
   pn.pane.Markdown("**Methodology:** Ginsberg (2019) Swept Area Method | **Data:** von Krauland et al. (2023) NE Atlantic US")
   ```

2. **EPF visibility** (in single turbine section):
   ```python
   pn.Row(
       pn.pane.Markdown("**Energy Pattern Factor (EPF):** 1.91"),
       info_icon("Rayleigh wind distribution correction factor (Weibull k=2). Converts ⟨v⟩³ to ⟨v³⟩.")
   )
   ```

3. **Improved efficiency tooltip**:
   ```python
   efficiency_input = pn.widgets.IntInput(
       name="Overall Conversion Efficiency (%)",
       start=20, end=30, step=1, value=20
   )
   info_icon("Overall conversion from wind kinetic energy to electrical output. "
             "Includes: turbine Cp (~40%), availability (~95%), wake losses (~10-15%), "
             "electrical losses (~3%), power curve effects. "
             "Ginsberg (2019) recommends 20% for conservative planning.")
   ```

4. **Hub height display**:
   ```python
   hub_height_lookup = {100: 100, 150: 150, 200: 200, 250: 250}
   pn.pane.Markdown(f"**Hub Height:** {hub_height_lookup[rotor_diameter]} m")
   ```

5. **Spacing-efficiency warning** (conditional):
   ```python
   if spacing_factor < 6.5 and efficiency > 25:
       pn.pane.Markdown(
           "⚠️ **Warning:** Tight spacing (F < 6.5D) typically requires "
           "efficiency < 25% due to increased wake losses.",
           styles={'color': 'orange'}
       )
   ```

6. **Wind speed source tooltip**:
   ```python
   info_icon("Average wind speed at hub height. Source: von Krauland et al. (2023), "
             "Northeast Atlantic US offshore data (proxy for Scotian Shelf).")
   ```

**Optional enhancements:**
- Add "Show formulas" expander with LaTeX equations
- Add "About this calculator" modal with full methodology
- Export results to CSV/Excel
- Comparison mode (multiple scenarios side-by-side)

### 4.3 Documentation Files

**Create new file:** `docs/methodology.md`
- Deep dive into why EPF is needed
- Explanation of v³ relationship (carrier = cargo concept)
- Integration vs. averaging discussion
- When to use this tool vs. full wind resource assessment

**Create new file:** `docs/regional_adaptation.md`
- Why NE Atlantic US is good proxy for Scotian Shelf
- Oceanographic and meteorological similarities
- Limitations of proxy data
- Recommendation for site-specific measurements

### 4.4 Binder Deployment Configuration (PRIMARY TASK)

**Problem:** The current notebook uses `pn.serve(app_panel)` which works locally but not on Binder. Panel deployment best practices have evolved significantly since 2020-2021.

**Goal:** Restructure the notebook to support **dual deployment modes**:
1. **Local mode:** Run cells, app launches in browser via `pn.serve()`
2. **Binder mode:** App renders inline in notebook or via Panel's Binder-compatible serving

**Required research:** Consult current Panel documentation for Binder deployment:
- https://panel.holoviz.org/how_to/deployment/index.html
- https://panel.holoviz.org/how_to/deployment/binder.html
- Check for `jupyter_panel_config.py` requirements
- Check for `postBuild` script requirements
- Review current `environment.yml` for necessary dependencies

**Implementation approach:**

1. **Restructure notebook cells:**

   **Cell 1: Imports** (no change)
   ```python
   import wind_calculations as wc
   import panel as pn
   ```

   **Cell 2: Environment detection**
   ```python
   # Detect if running on Binder or locally
   import os
   ON_BINDER = 'BINDER_SERVICE_HOST' in os.environ
   # Alternative detection methods may be needed - research current best practice
   ```

   **Cell 3: Panel extension with appropriate config**
   ```python
   if ON_BINDER:
       pn.extension(sizing_mode='stretch_width')  # or other Binder-appropriate settings
   else:
       pn.extension()
   ```

   **Cell 4: All widget and function definitions** (existing code, no changes)

   **Cell 5: App assembly** (existing `app_panel` definition)

   **Cell 6: Deployment (SPLIT INTO TWO OPTIONS)**
   
   **Cell 6a: For Binder (inline display)**
   ```python
   # Run this cell on Binder
   if ON_BINDER:
       app_panel.servable()  # or app_panel for inline display
   ```
   
   **Cell 6b: For local development**
   ```python
   # Run this cell locally (launches browser)
   if not ON_BINDER:
       pn.serve(app_panel)
   ```

2. **Create/update Binder configuration files:**

   **`postBuild`** (if needed):
   ```bash
   #!/bin/bash
   # Panel Binder configuration
   jupyter serverextension enable panel.io.jupyter_server_extension
   # Add other setup as needed per current Panel docs
   ```

   **`jupyter_panel_config.py`** (if needed):
   ```python
   # Configuration for Panel on JupyterHub/Binder
   # Consult current Panel documentation for correct settings
   c.ServerApp.jpserver_extensions = {
       'panel.io.jupyter_server_extension': True
   }
   ```

   **Update `environment.yml`:**
   - Ensure Panel version is current
   - Add any Binder-specific dependencies
   - Consider pinning versions for reproducibility

3. **Add Binder badge to README:**
   ```markdown
   [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mycarta/wind-calculator/HEAD?urlpath=panel/Panel_app_pkg)
   ```
   Note: The `urlpath` parameter may need adjustment based on current Panel/Binder integration.

**Critical:** The exact implementation will depend on **current Panel documentation** (as of 2025-2026). The patterns from 2020-2021 are likely outdated. The developer should:
1. Read the current Panel deployment docs thoroughly
2. Test on a fresh Binder build
3. Consider using Panel's recommended Binder template if one exists

**Testing checklist:**
- [ ] App runs locally with `pn.serve()`
- [ ] App displays inline in notebook (for Binder)
- [ ] Binder badge link works
- [ ] All widgets are responsive on Binder
- [ ] No JavaScript/WebSocket errors in Binder console

### 4.5 Minor Code Quality Improvements (LOW PRIORITY)

These are optional refactoring suggestions that improve maintainability but don't affect functionality:

**1. Split `results_panel()` into smaller functions**

The current `results_panel()` function is ~100 lines. Consider splitting into:
```python
def single_turbine_section(rotor_diameter, efficiency, p_unit, e_unit):
    """Build the single turbine output section."""
    # ... single turbine logic
    return pn.Column(...)

def site_section(rotor_diameter, available_area_km2, spacing_factor, efficiency, p_unit, e_unit):
    """Build the site output section."""
    # ... site logic
    return pn.Column(...)

@pn.depends(...)
def results_panel(...):
    """Main reactive panel combining all sections."""
    return pn.Column(
        source_banner(),
        single_turbine_section(...),
        site_section(...)
    )
```

**Benefits:**
- Easier to test individual sections
- Clearer separation of concerns
- Easier to modify one section without affecting others

**2. Create helper for repeated row pattern**

The pattern `pn.Row(pn.pane.Markdown(...), info_icon(...))` appears many times. Abstract it:
```python
def labeled_output(label, value, tooltip, unit=""):
    """Create a labeled output row with info tooltip.
    
    Args:
        label: Display label (e.g., "Swept Area")
        value: Numeric value to display
        tooltip: Explanation text for info icon
        unit: Optional unit string (e.g., "m²", "kW")
    
    Returns:
        pn.Row with formatted label, value, and info icon
    """
    if unit:
        text = f"**{label}:** {value:,.2f} {unit}"
    else:
        text = f"**{label}:** {value:,.2f}"
    return pn.Row(
        pn.pane.Markdown(text),
        info_icon(tooltip)
    )
```

**Usage:**
```python
labeled_output("Swept Area", out['swept_area'], "Area swept by the turbine blades", "m²")
labeled_output("Mean Power", single_power_scaled, "Mean power based on EPF-adjusted calculation", p_unit)
```

**Benefits:**
- Reduces code duplication
- Consistent formatting across all outputs
- Single place to change styling

**3. Remove redundant efficiency helper text**

Current code has:
```python
pn.pane.Markdown("<span style='color:#555;'>Please select a value between 20 and 30</span>")
```

This is redundant because `IntInput` already constrains the range with `start=20, end=30`. Remove it or replace with more useful guidance about what efficiency values mean.

**4. Consider extracting constants**

Currently, magic numbers like `8760` (hours/year) are inline. Consider:
```python
# At top of wind_calculations.py
HOURS_PER_YEAR = 8760
EPF_RAYLEIGH = 1.91
BETZ_LIMIT = 0.593
```

**Benefits:**
- Self-documenting code
- Single source of truth
- Easier to find and update if needed

---

## 5. File-by-File Action Items

### 5.1 README.md

**Action:** Complete rewrite

**Template provided in Section 7.1**

**Key changes:**
- Add Ginsberg worked example as validation
- Clarify NE Atlantic US as proxy
- Explain EPF thoroughly
- Detail what "efficiency" includes
- Add assumptions and limitations section
- Add Binder badge and deployment instructions

### 5.2 Panel_app_pkg.ipynb

**Action:** Enhance UI with context AND restructure for dual deployment

**Specific edits needed:**

1. **Cell 1 (imports) - no changes**

2. **NEW Cell 2 (environment detection):**
```python
# Detect deployment environment
import os
ON_BINDER = 'BINDER_SERVICE_HOST' in os.environ
print(f"Running on Binder: {ON_BINDER}")
```

3. **Cell 3 (was Cell 2 - main app code):**

Add after `pn.extension()`:

```python
# Source attribution banner
source_banner = pn.pane.Markdown(
    "### Methodology: Ginsberg (2019) Swept Area Method | "
    "Data: von Krauland et al. (2023) Northeast Atlantic US",
    styles={'background-color': '#f0f0f0', 'padding': '10px', 'border-radius': '5px'}
)
```

Add EPF display in `results_panel()` function, in single turbine section:

```python
pn.Row(
    pn.pane.Markdown("**Energy Pattern Factor (EPF):** 1.91"),
    info_icon("Rayleigh distribution correction: ⟨v³⟩/⟨v⟩³ ≈ 1.91 for Weibull k=2")
)
```

Update efficiency widget:

```python
efficiency_input = pn.widgets.IntInput(
    name="Overall Conversion Efficiency (%)",  # Changed from just "Efficiency"
    start=20, end=30, step=1, value=20
)
```

Add conditional warning before site section:

```python
# In results_panel(), calculate this early:
efficiency_pct = efficiency  # from function parameter
show_warning = spacing_factor < 6.5 and efficiency_pct > 25

# Then in the layout, before site_row:
warning_row = pn.Row()
if show_warning:
    warning_row = pn.pane.Markdown(
        "⚠️ **Spacing-Efficiency Alert:** Tight spacing (F < 6.5D) increases "
        "wake losses. Consider reducing efficiency to < 25% for more realistic estimates.",
        styles={'color': '#ff8c00', 'padding': '10px', 'border': '1px solid #ff8c00'}
    )
```

Update final return to include source_banner:

```python
return pn.Column(
    source_banner,
    single_turbine_row,
    warning_row,
    site_row
)
```

4. **NEW Cell 4 (Binder deployment):**
```python
# === RUN THIS CELL ON BINDER ===
# Displays app inline in notebook
if ON_BINDER:
    app_panel.servable()
    # or simply: app_panel
```

5. **Cell 5 (was Cell 3 - local deployment):**
```python
# === RUN THIS CELL FOR LOCAL DEVELOPMENT ===
# Launches app in browser
if not ON_BINDER:
    pn.serve(app_panel)
```

### 5.3 wind_calculations.py

**Action:** Add docstrings if missing, ensure EPF parameter

Verify that `annual_power_density()` has:

```python
def annual_power_density(wind_speed, air_density, epf=1.91):
    """Calculate EPF-adjusted mean power density.
    
    Uses Energy Pattern Factor to correct for wind speed distribution.
    For Rayleigh distribution (Weibull k=2), EPF ≈ 1.91.
    
    Args:
        wind_speed: Average wind speed at hub height (m/s)
        air_density: Air density at hub height (kg/m³)
        epf: Energy Pattern Factor (default 1.91)
    
    Returns:
        Mean power density (W/m²)
    
    Formula:
        P̄ₐ = ½ρ · EPF · v̄³
    
    Source:
        Ginsberg, M. (2019). Harness It, pp. 56-59.
    """
    return 0.5 * air_density * epf * (wind_speed ** 3)
```

### 5.4 tests/test_wind_calculations.py

**Action:** Verify Ginsberg worked example test exists

Ensure this test is present:

```python
def test_ginsberg_worked_example():
    """
    Validate implementation against Ginsberg (2019) worked example.
    
    Reference: Ginsberg, M. (2019). Harness It, pp. 60-62.
    
    Inputs:
        D = 50 m
        v̄ = 4.47 m/s
        ρ = 1.225 kg/m³
        EPF = 1.91
        η = 0.20
    
    Expected outputs:
        Power density ≈ 104 W/m²
        Swept area = 1,963.5 m²
        Power ≈ 204 kW
        AEP (non-derated) ≈ 1,787 MWh/year
        AEP (derated, 20%) ≈ 357 MWh/year
    """
    # Power density
    pd = wc.annual_power_density(4.47, 1.225, epf=1.91)
    assert abs(pd - 104) < 1.0, f"Expected ~104 W/m², got {pd}"
    
    # Swept area
    area = wc.swept_area(50)
    assert abs(area - 1963.5) < 0.5, f"Expected 1,963.5 m², got {area}"
    
    # Power
    power = wc.power_kw(pd, 50)
    assert abs(power - 204) < 1.0, f"Expected ~204 kW, got {power}"
    
    # Annual energy (non-derated)
    aep_nd = wc.annual_energy_output(power)
    assert abs(aep_nd - 1787) < 10, f"Expected ~1,787 MWh/year, got {aep_nd}"
    
    # Annual energy (derated)
    aep_d = wc.derated_annual_energy_output(power, 0.20)
    assert abs(aep_d - 357) < 5, f"Expected ~357 MWh/year, got {aep_d}"
```

### 5.5 Create docs/methodology.md

**Action:** New file documenting the v³ relationship and EPF

**Content outline:**
1. Why wind power scales as v³
2. The "carrier is the cargo" concept
3. Why you can't just use average wind speed
4. What EPF is and where 1.91 comes from
5. Rayleigh vs. Weibull distributions
6. When this approximation is valid

**See Section 7.3 for template.**

### 5.6 Create docs/scotian_shelf_proxy.md

**Action:** New file explaining regional adaptation

**Content:**
- Geographic context (Scotian Shelf location)
- Why NE Atlantic US is appropriate proxy
- Oceanographic similarities
- Meteorological regime similarities
- Limitations and when to use site-specific data

**See Section 7.4 for template.**

### 5.7 Binder Configuration Files (NEW)

**Action:** Create/update files for Binder deployment

**5.7.1 Update `environment.yml`:**
- Verify Panel version is current (check PyPI for latest stable)
- Add `jupyter_bokeh` if not present (may be required for inline rendering)
- Consider adding version pins for reproducibility

```yaml
name: wind-panel-app
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - panel>=1.0  # Update to current version
  - bokeh
  - jupyter_bokeh  # For inline Panel rendering
  - numpy
  - pytest
  - hypothesis  # Optional, for property-based tests
  - pip
  - pip:
    - # any pip-only dependencies
```

**5.7.2 Create `postBuild`** (if required by current Panel docs):
```bash
#!/bin/bash
set -ex

# Enable Panel server extension for Jupyter
jupyter serverextension enable --sys-prefix panel.io.jupyter_server_extension || true

# Any other Binder setup
echo "Binder postBuild complete"
```

Make executable: `chmod +x postBuild`

**5.7.3 Create `jupyter_panel_config.py`** (if required):
```python
# Panel configuration for JupyterHub/Binder
# Consult current Panel documentation for correct settings
```

**5.7.4 Update `README.md` with Binder badge:**
```markdown
## Try It Online

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mycarta/wind-calculator/HEAD?urlpath=panel/Panel_app_pkg)

Click the badge above to launch the calculator in your browser (no installation required).
```

**Critical note:** The exact Binder configuration depends on **current Panel documentation**. The developer should:
1. Check https://panel.holoviz.org/how_to/deployment/binder.html
2. Review any Panel Binder templates or examples
3. Test incrementally on mybinder.org

---

## 6. Testing Strategy

### 6.1 Regression Tests

**Already in place:**
- Ginsberg worked example (validates entire calculation chain)
- Unit tests for each function
- Property-based tests (if Hypothesis available)

**Run tests:**
```bash
# In conda environment
conda activate wind-panel-app
python -m pytest -v
```

### 6.2 Manual UI Testing Checklist

After making Panel app changes:

1. **Launch app locally:**
   ```bash
   jupyter notebook Panel_app_pkg.ipynb
   # Run all cells
   ```

2. **Test single turbine section:**
   - [ ] Select each rotor diameter (100, 150, 200, 250 m)
   - [ ] Verify air density and wind speed update from lookup tables
   - [ ] Verify EPF = 1.91 is displayed
   - [ ] Check tooltips appear on info icons
   - [ ] Change power units (kW → MW → GW) and verify scaling
   - [ ] Change energy units and verify scaling
   - [ ] Adjust efficiency slider (20-30%) and verify outputs update

3. **Test site section:**
   - [ ] Adjust available area slider
   - [ ] Adjust spacing factor slider
   - [ ] Verify turbine count updates
   - [ ] Verify spacing in meters is calculated correctly
   - [ ] Check site totals = single turbine × N

4. **Test warnings:**
   - [ ] Set spacing < 6.5D and efficiency > 25% → warning should appear
   - [ ] Adjust either parameter to dismiss warning

5. **Test edge cases:**
   - [ ] Minimum area (100 km²) with maximum diameter (250 m) and tight spacing (3.0)
   - [ ] Maximum area (1000 km²) with minimum diameter (100 m) and wide spacing (9.0)
   - [ ] Verify no crashes, reasonable outputs

### 6.3 Binder Deployment Testing (NEW)

**Test checklist for Binder:**

1. **Build test:**
   - [ ] Push changes to GitHub
   - [ ] Click Binder badge in README
   - [ ] Verify build completes without errors

2. **Functionality test on Binder:**
   - [ ] App renders inline in notebook
   - [ ] All widgets are interactive
   - [ ] Calculations update correctly
   - [ ] No JavaScript console errors
   - [ ] No WebSocket connection errors

3. **Performance test:**
   - [ ] App loads within reasonable time (< 30 seconds after build)
   - [ ] Widget responses are not sluggish

4. **Edge cases on Binder:**
   - [ ] Refresh browser — app should reload correctly
   - [ ] Multiple rapid widget changes — no crashes

### 6.4 Validation Checks

**Cross-check calculations manually:**

Example: D=100m, v̄=8 m/s, ρ=1.2 kg/m³, efficiency=25%

```python
# Manual calculation
A = 3.14159 * (50)**2 = 7,854 m²
P̄ₐ = 0.5 * 1.2 * 1.91 * (8**3) = 0.5 * 1.2 * 1.91 * 512 ≈ 587 W/m²
P̄ = 587 * 7,854 / 1000 ≈ 4,610 kW
AEP_nd = 4,610 * 8.76 ≈ 40,400 MWh/year
AEP_d = 0.25 * 40,400 ≈ 10,100 MWh/year
```

Verify app outputs match (within rounding).

---

## 7. Code Snippets and Templates

### 7.1 Complete New README.md

[Content unchanged from original handoff - see original Section 7.1]

### 7.2 Panel App Enhancement Code Block

[Content unchanged from original handoff - see original Section 7.2]

### 7.3 docs/methodology.md Template

[Content unchanged from original handoff - see original Section 7.3]

### 7.4 docs/scotian_shelf_proxy.md Template

[Content unchanged from original handoff - see original Section 7.4]

---

## 8. References and Resources

### 8.1 Key Papers

**von Krauland et al. (2023) - Primary data source:**
- Title: "United States offshore wind energy atlas: availability, potential, and economic insights based on wind speeds at different altitudes and thresholds and policy-informed exclusions"
- Journal: Applied Energy, Volume 345, 2023, 121243
- DOI: https://doi.org/10.1016/j.apenergy.2023.121243
- Key contributions: Comprehensive offshore wind resource data for Northeast Atlantic US, air density by altitude, wind speeds at multiple hub heights

**Ginsberg (2019) - Methodology source:**
- Title: "Harness It: Renewable Energy Technologies and Project Development Models Transforming the Grid"
- Publisher: Business Expert Press
- ISBN: 978-1-63157-931-8
- Key contributions: Swept Area Method, Energy Pattern Factor (EPF), conservative planning assumptions, worked examples

### 8.2 Panel Deployment Documentation (CRITICAL FOR BINDER TASK)

**Primary resources to consult:**
- Panel deployment overview: https://panel.holoviz.org/how_to/deployment/index.html
- Panel on Binder: https://panel.holoviz.org/how_to/deployment/binder.html
- Panel GitHub examples: https://github.com/holoviz/panel/tree/main/examples
- mybinder.org documentation: https://mybinder.readthedocs.io/

**Note:** Deployment best practices evolve rapidly. Always check the **current** documentation rather than relying on 2020-2021 patterns.

### 8.3 Important Concepts

**Betz Limit:**
- Theoretical maximum efficiency: 59.3%
- Real turbines achieve 40-45%
- Represents maximum fraction of wind kinetic energy that can be extracted

**Capacity Factor:**
- Ratio: Actual annual energy / (Nameplate power × 8,760 hours)
- NOT the same as the "efficiency" parameter in this calculator
- Typical offshore: 40-50%
- Related but distinct from conversion efficiency

**Weibull Distribution:**
- Characterized by shape (k) and scale (λ) parameters
- k=2 is Rayleigh distribution
- Offshore wind typically k=1.8-2.2
- Determines EPF value

### 8.4 Terminology Clarifications

**Power vs. Energy:**
- Power (W, kW, MW): Instantaneous rate
- Energy (Wh, kWh, MWh): Accumulated over time
- Relationship: Energy = Power × Time

**Mean vs. Average:**
- Used interchangeably in this calculator
- Both refer to time-averaged quantities
- Denoted with overbar (P̄) in equations

**Derated vs. Non-derated:**
- Non-derated: Before applying efficiency losses
- Derated: After applying efficiency losses
- This calculator provides both for comparison

### 8.5 Common Pitfalls

1. **Using ⟨v⟩³ directly** → Underestimates by ~50%
   - Must use EPF correction

2. **Confusing capacity factor with efficiency** → Different concepts
   - Capacity factor: ratio to nameplate
   - Efficiency (here): ratio to wind kinetic energy

3. **Ignoring wake losses** → Overestimates for wind farms
   - Single turbine: no wake losses
   - Wind farm: 5-15% wake losses typical

4. **Assuming linear scaling** → Power is NOT linear in v
   - P ∝ v³, not P ∝ v

5. **Neglecting altitude effects** → Air density decreases with height
   - 10% lower density → 10% lower power
   - Must use correct ρ for hub height

### 8.6 VSCode + GitHub Copilot Tips

**Using Claude Sonnet in GitHub Copilot Chat:**

1. **Context provision:**
   - Open relevant files in VSCode editor
   - Copilot Chat will see open files as context
   - Reference this handoff document in prompts

2. **Iterative development:**
   - Start with small changes (one function, one section)
   - Test immediately
   - Build up to larger refactors

3. **Asking for code:**
   ```
   Generate a Panel widget to display EPF=1.91 with an info tooltip 
   explaining Rayleigh distribution correction. Follow the style in 
   the existing info_icon() function.
   ```

4. **Asking for documentation:**
   ```
   Write a docstring for the annual_power_density() function that 
   explains what EPF is and cites Ginsberg (2019) pp. 56-59.
   ```

5. **Debugging:**
   ```
   The spacing_efficiency_warning is not appearing when spacing_factor < 6.5 
   and efficiency > 25. Here's the function [paste code]. What's wrong?
   ```

6. **Testing:**
   ```
   Generate a pytest test for the turbine spacing calculation with 
   edge cases: minimum area, maximum diameter, tight spacing.
   ```

7. **For Binder deployment specifically:**
   ```
   I need to deploy a Panel app on Binder. The app currently uses pn.serve().
   What's the current best practice for dual local/Binder deployment?
   Check the Panel documentation at panel.holoviz.org.
   ```

### 8.7 Git Workflow Recommendations

**Branch strategy:**
```bash
# Create feature branch for README update
git checkout -b update-readme-methodology

# Make changes
git add README.md
git commit -m "docs: add Ginsberg worked example and regional adaptation section"

# Push and create PR
git push -u origin update-readme-methodology
```

**Commit message conventions:**
- `docs:` for documentation changes
- `feat:` for new features
- `fix:` for bug fixes
- `test:` for test additions/changes
- `refactor:` for code restructuring
- `deploy:` for deployment configuration changes

**Example commits:**
```bash
git commit -m "docs: add complete methodology section to README"
git commit -m "feat: add EPF display and source attribution banner to Panel app"
git commit -m "docs: create methodology.md explaining v³ relationship"
git commit -m "feat: add spacing-efficiency warning to UI"
git commit -m "test: add Ginsberg worked example validation test"
git commit -m "deploy: add Binder configuration files"
git commit -m "deploy: restructure notebook for dual local/Binder deployment"
```

---

## 9. Quick Start Checklist for VSCode

### Setup (First Time)

- [ ] Clone repository: `git clone https://github.com/mycarta/wind-calculator.git`
- [ ] Open in VSCode: `code wind-calculator`
- [ ] Activate conda env: `conda activate wind-panel-app`
- [ ] Install VSCode extensions:
  - Python (Microsoft)
  - Jupyter (Microsoft)
  - GitHub Copilot (if available)
- [ ] Run tests to verify: `python -m pytest -v`
- [ ] Open `Panel_app_pkg.ipynb` and run all cells

### Priority Tasks (First Session)

- [ ] **Task 1:** Replace README.md with new version from Section 7.1
  - Backup current README: `cp README.md README_old.md`
  - Copy new content from handoff doc
  - Commit: `git commit -m "docs: comprehensive README rewrite with Ginsberg methodology"`

- [ ] **Task 2:** Add source banner to Panel app (Section 7.2)
  - Open `Panel_app_pkg.ipynb`
  - Add `source_banner()` function
  - Update `results_panel()` to include banner
  - Test in browser
  - Commit: `git commit -m "feat: add methodology and data source attribution banner"`

- [ ] **Task 3:** Add EPF display to Panel app (Section 7.2)
  - Add `epf_display()` function
  - Insert into single turbine section
  - Test tooltip works
  - Commit: `git commit -m "feat: add EPF display with Rayleigh distribution explanation"`

- [ ] **Task 4:** Fix Binder deployment (Section 4.4, 5.7)
  - Research current Panel Binder documentation
  - Restructure notebook cells for dual deployment
  - Create/update Binder configuration files
  - Test on mybinder.org
  - Commit: `git commit -m "deploy: enable Binder deployment with dual local/Binder mode"`

- [ ] **Task 5:** Create docs/methodology.md (Section 7.3)
  - Create `docs/` directory if needed: `mkdir -p docs`
  - Create file from template
  - Commit: `git commit -m "docs: add in-depth v³ scaling and EPF explanation"`

### Testing After Changes

- [ ] Run pytest: `python -m pytest -v`
- [ ] Verify Ginsberg test passes: `python -m pytest -v tests/test_wind_calculations.py::test_ginsberg_worked_example`
- [ ] Launch Panel app locally: Run notebook cells
- [ ] Test Binder deployment: Push to GitHub, click Binder badge
- [ ] Manual UI testing:
  - [ ] Select each rotor diameter
  - [ ] Verify source banner displays
  - [ ] Verify EPF=1.91 shown
  - [ ] Check all tooltips work
  - [ ] Test unit conversions
  - [ ] Adjust spacing and efficiency sliders
  - [ ] Check warning appears when appropriate

### Documentation After Changes

- [ ] Update any modified function docstrings
- [ ] Add inline comments for non-obvious code
- [ ] Update CHANGELOG.md if exists (create if not)
- [ ] Consider creating GitHub release notes

---

## 10. Contact and Support

**Repository:** https://github.com/mycarta/wind-calculator

**Issues:** Use GitHub Issues for bugs and feature requests

**This Handoff Document:**
- Created: January 20, 2026
- Updated: January 21, 2026 (added Binder deployment task, minor code quality suggestions)
- Author: Claude (Anthropic)
- Purpose: Transition to VSCode + GitHub Copilot environment
- Version: 1.1

**For Continuity:**
This document contains all necessary information to continue development without access to the original context. If you need clarification on any section, the following are good starting points:

1. **Physics questions:** Section 2 (Core Physics and Methodology)
2. **Code structure:** Section 3 (Current Implementation Details)
3. **What to change:** Section 4 (Required Changes)
4. **How to change it:** Section 5 (File-by-File Action Items)
5. **Ready-to-use code:** Section 7 (Code Snippets and Templates)
6. **Binder deployment:** Section 4.4 and 5.7 (PRIMARY TASK)

**Good luck with the continued development!**

---

*End of Handoff Document*
