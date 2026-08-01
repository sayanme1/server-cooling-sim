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
# BASIC CONVECTION MODEL
# ============================================================

time = np.linspace(0, 600, 200)


# simplified thermal response
thermal_mass = fluid_volume * 4186

cooling_constant = 0.002


temperature = (
    ambient_temperature
    +
    (fluid_temperature - ambient_temperature)
    *
    np.exp(-cooling_constant * time)
    +
    (
        heat_input /
        thermal_mass
    )
    *
    (1 - np.exp(-cooling_constant*time))
    * 100
)


current_temperature = temperature[-1]


# ============================================================
# LIVE TELEMETRY
# ============================================================

a, b, c = st.columns(3)


with a:
    st.metric(
        "Current Fluid Temperature",
        f"{current_temperature:.2f} °C"
    )


with b:
    st.metric(
        "Heat Input",
        f"{heat_input} W"
    )


with c:
    st.metric(
        "Thermal Mass",
        f"{thermal_mass/1000:.2f} kJ/K"
    )


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
