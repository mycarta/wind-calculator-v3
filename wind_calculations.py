"""
Wind Calculations Module for Offshore Wind Power Assessment

This module implements the Swept Area Method from Ginsberg (2019) "Harness It"
for calculating offshore wind power and energy outputs.

Methodology:
    - Power density uses Energy Pattern Factor (EPF = 1.91) to correct for
      wind speed distribution (Rayleigh/Weibull k=2)
    - Overall conversion efficiency (20-30%) accounts for Betz limit, 
      availability, wake losses, electrical losses, and power curve effects

Data Sources:
    - Air density and wind speed lookup tables: von Krauland et al. (2023)
    - Energy Pattern Factor (EPF = 1.91): Ginsberg (2019)
    - Turbine spacing methodology: von Krauland et al. (2023)

References:
    Ginsberg, M. (2019). Harness It: Renewable Energy Technologies and Project
        Development Models Transforming the Grid. Business Expert Press.
        ISBN: 978-1-63157-931-8
    
    von Krauland, A.-K., et al. (2023). United States offshore wind energy atlas.
        Applied Energy, 345, 121243. 
        https://doi.org/10.1016/j.apenergy.2023.121243

Author: Matteo Niccoli
Updated: January 2026
"""

import numpy as np


# =============================================================================
# Constants
# =============================================================================

HOURS_PER_YEAR = 8760
EPF_RAYLEIGH = 1.91  # Energy Pattern Factor for Rayleigh distribution (Weibull k=2)
BETZ_LIMIT = 0.593   # Theoretical maximum power extraction (59.3%)
DEFAULT_EFFICIENCY = 0.20  # Ginsberg's recommended conservative value


# =============================================================================
# Lookup Tables
# =============================================================================

# Air density (kg/m³) by hub height/rotor diameter (m)
# Source: von Krauland et al. (2023), Northeast Atlantic US offshore data
# Used as proxy for Scotian Shelf (Nova Scotia) conditions
air_density_lookup = {
    100: 1.000,
    150: 0.995,
    200: 0.990,
    250: 0.986
}

# Average wind speed (m/s) by hub height/rotor diameter (m)
# Source: von Krauland et al. (2023), Northeast Atlantic US offshore data
wind_speed_lookup = {
    100: 9.54,
    150: 9.92,
    200: 10.10,
    250: 10.25
}


# =============================================================================
# Core Calculation Functions
# =============================================================================

def annual_power_density(wind_speed: float, air_density: float = 0.990, 
                         energy_pattern_factor: float = EPF_RAYLEIGH) -> np.float64:
    """
    Calculate the EPF-adjusted mean power density of wind.

    Uses Energy Pattern Factor to correct for wind speed distribution.
    For Rayleigh distribution (Weibull k=2), EPF ≈ 1.91.

    Parameters
    ----------
    wind_speed : float
        Mean wind speed in m/s (rounded to 2 decimal places)
    air_density : float, optional
        Air density in kg/m³, default 0.990 (value at 200 m altitude).
        Other typical values:
            - 0 m (sea level): 1.225
            - 100 m: 1.000
            - 150 m: 0.995
            - 250 m: 0.986
    energy_pattern_factor : float, optional
        Default is 1.91, representing a Rayleigh distribution (k=2).
        This corrects for the fact that ⟨v³⟩ ≠ ⟨v⟩³.

    Returns
    -------
    np.float64
        Mean power density in W/m² (rounded to nearest integer)

    Formula
    -------
    P̄ₐ = ½ρ · EPF · v̄³

    Source
    ------
    Ginsberg, M. (2019). Harness It, pp. 56-59.

    Example
    -------
    >>> annual_power_density(4.47, 1.225, 1.91)
    104.0  # Matches Ginsberg worked example (p. 60)
    """
    wind_speed = np.round(wind_speed, 2)
    power_density = 0.5 * air_density * energy_pattern_factor * (wind_speed ** 3)
    return np.rint(power_density)


def swept_area(diameter: float) -> float:
    """
    Calculate the swept area of a wind turbine rotor.
    
    Parameters
    ----------
    diameter : float
        Rotor diameter in meters.
    
    Returns
    -------
    float
        Swept area in square meters (m²).

    Formula
    -------
    A = π(D/2)² = πD²/4

    Example
    -------
    >>> swept_area(50)
    1963.495...  # Matches Ginsberg worked example
    """
    return np.pi * (diameter / 2) ** 2


def power_kw(power_density: float, rotor_diameter: float) -> float:
    """
    Calculate the mean power output in kW.
    
    Multiplies power density by swept area to get total power.

    Parameters
    ----------
    power_density : float
        Mean power density in W/m² (from annual_power_density).
    rotor_diameter : float
        Rotor diameter in meters.

    Returns
    -------
    float
        Mean power output in kW, rounded to nearest integer.

    Formula
    -------
    P̄ = P̄ₐ × A / 1000

    Example
    -------
    >>> power_kw(104, 50)
    204.0  # Matches Ginsberg worked example (104 W/m² × 1963.5 m²)
    """
    area = swept_area(rotor_diameter)
    return np.rint((power_density * area) / 1000)


def annual_energy_output(power_kw_val: float) -> float:
    """
    Calculate the non-derated annual energy output.
    
    Parameters
    ----------
    power_kw_val : float
        Mean power output in kW.
    
    Returns
    -------
    float
        Annual energy output in MWh/year, rounded to nearest integer.

    Formula
    -------
    AEP_nd = P̄ × 8760 / 1000

    Example
    -------
    >>> annual_energy_output(204)
    1787.0  # Matches Ginsberg worked example
    """
    annual_energy_mwh = power_kw_val * HOURS_PER_YEAR / 1000
    return np.rint(annual_energy_mwh)


def derated_annual_energy_output(power_kw: float, efficiency: float = DEFAULT_EFFICIENCY) -> float:
    """
    Calculate the derated annual energy output accounting for all losses.

    Applies overall conversion efficiency to account for:
    - Betz limit & real Cp (~40% of theoretical 59.3%)
    - Availability (~95-97%)
    - Wake losses (~5-15%, depends on spacing)
    - Electrical losses (~2-3%)
    - Power curve effects (cut-in, rated capping, cut-out)

    Parameters
    ----------
    power_kw : float
        Mean power output in kW (from power_kw function).
    efficiency : float, optional
        Overall conversion efficiency (default 0.20 for 20%).
        Ginsberg (2019) recommends 20% for conservative planning.
        Calculator allows 20-30% range.

    Returns
    -------
    float
        Derated annual energy output in MWh/year, rounded to nearest integer.

    Formula
    -------
    AEP_d = η × P̄ × 8760 / 1000

    Source
    ------
    Ginsberg, M. (2019). Harness It, pp. 60-62.

    Example
    -------
    >>> derated_annual_energy_output(204, 0.20)
    357.0  # Matches Ginsberg worked example (1787 × 0.20)
    """
    annual_energy_mwh = power_kw * HOURS_PER_YEAR * efficiency / 1000
    return np.rint(annual_energy_mwh)


def possible_turbine_installations(available_area_km2: float, rotor_diameter_m: float, 
                                    spacing_factor: float) -> int:
    """
    Calculate the number of possible wind turbine installations.

    Uses a square grid layout where center-to-center spacing is
    F × D (spacing factor × rotor diameter).

    Parameters
    ----------
    available_area_km2 : float
        Total available area in square kilometers (km²).
    rotor_diameter_m : float
        Turbine rotor diameter in meters (m).
    spacing_factor : float
        Turbine density factor (user-controlled).
        Typical range: 3-10 for offshore wind farms.
        von Krauland et al. (2023) uses 5.98 as reference.

    Returns
    -------
    int
        Number of possible wind turbine installations (rounded down).

    Formula
    -------
    N = Available_Area / (F × D)²

    Source
    ------
    von Krauland, A.-K., et al. (2023). United States offshore wind energy atlas.
    Supplemental material.

    Example
    -------
    >>> possible_turbine_installations(1, 50, 6)
    11
    # Available Area = 1 km² = 1,000,000 m²
    # Turbine Spacing Density = (6 × 50)² = 90,000 m²
    # Nturb = 1,000,000 / 90,000 = 11.11 → 11 turbines
    """
    available_area_m2 = available_area_km2 * 1_000_000
    spacing_density = (spacing_factor * rotor_diameter_m) ** 2
    nturb = available_area_m2 // spacing_density
    return int(nturb)
