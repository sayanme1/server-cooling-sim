# app.py
# Convection-Based Passive Liquid Cooling System
# Part 1A - Dashboard Foundation

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Passive Liquid Cooling | Mission Control",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# NASA / TESLA STYLE CSS
# ============================================================

st.markdown(
    """
    <style>

    body {
        background-color: #05070d;
    }

    .stApp {
        background:
        linear-gradient(
            180deg,
            #05070d 0%,
            #0b1220 100%
        );
        color: white;
    }

    h1, h2, h3 {
        color: #ffffff;
        font-family: Arial, Helvetica, sans-serif;
        letter-spacing: 1px;
    }

    .metric-card {
        background:
        linear-gradient(
            145deg,
            #111827,
            #020617
        );
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #1e40af;
        box-shadow:
        0px 0px 15px rgba(0,120,255,0.25);
    }

    .metric-title {
        color: #94a3b8;
        font-size: 14px;
        text-transform: uppercase;
    }

    .metric-value {
        color: #38bdf8;
        font-size: 32px;
        font-weight: bold;
    }

    .status-online {
        color: #22c55e;
        font-weight: bold;
    }

    .footer {
        text-align:center;
        color:#64748b;
        font-size:12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.title("🚀 PASSIVE LIQUID COOLING SYSTEM")
st.subheader(
    "Convection-Based Thermal Management | Mission Control Dashboard"
)

st.divider()


# ============================================================
# SYSTEM STATUS PANEL
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        """
        <div class="metric-card">
        <div class="metric-title">System Status</div>
        <div class="metric-value status-online">
        ONLINE
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        """
        <div class="metric-card">
        <div class="metric-title">Cooling Mode</div>
        <div class="metric-value">
        PASSIVE
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        """
        <div class="metric-card">
        <div class="metric-title">Pump</div>
        <div class="metric-value">
        NONE
        </div>
        </div>
        """,
        unsafe_allow=True
    )


with col4:
    st.markdown(
        """
        <div class="metric-card">
        <div class="metric-title">Mission Time</div>
        <div class="metric-value">
        T+001
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# SIDEBAR PARAMETERS
# ============================================================

st.sidebar.title("⚙️ Thermal Parameters")

heat_input = st.sidebar.slider(
    "Heat Source Power (W)",
    min_value=10,
    max_value=500,
    value=100
)

fluid_temperature = st.sidebar.slider(
    "Initial Fluid Temperature (°C)",
    min_value=20,
    max_value=90,
    value=40
)

ambient_temperature = st.sidebar.slider(
    "Ambient Temperature (°C)",
    min_value=0,
    max_value=50,
    value=25
)

fluid_volume = st.sidebar.slider(
    "Liquid Volume (L)",
    min_value=0.5,
    max_value=10.0,
    value=3.0
)


# ============================================================
# PART 1B - PASSIVE CONVECTION PHYSICS ENGINE
# ============================================================


st.sidebar.divider()
st.sidebar.subheader("🧪 Fluid Properties")


fluid_density = st.sidebar.slider(
    "Fluid Density (kg/m³)",
    min_value=700,
    max_value=1200,
    value=1000
)


specific_heat = st.sidebar.slider(
    "Specific Heat (J/kg·K)",
    min_value=1000,
    max_value=5000,
    value=4186
)


thermal_conductivity = st.sidebar.slider(
    "Fluid Thermal Conductivity (W/mK)",
    min_value=0.05,
    max_value=1.0,
    value=0.60
)


loop_height = st.sidebar.slider(
    "Vertical Loop Height (m)",
    min_value=0.1,
    max_value=5.0,
    value=1.0
)


radiator_area = st.sidebar.slider(
    "Radiator Surface Area (m²)",
    min_value=0.05,
    max_value=5.0,
    value=1.0
)


# ------------------------------------------------------------
# PHYSICAL CONSTANTS
# ------------------------------------------------------------

gravity = 9.81

thermal_expansion = 0.00021


# ------------------------------------------------------------
# TEMPERATURE DIFFERENCE
# ------------------------------------------------------------

delta_T = max(
    fluid_temperature - ambient_temperature,
    0.1
)


# ------------------------------------------------------------
# BUOYANCY FLOW ESTIMATION
# ------------------------------------------------------------

buoyancy_velocity = np.sqrt(
    gravity *
    thermal_expansion *
    delta_T *
    loop_height
)


# ------------------------------------------------------------
# REYNOLDS NUMBER
# ------------------------------------------------------------

characteristic_length = loop_height

kinematic_viscosity = 1e-6


Reynolds = (
    buoyancy_velocity *
    characteristic_length /
    kinematic_viscosity
)


# ------------------------------------------------------------
# NUSSELT APPROXIMATION
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# CONVECTION COEFFICIENT
# ------------------------------------------------------------

h = (
    Nusselt *
    thermal_conductivity /
    characteristic_length
)


# ------------------------------------------------------------
# HEAT REJECTION CAPACITY
# ------------------------------------------------------------

heat_rejection = (
    h *
    radiator_area *
    delta_T
)


# ------------------------------------------------------------
# THERMAL MASS
# ------------------------------------------------------------

thermal_mass = (
    fluid_volume *
    fluid_density *
    specific_heat
)


# ------------------------------------------------------------
# TIME SIMULATION
# ------------------------------------------------------------

time = np.linspace(
    0,
    1800,
    300
)


temperature = np.zeros_like(time)

temperature[0] = fluid_temperature


for i in range(1, len(time)):

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
            time[i]
            -
            time[i-1]
        )
    )


current_temperature = temperature[-1]

# ============================================================
# TEMPERATURE GRAPH
# ============================================================

st.subheader("🌡️ Thermal Response Curve")


fig, ax = plt.subplots(figsize=(10,4))

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
    "Passive Convection Cooling Simulation"
)

ax.grid(True)


st.pyplot(fig)


# ============================================================
# SYSTEM ARCHITECTURE PLACEHOLDER
# ============================================================

st.subheader("🛰️ System Architecture")

architecture = st.columns(3)


with architecture[0]:
    st.info(
        """
        🔥 Heat Source

        Electronic load / thermal generator
        """
    )


with architecture[1]:
    st.info(
        """
        💧 Liquid Loop

        Buoyancy driven circulation
        """
    )


with architecture[2]:
    st.info(
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
