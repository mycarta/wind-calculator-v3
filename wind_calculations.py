"""
Wind Calculations Module for Offshore Wind Power Assessment

This module implements the Swept Area Method from Ginsberg (2019) "Harness It"
for calculating offshore wind power and energy outputs.

Methodology:
    - Power density uses Energy Pattern Factor (EPF = 1.91) to correct for
      wind speed distribution (Rayleigh/Weibull k=2)
    - Overall conversion efficiency (20-30%) is Ginsberg's single lumped derating:
      Betz-limited capture (59.3% ceiling) reduced by electrical conversion losses,
      wind speed/direction variability, and maintenance downtime. Ginsberg
      recommends 20% for conservative planning. (He does NOT provide a
      component-by-component breakdown; see derated_annual_energy_output.)

Data Sources:
    - Air density and wind speed lookup tables: von Krauland et al. (2023)
    - Energy Pattern Factor (EPF = 1.91): Ginsberg (2019)
    - Turbine spacing methodology: von Krauland et al. (2023)

References:
    Ginsberg, M. (2019). Harness It: Renewable Energy Technologies and Project
        Development Models Transforming the Grid. Business Expert Press.
        ISBN: 978-1-63157-931-8
    
    von Krauland, A.-K., Long, Q., Enevoldsen, P., & Jacobson, M. Z. (2023).
        United States offshore wind energy atlas: availability, potential, and
        economic insights based on wind speeds at different altitudes and
        thresholds and policy-informed exclusions.
        Energy Conversion and Management: X, 20, 100410.
        https://doi.org/10.1016/j.ecmx.2023.100410

Author: Matteo Niccoli
Updated: February 2026 (corrected efficiency attribution and von Krauland citation)
"""

import numpy as np


# =============================================================================
# Constants
# =============================================================================

HOURS_PER_YEAR = 8760
EPF_RAYLEIGH = 1.91  # Energy Pattern Factor for Rayleigh distribution (Weibull k=2)
BETZ_LIMIT = 0.593   # Theoretical maximum power extraction (59.3%)
DEFAULT_EFFICIENCY = 0.20  # Ginsberg's recommended conservative value
AIR_DENSITY_100M = 1.21328  # kg/m^3 at 100 m (standard atmosphere); von Krauland (2023) SI S5, ref [95]


# =============================================================================
# Lookup Tables
# =============================================================================

# Air density by hub height/rotor diameter (m), in kg/m^3.
# Source: von Krauland et al. (2023), Supplementary Material Section S5 (ref [95]).
# von Krauland gives the standard-atmosphere air density at 100 m
# (AIR_DENSITY_100M = 1.21328 kg/m^3) and DIMENSIONLESS ratios relative to 100 m for
# higher hub heights. Absolute density = AIR_DENSITY_100M * ratio. Air density here is
# standard-atmosphere by altitude (NOT region-specific).
#
# CORRECTION (Feb 2026): earlier versions stored the RATIOS (1.000, 0.995, 0.990, 0.986)
# and fed them into the power equation directly as rho, underestimating all outputs by
# the factor AIR_DENSITY_100M (~17.6%). Now resolved to absolute densities.
air_density_ratio_lookup = {
    100: 1.0,
    150: 0.995203086,
    200: 0.990414414,
    250: 0.985650468,
}

# Absolute air density (kg/m^3) by hub height (m)
air_density_lookup = {
    height: AIR_DENSITY_100M * ratio
    for height, ratio in air_density_ratio_lookup.items()
}

# Default air density used when none is supplied (200 m hub height)
DEFAULT_AIR_DENSITY = air_density_lookup[200]

# Average wind speed (m/s) by hub height/rotor diameter (m)
# NOTE: specific values pending verification against von Krauland (2023) SI Table S8.
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

def annual_power_density(wind_speed: float, air_density: float = DEFAULT_AIR_DENSITY, 
                         energy_pattern_factor: float = EPF_RAYLEIGH) -> np.float64:
    """
    Calculate the EPF-adjusted mean power density of wind.

    Uses Energy Pattern Factor to correct for wind speed distribution.
    For Rayleigh distribution (Weibull k=2), EPF ~ 1.91.

    Parameters
    ----------
    wind_speed : float
        Mean wind speed in m/s (rounded to 2 decimal places)
    air_density : float, optional
        Air density in kg/m^3, default DEFAULT_AIR_DENSITY (~1.20165 kg/m^3, 200 m hub height).
        Other typical values:
            - 0 m (sea level): 1.225
            - 100 m: 1.21328
            - 150 m: 1.20746
            - 250 m: 1.19587
    energy_pattern_factor : float, optional
        Default is 1.91, representing a Rayleigh distribution (k=2).
        This corrects for the fact that <v^3> != <v>^3.

    Returns
    -------
    np.float64
        Mean power density in W/m^2 (rounded to nearest integer)

    Formula
    -------
    P_bar_A = (1/2)rho * EPF * v_bar^3

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
        Swept area in square meters (m^2).

    Formula
    -------
    A = pi(D/2)^2 = piD^2/4

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
        Mean power density in W/m^2 (from annual_power_density).
    rotor_diameter : float
        Rotor diameter in meters.

    Returns
    -------
    float
        Mean power output in kW, rounded to nearest integer.

    Formula
    -------
    P_bar = P_bar_A x A / 1000

    Example
    -------
    >>> power_kw(104, 50)
    204.0  # Matches Ginsberg worked example (104 W/m^2 x 1963.5 m^2)
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
    AEP_nd = P_bar x 8760 / 1000

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

    Applies Ginsberg's single overall conversion efficiency (a lumped derating).
    Ginsberg caps capture at the Betz limit (59.3%) and notes that real turbines
    deliver roughly 20-30% once electrical conversion losses, changes in wind
    speed and direction, and maintenance downtime are accounted for. He does NOT
    decompose the factor into component sub-efficiencies; 20% is his conservative
    recommended value. (A component-by-component breakdown should not be
    attributed to Ginsberg.)

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
    AEP_d = eta x P_bar x 8760 / 1000

    Source
    ------
    Ginsberg, M. (2019). Harness It, pp. 60-62.

    Example
    -------
    >>> derated_annual_energy_output(204, 0.20)
    357.0  # Matches Ginsberg worked example (1787 x 0.20)
    """
    annual_energy_mwh = power_kw * HOURS_PER_YEAR * efficiency / 1000
    return np.rint(annual_energy_mwh)


def possible_turbine_installations(available_area_km2: float, rotor_diameter_m: float, 
                                    spacing_factor: float) -> int:
    """
    Calculate the number of possible wind turbine installations.

    Uses a square grid layout where center-to-center spacing is
    F x D (spacing factor x rotor diameter).

    Parameters
    ----------
    available_area_km2 : float
        Total available area in square kilometers (km^2).
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
    N = Available_Area / (F x D)^2

    Source
    ------
    von Krauland, A.-K., Long, Q., Enevoldsen, P., & Jacobson, M. Z. (2023).
    United States offshore wind energy atlas. Energy Conversion and Management: X,
    20, 100410. https://doi.org/10.1016/j.ecmx.2023.100410 (Supplemental material.)

    Example
    -------
    >>> possible_turbine_installations(1, 50, 6)
    11
    # Available Area = 1 km^2 = 1,000,000 m^2
    # Turbine Spacing Density = (6 x 50)^2 = 90,000 m^2
    # Nturb = 1,000,000 / 90,000 = 11.11 -> 11 turbines
    """
    available_area_m2 = available_area_km2 * 1_000_000
    spacing_density = (spacing_factor * rotor_diameter_m) ** 2
    nturb = available_area_m2 // spacing_density
    return int(nturb)
