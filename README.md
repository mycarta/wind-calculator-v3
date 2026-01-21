# Offshore Wind Calculator

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mycarta/wind-calculator-v3/main?urlpath=lab/tree/Panel_app_pkg.ipynb)

An interactive web-based calculator for offshore wind farm planning, implementing **Ginsberg's (2019) Swept Area Method** with regional data for the Northeast Atlantic US as a proxy for Scotian Shelf (Nova Scotia) conditions.

**[▶ Launch Calculator on Binder](https://mybinder.org/v2/gh/mycarta/wind-calculator-v3/main?urlpath=lab/tree/Panel_app_pkg.ipynb)** *(no installation required)*

### How to Run on Binder

1. Click the **Launch Binder** badge above (allow 1-2 minutes for the environment to load)
2. Once JupyterLab opens, you'll see the notebook `Panel_app_pkg.ipynb`
3. From the menu, select **Run → Run All Cells** (or press `Shift+Enter` twice to run Cells 1-2)
4. The interactive calculator will appear below Cell 2
5. Adjust the sliders and dropdowns to explore different scenarios

---

## 1. Overview

This calculator estimates:
- **Single turbine output:** Mean power (kW/MW) and annual energy production (MWh/year)
- **Site-level output:** Total power and energy for a wind farm based on available area and turbine spacing

**Technology Stack:**
- Python 3.12
- Panel (HoloViews/Bokeh-based UI)
- NumPy for calculations

**Design Philosophy:**
- Follows Ginsberg (2019) methodology exactly
- Uses conservative efficiency values (20-30%)
- Emphasizes transparency of assumptions and limitations

---

## 2. Methodology: Ginsberg Swept Area Method

The calculator uses the **Swept Area Method** from Ginsberg (2019) "Harness It."

### Fundamental Power Equation

Wind power available in the swept area:

$$P = \frac{1}{2} \rho A v^3$$

Where:
- $P$ = power (W)
- $\rho$ = air density (kg/m³)
- $A$ = swept area = $\pi D^2 / 4$ (m²)
- $v$ = wind velocity (m/s)

**Critical insight:** Power scales as $v^3$ (cubic). This means:
- 2× wind speed → 8× power
- 10% error in wind speed → ~33% error in power estimate

### Energy Pattern Factor (EPF)

You **cannot** use average wind speed directly in the power equation:

$$\langle P \rangle \neq \frac{1}{2} \rho A \langle v \rangle^3$$

Because $v^3$ is nonlinear (convex), Jensen's inequality tells us $\langle v^3 \rangle > \langle v \rangle^3$.

**Solution:** For a Rayleigh wind distribution (Weibull shape parameter k=2):

$$\text{EPF} = \frac{\langle v^3 \rangle}{\langle v \rangle^3} \approx 1.91$$

Therefore, the correct formula for mean power density is:

$$\bar{P}_a = \frac{1}{2} \rho \cdot \text{EPF} \cdot \bar{v}^3 \quad [\text{W/m}^2]$$

**Source:** Ginsberg (2019), pp. 56-59.

### Overall Conversion Efficiency

Ginsberg's "Overall Conversion Efficiency" of **20%** accounts for ALL losses:

| Loss Factor | Typical Value |
|-------------|---------------|
| Betz limit & real Cp | ~40% of theoretical 59.3% |
| Availability | ~95-97% |
| Wake losses | ~5-15% (depends on spacing) |
| Electrical losses | ~2-3% |
| Power curve effects | Cut-in, rated capping, cut-out |

**Net result:** 0.593 × 0.40 × 0.95 × 0.90 × 0.97 ≈ 0.195 ≈ **20%**

The calculator allows a 20-30% range for flexibility.

---

## 3. Ginsberg Worked Example (Validation)

The implementation is validated against Ginsberg's worked example (pp. 60-62):

**Inputs:**
| Parameter | Value |
|-----------|-------|
| Rotor diameter (D) | 50 m |
| Wind speed (v̄) | 4.47 m/s |
| Air density (ρ) | 1.225 kg/m³ |
| EPF | 1.91 |
| Efficiency (η) | 20% |

**Calculation:**

```
A = π(50)²/4 = 1,963.5 m²

P̄ₐ = 0.5 × 1.225 × 1.91 × (4.47)³ = 104 W/m²

P̄ = 104 × 1,963.5 / 1000 = 204 kW

AEP (non-derated) = 204 × 8,760 / 1000 = 1,787 MWh/year

AEP (derated) = 0.20 × 1,787 = 357 MWh/year
```

**Expected outputs:** 104 W/m², 204 kW, 357 MWh/year ✓

This validation is included as an automated test in the repository.

---

## 4. Regional Application: NE Atlantic US → Scotian Shelf Proxy

The calculator uses offshore wind resource data from **von Krauland et al. (2023)** for the Northeast Atlantic US region as a proxy for Scotian Shelf (Nova Scotia) conditions.

**Why this proxy is appropriate:**
- Similar latitude (40-45°N) in mid-latitude westerlies
- Same weather systems (nor'easters, extratropical cyclones)
- Adjacent geography (Georges Bank straddles US-Canada boundary)
- Comparable oceanography (Gulf Stream influence)
- Best available published offshore wind resource data for the region

**Limitation:** For actual project development, site-specific measurements are essential. This calculator answers "Is this promising enough to investigate further?" — not "Should we invest $2 billion?"

---

## 5. Data Sources and Lookup Tables

### Air Density by Hub Height

| Hub Height (m) | Air Density (kg/m³) |
|----------------|---------------------|
| 100 | 1.000 |
| 150 | 0.995 |
| 200 | 0.990 |
| 250 | 0.986 |

**Source:** von Krauland et al. (2023), Northeast Atlantic US offshore data.

### Wind Speed by Hub Height

| Hub Height (m) | Average Wind Speed (m/s) |
|----------------|--------------------------|
| 100 | 9.54 |
| 150 | 9.92 |
| 200 | 10.10 |
| 250 | 10.25 |

**Source:** von Krauland et al. (2023), Northeast Atlantic US offshore data.

---

## 6. Default Parameters

| Parameter | Value | Explanation |
|-----------|-------|-------------|
| **EPF** | 1.91 (fixed) | Energy Pattern Factor for Rayleigh distribution (Weibull k=2). Converts ⟨v⟩³ to ⟨v³⟩. Not user-configurable. |
| **Efficiency** | 20-30% (user-selectable) | Overall conversion from wind kinetic energy to electrical output. Ginsberg recommends 20% for conservative planning. |
| **Spacing factor** | 3.0-9.0 (user-selectable, no default) | Turbine center-to-center spacing as multiple of rotor diameter. von Krauland et al. (2023) uses 5.98 as reference. User must explicitly choose. |
| **Available area** | 100-1000 km² (user-selectable) | Site area for wind farm planning. |

---

## 7. Calculations and Formulas

### Complete Calculation Chain

```
1. Swept Area
   A = πD²/4

2. Mean Power Density (EPF-adjusted)
   P̄ₐ = ½ρ · EPF · v̄³  [W/m²]

3. Mean Power (single turbine)
   P̄ = P̄ₐ × A / 1000  [kW]

4. Annual Energy (non-derated)
   AEP_nd = P̄ × 8,760 / 1000  [MWh/year]

5. Annual Energy (derated)
   AEP_d = η × AEP_nd  [MWh/year]

6. Turbine Count
   N = Available_Area / (F × D)²

7. Site Totals
   Site_Power = P̄ × N
   Site_Energy = AEP_d × N
```

---

## 8. Assumptions and Limitations

### Assumptions

1. **Rayleigh wind distribution** (Weibull k=2) — EPF = 1.91 assumes this distribution
2. **Square grid turbine layout** — spacing calculated as (F × D)²
3. **Uniform wind resource** — same wind speed applies across entire site
4. **No terrain effects** — offshore environment assumed flat
5. **Hub height equals rotor diameter** — simplifying assumption for lookup tables

### Limitations

1. **Proxy data** — NE Atlantic US data is a proxy for Scotian Shelf; site-specific measurements needed for actual projects
2. **Simplified wake model** — wake losses included in efficiency factor, not modeled dynamically
3. **No power curve modeling** — uses efficiency factor rather than manufacturer power curves
4. **Planning tool only** — not suitable for financial or engineering decisions without additional validation

---

## 9. Running the Calculator

### Prerequisites

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate wind-panel-app
```

### Local Deployment

```bash
# Open the notebook
jupyter notebook Panel_app_pkg.ipynb

# Run all cells — app launches in browser
```

### Binder (Online)

**No installation required!** Click the badge or link below to launch the calculator in your browser:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mycarta/wind-calculator-v3/main?urlpath=/panel/Panel_app_pkg)

The first launch may take 1-2 minutes while Binder builds the environment.

---

## 10. Running Tests

```bash
# Activate environment
conda activate wind-panel-app

# Run all tests
python -m pytest -v

# Run only the Ginsberg validation test
python -m pytest -v tests/test_wind_calculations.py::test_ginsberg_worked_example
```

*Note: Test suite is currently in development. Additional tests for edge cases and property-based testing are planned.*

---

## 11. References

**Ginsberg, M. (2019).** *Harness It: Renewable Energy Technologies and Project Development Models Transforming the Grid.* Business Expert Press. ISBN: 978-1-63157-931-8.

**von Krauland, A.-K., et al. (2023).** United States offshore wind energy atlas: availability, potential, and economic insights based on wind speeds at different altitudes and thresholds and policy-informed exclusions. *Applied Energy*, 345, 121243. https://doi.org/10.1016/j.apenergy.2023.121243

---

## AI/HI Statement

This project was developed collaboratively between a human (Matteo Niccoli) and AI assistants (Claude by Anthropic). The AI assisted with code implementation, documentation, and methodology validation. All scientific claims and calculations have been verified against published sources.

---

**Author:** Matteo Niccoli ([@mycarta](https://github.com/mycarta))

*Last updated: January 2026*
