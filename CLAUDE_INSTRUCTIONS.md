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