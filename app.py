# ============================================================
# app.py
# Convection-Based Passive Liquid Cooling System
# Combined Part 1A + Part 1B
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Passive Liquid Cooling | Mission Control",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# NASA / TESLA STYLE
# ============================================================

st.markdown(
"""
<style>

.stApp {
    background:
    linear-gradient(
        180deg,
        #05070d,
        #0b1220
    );
    color:white;
}


h1,h2,h3 {
    color:white;
}


.metric-card {

    background:#111827;

    padding:18px;

    border-radius:12px;

    border:1px solid #1e40af;

}


.metric-title {

    color:#94a3b8;

    font-size:14px;

}


.metric-value {

    color:#38bdf8;

    font-size:30px;

    font-weight:bold;

}


.footer {

    text-align:center;

    color:#64748b;

}

</style>
""",
unsafe_allow_html=True
)



# ============================================================
# HEADER
# ============================================================

st.title(
    "🚀 PASSIVE LIQUID COOLING SYSTEM"
)

st.subheader(
    "Convection-Based Thermal Management | Mission Control Dashboard"
)

st.divider()



# ============================================================
# STATUS CARDS
# ============================================================

cards = [

    ("SYSTEM STATUS","ONLINE"),

    ("COOLING MODE","PASSIVE"),

    ("PUMP","NONE"),

    ("MISSION TIME","T+001")

]


columns = st.columns(4)


for col,card in zip(columns,cards):

    with col:

        st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        {card[0]}
        </div>

        <div class="metric-value">
        {card[1]}
        </div>

        </div>
        """,
        unsafe_allow_html=True
        )



# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.title(
    "⚙️ Thermal Parameters"
)


heat_input = st.sidebar.slider(
    "Heat Source Power (W)",
    10,
    500,
    100
)


fluid_temperature = st.sidebar.slider(
    "Initial Fluid Temperature (°C)",
    20,
    90,
    40
)


ambient_temperature = st.sidebar.slider(
    "Ambient Temperature (°C)",
    0,
    50,
    25
)


fluid_volume = st.sidebar.slider(
    "Liquid Volume (L)",
    0.5,
    10.0,
    3.0
)



st.sidebar.divider()


st.sidebar.subheader(
    "🧪 Fluid Properties"
)


fluid_density = st.sidebar.slider(
    "Fluid Density (kg/m³)",
    700,
    1200,
    1000
)


specific_heat = st.sidebar.slider(
    "Specific Heat (J/kgK)",
    1000,
    5000,
    4186
)


thermal_conductivity = st.sidebar.slider(
    "Thermal Conductivity (W/mK)",
    0.05,
    1.0,
    0.60
)


loop_height = st.sidebar.slider(
    "Vertical Loop Height (m)",
    0.1,
    5.0,
    1.0
)


radiator_area = st.sidebar.slider(
    "Radiator Area (m²)",
    0.05,
    5.0,
    1.0
)



# ============================================================
# PHYSICS ENGINE
# ============================================================

gravity = 9.81

thermal_expansion = 0.00021


delta_T = max(
    fluid_temperature -
    ambient_temperature,
    0.1
)



# Buoyancy velocity

buoyancy_velocity = np.sqrt(

    gravity *
    thermal_expansion *
    delta_T *
    loop_height

)



# Reynolds number

kinematic_viscosity = 1e-6


Reynolds = (

    buoyancy_velocity *
    loop_height /
    kinematic_viscosity

)



# Nusselt approximation

if Reynolds < 2300:

    Nusselt = (
        0.54 *
        Reynolds**0.25
    )

else:

    Nusselt = (
        0.15 *
        Reynolds**0.33
    )



# Heat transfer coefficient

h = (

    Nusselt *
    thermal_conductivity /
    loop_height

)



# Cooling capacity

heat_rejection = (

    h *
    radiator_area *
    delta_T

)



# Thermal mass

thermal_mass = (

    fluid_volume *
    fluid_density *
    specific_heat

)



# ============================================================
# SIMULATION
# ============================================================

time = np.linspace(
    0,
    1800,
    300
)


temperature = np.zeros_like(time)


temperature[0] = fluid_temperature



for i in range(1,len(time)):


    heat_loss = (

        heat_rejection *
        (
            temperature[i-1]
            -
            ambient_temperature
        )
        /
        delta_T

    )


    net_power = (

        heat_input -
        heat_loss

    )


    temperature[i] = (

        temperature[i-1]

        +

        (

        net_power /
        thermal_mass

        )

        *

        (

        time[i] -
        time[i-1]

        )

    )



current_temperature = temperature[-1]



# ============================================================
# TELEMETRY
# ============================================================

st.subheader(
    "🛰️ Live Thermal Telemetry"
)


telemetry = st.columns(4)


telemetry[0].metric(
    "Fluid Temperature",
    f"{current_temperature:.2f} °C"
)


telemetry[1].metric(
    "Flow Velocity",
    f"{buoyancy_velocity:.3f} m/s"
)


telemetry[2].metric(
    "Reynolds Number",
    f"{Reynolds:,.0f}"
)


telemetry[3].metric(
    "Heat Rejection",
    f"{heat_rejection:.2f} W"
)



# ============================================================
# GRAPH
# ============================================================

st.subheader(
    "🌡️ Thermal Response Curve"
)


fig,ax = plt.subplots(
    figsize=(10,4)
)


ax.plot(
    time,
    temperature,
    linewidth=2
)


ax.set_xlabel(
    "Time (seconds)"
)


ax.set_ylabel(
    "Temperature (°C)"
)


ax.set_title(
    "Natural Convection Thermal Stabilization"
)


ax.grid(True)


st.pyplot(fig)

# ============================================================
# PART 2 - LIQUID LOOP VISUALIZATION
# ============================================================

st.divider()

st.subheader(
    "💧 Passive Cooling Loop Visualization"
)


fig2, ax2 = plt.subplots(
    figsize=(8,5)
)


# ------------------------------------------------------------
# LOOP GEOMETRY
# ------------------------------------------------------------

loop_x = [
    0.2,
    0.8,
    0.8,
    0.2,
    0.2
]


loop_y = [
    0.2,
    0.2,
    0.8,
    0.8,
    0.2
]


ax2.plot(
    loop_x,
    loop_y,
    linewidth=8
)



# ------------------------------------------------------------
# HEAT SOURCE
# ------------------------------------------------------------

heat_block = Rectangle(
    (0.05,0.4),
    0.12,
    0.25
)


ax2.add_patch(
    heat_block
)


ax2.text(
    0.05,
    0.35,
    "🔥 HOT\nSOURCE",
    fontsize=10
)



# ------------------------------------------------------------
# RADIATOR
# ------------------------------------------------------------

radiator = Rectangle(
    (0.83,0.4),
    0.12,
    0.25
)


ax2.add_patch(
    radiator
)


ax2.text(
    0.78,
    0.35,
    "❄️ RADIATOR",
    fontsize=10
)



# ------------------------------------------------------------
# FLOW ARROW
# ------------------------------------------------------------

arrow = FancyArrowPatch(
    (0.5,0.85),
    (0.75,0.85),
    arrowstyle="->",
    mutation_scale=25
)


ax2.add_patch(
    arrow
)


ax2.text(
    0.35,
    0.92,
    f"Natural Flow: {buoyancy_velocity:.3f} m/s"
)



# ------------------------------------------------------------
# DISPLAY SETTINGS
# ------------------------------------------------------------

ax2.set_xlim(
    0,
    1
)

ax2.set_ylim(
    0,
    1
)


ax2.axis(
    "off"
)


ax2.set_title(
    "Buoyancy Driven Liquid Circulation"
)


st.pyplot(fig2)



# ============================================================
# SYSTEM ARCHITECTURE
# ============================================================

st.subheader(
    "🛰️ System Architecture"
)


architecture = st.columns(3)


architecture[0].info(
"""
🔥 Heat Source

Electronic thermal load
"""
)


architecture[1].info(
"""
💧 Liquid Loop

Buoyancy driven circulation
"""
)


architecture[2].info(
"""
❄️ Heat Dissipation

Natural convection radiator
"""
)



# ============================================================
# FOOTER
# ============================================================

st.markdown(
"""
<div class="footer">

Passive Liquid Cooling Research Platform |
Thermal Simulation Core v1.0

</div>
""",
unsafe_allow_html=True
)
