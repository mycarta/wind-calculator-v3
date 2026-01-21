"""
Offshore Wind Calculator - Panel App
Standalone version for Binder deployment via panel serve
"""
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="param")

import wind_calculations as wc
import panel as pn

pn.extension(sizing_mode='stretch_width')

def info_icon(text):
    return pn.pane.Markdown(
        f"<span title='{text}' style='cursor:help; color:#1976d2; font-size:18px;'>ℹ️</span>",
        width=20
    )

def calculate_outputs(rotor_diameter, available_area_km2, spacing_factor, efficiency):
    air_density = wc.air_density_lookup[rotor_diameter]
    wind_speed = wc.wind_speed_lookup[rotor_diameter]
    pd = wc.annual_power_density(wind_speed, air_density)
    area = wc.swept_area(rotor_diameter)
    pk = wc.power_kw(pd, rotor_diameter)
    energy_non_derated = wc.annual_energy_output(pk)
    energy_derated = wc.derated_annual_energy_output(pk, efficiency)
    turbines = wc.possible_turbine_installations(available_area_km2, rotor_diameter, spacing_factor)
    spacing_m = rotor_diameter * spacing_factor
    site_power = pk * turbines
    site_energy_non_derated = energy_non_derated * turbines
    site_energy_derated = energy_derated * turbines
    return {
        'air_density': air_density,
        'wind_speed': wind_speed,
        'power_density': pd,
        'swept_area': area,
        'power_kw': pk,
        'energy_non_derated': energy_non_derated,
        'energy_derated': energy_derated,
        'turbines': turbines,
        'turbine_spacing_m': spacing_m,
        'site_power': site_power,
        'site_energy_non_derated': site_energy_non_derated,
        'site_energy_derated': site_energy_derated,
        'efficiency': efficiency
    }

# Panel widgets
rotor_diameter_dropdown = pn.widgets.Select(
    name="Turbine Rotor Diameter (m)",
    options=[100, 150, 200, 250],
    value=100
)
available_area_input = pn.widgets.IntSlider(
    name="Available Area (km²)",
    start=100, end=1000, step=50, value=200
)
spacing_factor_slider = pn.widgets.FloatSlider(
    name="Turbine Density Factor (Spacing Factor)",
    start=3.0, end=9.0, step=0.1, value=6.0, format='0.00'
)
efficiency_input = pn.widgets.IntInput(
    name="Overall Conversion Efficiency (%)",
    start=20, end=30, step=1, value=20
)
power_unit_select = pn.widgets.Select(
    name="Power unit", options=["kW", "MW", "GW"], value="kW"
)
energy_unit_select = pn.widgets.Select(
    name="Energy unit", options=["MWh/year", "GWh/year", "TWh/year"], value="MWh/year"
)

def _scale_power_kw(val_kw, unit):
    factors = {"kW": 1.0, "MW": 1e-3, "GW": 1e-6}
    return val_kw * factors[unit]

def _scale_energy_mwh(val_mwh, unit):
    factors = {"MWh/year": 1.0, "GWh/year": 1e-3, "TWh/year": 1e-6}
    return val_mwh * factors[unit]

def _fmt_number(val, decimals):
    fmt = f",.{decimals}f"
    return format(val, fmt)

source_banner = pn.pane.Markdown(
    "**Methodology:** Ginsberg (2019) Swept Area Method &nbsp;|&nbsp; "
    "**Data:** von Krauland et al. (2023) Northeast Atlantic US",
    styles={'background-color': '#f0f0f0', 'padding': '10px', 'border-radius': '5px', 'margin-bottom': '15px'}
)

@pn.depends(rotor_diameter_dropdown, available_area_input, spacing_factor_slider, efficiency_input, power_unit_select, energy_unit_select)
def results_panel(rotor_diameter, available_area_km2, spacing_factor, efficiency, p_unit, e_unit):
    eff_fraction = efficiency / 100.0
    out = calculate_outputs(rotor_diameter, available_area_km2, spacing_factor, eff_fraction)
    hub_height = rotor_diameter

    widget_row = pn.Row(
        rotor_diameter_dropdown,
        pn.Column(
            pn.Row(pn.pane.Markdown(f"**Hub Height:** {hub_height} m"),
                   info_icon("Hub height assumed equal to rotor diameter for lookup tables")),
            pn.Row(pn.pane.Markdown("<b>Air Density (kg/m³):</b> {:.3f}".format(out['air_density'])),
                   info_icon("Density of air at hub height. Source: von Krauland et al. (2023)")),
            pn.Row(pn.pane.Markdown("<b>Average Wind Speed (m/s):</b> {:.2f}".format(out['wind_speed'])),
                   info_icon("Average wind speed at hub height. Source: von Krauland et al. (2023), Northeast Atlantic US offshore data (proxy for Scotian Shelf)"))
        )
    )

    units_row = pn.Row(power_unit_select, energy_unit_select,
                       info_icon("Select units for power and annual energy outputs"))
    divider = pn.pane.HTML("<hr style='border:1px solid #bbb; margin:20px 0;'>")

    single_power_scaled = _scale_power_kw(out['power_kw'], p_unit)
    single_energy_nd_scaled = _scale_energy_mwh(out['energy_non_derated'], e_unit)
    single_energy_d_scaled = _scale_energy_mwh(out['energy_derated'], e_unit)
    site_power_scaled = _scale_power_kw(out['site_power'], p_unit)
    site_energy_nd_scaled = _scale_energy_mwh(out['site_energy_non_derated'], e_unit)
    site_energy_d_scaled = _scale_energy_mwh(out['site_energy_derated'], e_unit)

    p_decimals = 0 if p_unit == "kW" else 3
    e_decimals = 0 if e_unit.startswith("MWh") else 3

    show_warning = spacing_factor < 6.5 and efficiency > 25
    warning_row = pn.pane.Markdown("")
    if show_warning:
        warning_row = pn.pane.Markdown(
            "⚠️ **Spacing-Efficiency Alert:** Tight spacing (F < 6.5D) increases wake losses. "
            "Consider reducing efficiency to ≤ 25% for more realistic estimates.",
            styles={'color': '#ff8c00', 'padding': '10px', 'border': '1px solid #ff8c00', 'border-radius': '5px', 'margin': '10px 0'}
        )

    single_turbine_row = pn.Column(
        pn.pane.Markdown("## Single Turbine Output"),
        widget_row,
        pn.Row(pn.pane.Markdown("**Energy Pattern Factor (EPF):** 1.91"),
               info_icon("Rayleigh distribution correction: ⟨v³⟩/⟨v⟩³ ≈ 1.91 for Weibull k=2.")),
        units_row,
        pn.Row(efficiency_input,
               info_icon("Overall conversion from wind kinetic energy to electrical output. Ginsberg (2019) recommends 20% for conservative planning.")),
        pn.Row(pn.Column(
            pn.pane.Markdown("### Mean Power & Energy"),
            pn.Row(pn.pane.Markdown(f"**Swept Area:** {out['swept_area']:,.2f} m²"),
                   info_icon("Area swept by the turbine blades: A = πD²/4")),
            pn.Row(pn.pane.Markdown(f"**Mean Power Density (EPF-adjusted):** {out['power_density']:,} W/m²"),
                   info_icon("Mean power per unit rotor area: P̄ₐ = ½ρ × EPF × v̄³")),
            pn.Row(pn.pane.Markdown(f"**Mean Power (EPF-adjusted):** {_fmt_number(single_power_scaled, p_decimals)} {p_unit}"),
                   info_icon("Mean power based on average wind speed and EPF")),
            pn.Row(pn.pane.Markdown(f"**Annual Energy Output (non-derated):** {_fmt_number(single_energy_nd_scaled, e_decimals)} {e_unit}"),
                   info_icon("Total annual energy output without losses")),
            pn.Row(pn.pane.Markdown(f"**Derated Annual Energy Output ({out['efficiency']*100:.0f}% efficiency):** {_fmt_number(single_energy_d_scaled, e_decimals)} {e_unit}"),
                   info_icon("Annual energy output accounting for all conversion losses"))
        ))
    )

    site_row = pn.Column(
        divider,
        pn.pane.Markdown("## Site Output"),
        available_area_input,
        pn.Row(spacing_factor_slider, info_icon("Spacing factor F: center-to-center distance as multiple of rotor diameter.")),
        warning_row,
        pn.Row(pn.Column(
            pn.Row(pn.pane.Markdown(f"**Turbine Density Factor (F):** {spacing_factor:.2f}"),
                   info_icon("User-selected turbine density/spacing factor")),
            pn.Row(pn.pane.Markdown(f"**Turbine Spacing:** {out['turbine_spacing_m']:,.0f} m"),
                   info_icon("Center-to-center spacing = rotor diameter × F")),
            pn.Row(pn.pane.Markdown(f"**Installed Turbines:** {out['turbines']:,}"),
                   info_icon("Number of turbines that fit: N = Area / (F × D)²")),
            pn.Row(pn.pane.Markdown(f"**Total Mean Power (EPF-adjusted):** {_fmt_number(site_power_scaled, p_decimals)} {p_unit}"),
                   info_icon("Total mean power for all turbines on site")),
            pn.Row(pn.pane.Markdown(f"**Total Annual Energy Output (non-derated):** {_fmt_number(site_energy_nd_scaled, e_decimals)} {e_unit}"),
                   info_icon("Total annual energy output for the site without losses")),
            pn.Row(pn.pane.Markdown(f"**Total Derated Annual Energy Output ({out['efficiency']*100:.0f}% efficiency):** {_fmt_number(site_energy_d_scaled, e_decimals)} {e_unit}"),
                   info_icon("Total annual energy output for the site accounting for typical losses"))
        ))
    )

    return pn.Column(source_banner, single_turbine_row, site_row)

# Build the app
app_panel = pn.Column(
    pn.pane.Markdown("# Offshore Wind Calculator"),
    results_panel
)

# Make servable for panel serve
app_panel.servable(title="Offshore Wind Calculator")
