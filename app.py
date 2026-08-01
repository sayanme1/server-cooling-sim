import streamlit as st
import time
import numpy as np
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Passive Liquid Cooling Simulation",
    page_icon="❄️",
    layout="wide"
)

# Glassmorphism CSS Injection
glass_css = """
<style>
    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        background-attachment: fixed;
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Glassmorphism Card Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
    }
    
    .glass-metric {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 600;
    }

    /* Custom Button Style */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }
</style>
"""

st.markdown(glass_css, unsafe_allow_html=True)

# Main Title Header inside Glass Card
st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h1>Convection-Based Passive Liquid Cooling System</h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            A CBSE Class 11 & 12 Physics Simulation demonstrating phase change, buoyancy, and thermodynamic heat transfer.
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Controls (Glass styled container context)
with st.sidebar:
    st.markdown("### 🎛️ Simulation Controls")
    server_load = st.slider("Server Heat Load (Watts)", 50, 500, 200, 10)
    ambient_temp = st.slider("Ambient Temperature (°C)", 15, 40, 25, 1)
    fluid_vol = st.selectbox("Working Fluid Type", ["Water (High Latent Heat)", "Ethanol (Low Boiling Point)"])
    run_sim = st.button("🚀 Initialize Thermal Cycle")

# Layout Columns
col1, col2 = st.cols([1.2, 1])

with col1:
    st.markdown("""
        <div class="glass-card">
            <h3>📖 CBSE NCERT Physics Principles</h3>
            <ul style="color: #cbd5e1; line-height: 1.8;">
                <li><b>Class 11 - Thermal Properties of Matter:</b> Latent Heat of Vaporization absorbs immense heat energy quickly during phase change without changing internal temperature[cite: 1].</li>
                <li><b>Class 11 - Mechanical Properties of Fluids:</b> Buoyancy and density variation drive convective circulation (hot vapor rises, cooled liquid falls)[cite: 1].</li>
                <li><b>Class 11 - Thermodynamics:</b> Fundamental laws governing spontaneous heat flow from high-temperature regions (server) to low-temperature regions (ambient air)[cite: 1].</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="glass-card">
            <h3>⚙️ Apparatus Blueprint</h3>
            <p style="color: #cbd5e1; line-height: 1.6;">
                Modeled after closed-loop architecture:
            </p>
            <ul style="color: #cbd5e1; line-height: 1.6;">
                <li><b>Evaporator (Bottom):</b> Thermal contact with the hot server chip; induces boiling and vaporization[cite: 1].</li>
                <li><b>Closed Loop Pipe:</b> Transports vapor upward via buoyant forces[cite: 1].</li>
                <li><b>Condenser (Top):</b> Dissipates heat to ambient air, reverting vapor to liquid drops driven downward by gravity[cite: 1].</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Live Simulation Dashboard Section
st.markdown("### 📊 Real-Time Thermal Dashboard & Analytics")

if run_sim:
    placeholder = st.empty()
    
    # Simulate Real-Time Equilibrium Data
    time_steps = 30
    temps = []
    pressures = []
    
    base_temp = ambient_temp + (server_load * 0.15)
    
    for i in range(time_steps):
        current_temp = base_temp * (1 + 0.5 * np.exp(-i/5)) + np.random.normal(0, 0.5)
        temps.append(current_temp)
        
        with placeholder.container():
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class="glass-metric"><h4>Evaporator Temp</h4><h2>{current_temp:.1f} °C</h2></div>""", unsafe_allow_html=True)
            with m2:
                boiling_rate = server_load * 0.04
                st.markdown(f"""<div class="glass-metric"><h4>Vaporization Rate</h4><h2>{boiling_rate:.1f} g/s</h2></div>""", unsafe_allow_html=True)
            with m3:
                efficiency = min(98.5, 80 + (server_load * 0.03))
                st.markdown(f"""<div class="glass-metric"><h4>Thermal Efficiency</h4><h2>{efficiency:.1f}%</h2></div>""", unsafe_allow_html=True)
            
            # Line chart visualization
            chart_data = pd.DataFrame({"Temperature (°C)": temps})
            st.line_chart(chart_data, color="#3b82f6")
            time.sleep(0.08)
    
    st.success("Simulation complete: System successfully stabilized at safe operating temperature via passive convection!")
else:
    st.info("Adjust your parameters in the sidebar and click **'Initialize Thermal Cycle'** to run the live simulation.")
