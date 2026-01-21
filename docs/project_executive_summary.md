# Wind Calculator Project: Executive Summary for Future Self

**Last Updated:** January 21, 2026  
**Author:** Matteo Niccoli  
**Repository:** https://github.com/mycarta/wind-calculator

---

## What Is This Project?

An **interactive web-based calculator** for preliminary offshore wind farm assessment, specifically designed for the **Scotian Shelf (Nova Scotia)**. It implements Michael Ginsberg's "Swept Area Method" from his 2019 book *Harness It*.

**The core question it answers:** "Given a site area and turbine size, approximately how much energy could we produce per year?"

This is a **back-of-envelope planning tool**, not a project financing tool.

---

## Why Did I Build This?

1. **No open-source alternative existed** — Most wind assessment tools are proprietary or buried in consulting reports
2. **No Scotian Shelf wind atlas** — Had to use Northeast Atlantic US data as proxy
3. **Wanted transparency** — Show exactly what assumptions go into the numbers
4. **Educational value** — Help myself and others understand the physics (especially the v³ relationship)

---

## What's the Methodology?

### The Physics (Ginsberg's Swept Area Method)

**Core equation:** `P = ½ρAv³`

But you can't just plug in average wind speed—you'd underestimate by ~50% because power depends on v³ and ⟨v³⟩ ≠ ⟨v⟩³.

**Solution:** Energy Pattern Factor (EPF = 1.91 for Rayleigh distribution)

**Mean power density:** `P̄ₐ = ½ρ · EPF · v̄³`

**Overall efficiency:** 20% conservative (accounts for Betz limit, availability, wake losses, electrical losses, power curve effects)

### The Data (von Krauland et al. 2023)

Since no Scotian Shelf offshore wind atlas exists, I use **Northeast Atlantic US data** (Massachusetts to Virginia) as a proxy:
- Similar latitude (40-45°N)
- Same weather systems (nor'easters, westerlies)
- Adjacent geography (Georges Bank straddles the border)

This is documented as a limitation. For real projects, you need 1-3 years of site-specific measurements.

---

## What Files Matter?

### Core Files (Finalized January 2026)

| File | What It Does |
|------|--------------|
| `wind_calculations.py` | All calculation functions with full docstrings |
| `environment.yml` | Conda environment with pinned versions |
| `Panel_app_pkg.ipynb` | Interactive Panel application |

### Documentation Files

| File | What It Does |
|------|--------------|
| `wind_calculator_handoff_updated.md` | Complete technical handoff for continuing development |
| `wind_calculator_blog_handoff_updated.md` | Draft structure for blog post |
| `wind_power_intuition.md` | Deep dive on why P ∝ v³ (the "carrier is the cargo" insight) |

### Key References

| Source | What I Use From It |
|--------|-------------------|
| Ginsberg (2019) *Harness It*, pp. 56-62 | Swept Area Method, EPF = 1.91, 20% efficiency |
| von Krauland et al. (2023) *Applied Energy* | Wind speeds, air density, spacing factor (5.98) |

---

## What Were the Key Decisions?

### 1. EPF as a Constant (1.91)

I use Ginsberg's fixed EPF value rather than calculating from site-specific Weibull parameters. This is appropriate for a planning tool—real projects would derive site-specific values.

### 2. Spacing Factor as User Input

The original had a fixed 5.98 (from von Krauland). I made it a slider (3-10 range) because:
- Spacing dramatically affects turbine count
- Users should see the trade-off
- Different projects have different constraints

### 3. Efficiency Range 20-30%

Ginsberg recommends 20% as conservative. I allow up to 30% for:
- Technology improvements
- Optimistic scenarios
- Sensitivity analysis

### 4. No Default for `spacing_factor` Parameter

The `possible_turbine_installations()` function requires `spacing_factor` as an explicit argument. This is intentional—the user should always consciously choose this value rather than relying on a hidden default.

---

## What's the Current State? (January 2026)

### Working ✅
- `wind_calculations.py` — Complete, tested, documented
- Calculation chain validated against Ginsberg's worked example
- Environment specification with pinned versions

### Needs Work 🔧
- **Panel notebook** — Design complete (in handoff), needs implementation
- **Binder deployment** — Broken (learned Panel in 2020-2021, patterns changed)
- **README** — Needs methodology documentation
- **Tests** — Need to be created (templates in handoff)

### Nice to Have 📋
- Source attribution banner in UI
- Display EPF value in outputs
- Spacing-efficiency coupling warning
- Hub height display

---

## Why Did We Do a "Fresh Start"? (January 2026)

During handoff preparation, discovered **two divergent notebook versions**:

| Version | Status |
|---------|--------|
| `Panel_app_prototype.ipynb` | Early prototype, self-contained, fewer features |
| `Panel_app_pkg.ipynb` | More complete, but missing `wind_calculations.py` in the project folder |

Rather than untangle the confusion, decided to:
1. Extract the best parts from both
2. Create clean, documented `wind_calculations.py`
3. Document everything in comprehensive handoff
4. Start fresh in VSCode with clear instructions

---

## What's the Blog Post About?

**Working title:** "Building an Open-Source Offshore Wind Calculator: From Ginsberg's Method to a Working Tool"

**Focus:** How I adapted a textbook method into a usable open-source tool

**Key sections:**
1. The back-of-envelope problem
2. Ginsberg's Swept Area Method
3. Using NE Atlantic US data as proxy
4. Building the Panel calculator
5. The physics (v³ relationship, EPF)
6. What "efficiency" really means
7. Terminology note (cubic vs. "exponential")
8. Limitations & when to use
9. Try it yourself

**Status:** Detailed outline complete, draft opening written (see `wind_calculator_blog_handoff_updated.md`)

---

## Quick Reference: Key Numbers

| Parameter | Value | Source |
|-----------|-------|--------|
| EPF (Rayleigh) | 1.91 | Ginsberg (2019) |
| Default efficiency | 20% | Ginsberg (2019) |
| Spacing factor | 5.98 | von Krauland (2023) |
| Hours/year | 8,760 | Standard |
| Betz limit | 59.3% | Theoretical maximum |

### Ginsberg Worked Example (Validation Test)

| Parameter | Value |
|-----------|-------|
| Rotor diameter | 50 m |
| Wind speed | 4.47 m/s |
| Air density | 1.225 kg/m³ |
| **Power density** | **104 W/m²** |
| **Mean power** | **204 kW** |
| **AEP (non-derated)** | **1,787 MWh/year** |
| **AEP (20% efficiency)** | **357 MWh/year** |

---

## Reminders for Future Self

### If Binder Is Broken Again
- Panel deployment patterns evolve
- Check https://panel.holoviz.org/how_to/deployment/binder.html
- Key: environment detection (`BINDER_SERVICE_HOST` in `os.environ`)
- Use `.servable()` for Binder, `pn.serve()` for local

### If Calculations Seem Wrong
1. Run the Ginsberg validation test first
2. Check that `EPF_RAYLEIGH = 1.91` is being used
3. Remember: power density is W/m², NOT kW
4. Annual energy = power × 8760 / 1000 (converts kW to MWh)

### If You Want to Add New Turbine Sizes
1. Add to `air_density_lookup` (get value from von Krauland or interpolate)
2. Add to `wind_speed_lookup` (same source)
3. Keys are hub height in meters (= rotor diameter assumption)

### If Someone Asks About Scotian Shelf Data
- No published offshore wind atlas exists as of January 2026
- This calculator uses NE Atlantic US as a **proxy**
- For real projects: need 1-3 years of floating lidar data
- The proxy is for "Is this worth investigating?" not "Should we invest $2B?"

---

## Files to Keep Together

When archiving or moving this project, keep these together:

```
wind-calculator/
├── wind_calculations.py          # Core calculations
├── environment.yml               # Environment spec
├── Panel_app_pkg.ipynb           # Panel app
├── tests/
│   └── test_wind_calculations.py # Tests
├── docs/
│   ├── wind_calculator_handoff_updated.md
│   ├── wind_calculator_blog_handoff_updated.md
│   ├── wind_power_intuition.md
│   ├── Wind_calculations.md      # Formula reference
│   └── this_executive_summary.md # This file
└── references/
    └── Ginsberg.pdf              # Scanned pages 56-62
```

---

## Contact Points

- **GitHub:** https://github.com/mycarta/wind-calculator
- **Blog:** MyCarta (for eventual blog post)
- **Related post:** 52 Things chapter on iterative improvement

---

*This document created January 21, 2026, to help future-self understand what was done and why.*
