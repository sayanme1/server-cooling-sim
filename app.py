import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE SETUP ---
st.set_page_config(page_title="Passive Server Cooling Simulation", layout="wide")
st.title("⚡ Interactive Passive Server Cooling Simulation")
st.caption("Class 11 Physics Model: Convection, Latent Heat, and Buoyancy-Driven Heat Transfer")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Interactive Controls")
cpu_power = st.sidebar.slider("CPU Heat Load (Watts)", min_value=50, max_value=300, value=150, step=10)
ambient_temp = st.sidebar.slider("Ambient Air Temp (°C)", min_value=15, max_value=40, value=25, step=1)
fluid_type = st.sidebar.selectbox("Working Fluid", ["Novec 7100 (Low Boiling Point)", "Water (High Latent Heat)"])

# Fluid Properties
if "Novec" in fluid_type:
    boiling_point = 61.0  # °C
    latent_heat = 112     # kJ/kg
    thermal_res = 0.18    # °C/W
else:
    boiling_point = 100.0 # °C
    latent_heat = 2260    # kJ/kg
    thermal_res = 0.28    # °C/W

# --- CALCULATIONS ---
steady_state_temp = ambient_temp + (cpu_power * thermal_res)
is_boiling = steady_state_temp >= boiling_point

# --- METRICS DISPLAY ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Est. CPU Temp", f"{steady_state_temp:.1f} °C")
col2.metric("Boiling Point", f"{boiling_point:.1f} °C")
col3.metric("System State", "2-Phase (Boiling)" if is_boiling else "1-Phase (Liquid)")
col4.metric("Pump Power", "0 Watts (Passive)")

st.divider()

# --- VISUALIZATION COLUMNS ---
viz_col1, viz_col2 = st.columns([1, 1])

with viz_col1:
    st.subheader("📊 Thermal Stabilization Over Time")
    
    time_points = np.linspace(0, 60, 100)
    temp_curve = ambient_temp + (steady_state_temp - ambient_temp) * (1 - np.exp(-time_points / 12))
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(time_points, temp_curve, color="#ff4b4b", linewidth=2.5, label="CPU Temp (°C)")
    ax.axhline(boiling_point, color="#31333F", linestyle="--", label=f"Boiling Pt ({boiling_point}°C)")
    ax.axhline(ambient_temp, color="#00d26a", linestyle=":", label=f"Ambient ({ambient_temp}°C)")
    
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_ylim(10, 110)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with viz_col2:
    st.subheader("🔄 Thermosyphon Loop Status")
    
    st.markdown(f"""
    ```text
         ┌──────────────────────────────────────┐
         │     TOP RADIATOR / CONDENSER         │  <-- Heat rejected ({ambient_temp}°C)
         └──────────────────┬───────────────────┘
                            │
            Vapor Rises     │    Liquid Falls
            (Low Density)   │    (Gravity Return)
                            │
         ┌──────────────────┴───────────────────┐
         │     CPU EVAPORATOR BLOCK             │  <-- Heat Input: {cpu_power} W
         └──────────────────────────────────────┘
    ```
    """)
    
    if is_boiling:
        st.success("✅ **Active 2-Phase Mode:** Liquid is actively boiling into vapor at the CPU. Latent heat absorption is keeping the server cool!")
    else:
        st.info("ℹ️ **Sensible Heating Mode:** Temperature is below boiling point. Heat is transferred via liquid expansion.")

st.subheader("💡 Key Physics Takeaways")
st.markdown(f"""
* **Latent Heat:** At {boiling_point}°C, the fluid absorbs **{latent_heat} kJ/kg** of hidden energy during phase change without raising its temperature.
* **Buoyancy-Driven Flow:** Heating liquid lowers its density, causing vapor bubbles to rise naturally to the condenser.
* **Zero Power Consumption:** The circulation speed automatically increases as CPU power ({cpu_power}W) increases!
""")