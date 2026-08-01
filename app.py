import streamlit as st
from styles import load_css

st.set_page_config(
    page_title="Convection-Based Passive Liquid Cooling System",
    page_icon="❄️",
    layout="wide"
)

load_css()

st.title("Convection-Based Passive Liquid Cooling System")
st.caption("Interactive Physics Simulation | Class XI & XII Thermodynamics")

# ---------------- Sidebar ---------------- #

st.sidebar.header("Simulation Controls")

heat_input = st.sidebar.slider(
    "Heat Input (W)",
    20,
    200,
    80
)

ambient = st.sidebar.slider(
    "Ambient Temperature (°C)",
    15,
    45,
    25
)

fluid = st.sidebar.selectbox(
    "Cooling Liquid",
    [
        "Water",
        "Ethanol",
        "Ammonia"
    ]
)

start = st.sidebar.button("Start Simulation")
reset = st.sidebar.button("Reset")

# ---------------- Top Cards ---------------- #

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("CPU Temperature", "35 °C")

with c2:
    st.metric("Cooling Efficiency", "92 %")

with c3:
    st.metric("Heat Transfer", "80 W")

with c4:
    st.metric("System", "READY")

st.divider()

left, right = st.columns([2,1])

# ---------------- Diagram ---------------- #

with left:

    st.subheader("Cooling System")

    st.markdown(
    """
```text
        ┌───────────────┐
        │  CONDENSER ❄️ │
        └──────┬────────┘
               │
        Cool Liquid
               │
               ▼

        ╔══════════════╗
        ║              ║
        ║ Cooling Loop ║
        ║              ║
        ╚══════════════╝

               ▲
        Warm Liquid
               │

        ┌───────────────┐
        │   CPU 🔥      │
        └───────────────┘
