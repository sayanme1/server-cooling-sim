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

# Advanced Glassmorphism & UI Design CSS Injection
glass_css = """
<style>
    /* Global Background & Typography */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e1b4b 0%, #0f172a 60%, #020617 100%);
        background-attachment: fixed;
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Sleek Glassmorphism Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.025);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
        margin-bottom: 24px;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(59, 130, 246, 0.3);
    }
    
    /* Modern Dashboard Metric Cards */
    .glass-metric {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .glass-metric h4 {
        color: #94a3b8 !important;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .glass-metric h2 {
        color: #f8fafc !important;
        font-size: 1.8rem;
        font-weight: 700;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 600;
    }

    /* Custom Action Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
    }

    /* Customizing Sliders & Selectboxes */
    .stSlider, .stSelectbox {
        padding-top: 10px;
    }
</style>
"""

st.markdown(glass_css, unsafe_allow_html=True)

# Hero Header Card
st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 40px 20px;">
        <span style="font-size: 3rem;">❄️</span>
        <h1 style="margin-top: 10px; margin-bottom: 8px;">Convection-Based Passive Liquid Cooling</h1>
        <p style="color: #94a3b8; font-size: 1.15rem; max-width: 800px; margin: 0 auto;">
            An advanced interactive simulation demonstrating phase change dynamics, buoyancy-driven fluid mechanics, and thermodynamic heat transfer principles.
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Controls Configuration
with st.sidebar:
    st.markdown("### 🎛️ Simulation Parameters")
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>Configure system loads and environment settings.</p>", unsafe_allow_html=True)
    
    server_load = st.slider("Server Heat Load (Watts)", 50, 500, 200, 10)
    ambient_temp = st.slider("Ambient Temperature (°C)", 15, 40, 25, 1)
    fluid_vol = st.selectbox("Working Fluid Type", ["Water (High Latent Heat)", "Ethanol (Low Boiling Point)"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_sim = st.button("🚀 Initialize Thermal Cycle")

# Main Section Layout using st.columns (Fixed error)
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown("""
        <div class="glass-card">
            <h3>📖 CBSE NCERT Physics Foundations</h3>
            <ul style="color: #cbd5e1; line-height: 1.8; padding-left: 20px;">
                <li><b>Thermal Properties of Matter (Class 11):</b> High Latent Heat of Vaporization absorbs immense heat energy quickly during phase transitions without raising internal system temperatures[cite: 1].</li>
                <li><b>Mechanical Properties of Fluids (Class 11):</b> Density variations and buoyant forces govern convective loop circulation (hot vapor rises, condensed cool liquid descends)[cite: 1].</li>
                <li><b>Thermodynamics (Class 11/12):</b> Fundamental laws dictating spontaneous heat dissipation from hot server architecture to cooler ambient surroundings[cite: 1].</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="glass-card">
            <h3>⚙️ Closed-Loop Architecture</h3>
            <p style="color: #cbd5e1; line-height: 1.6; margin-bottom: 14px;">
                The simulation models a continuous zero-power passive loop mechanism:
            </p>
            <ul style="color: #cbd5e1; line-height: 1.7; padding-left: 20px;">
                <li><b>Evaporator Core (Bottom):</b> Direct thermal coupling with high-density server chips to vaporize fluid[cite: 1].</li>
                <li><b>Vapor Channel:</b> Leverages buoyancy for upward vertical momentum[cite: 1].</li>
                <li><b>Condenser Unit (Top):</b> Heat rejection to ambient air causing liquefaction, returning fluid via gravity[cite: 1].</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Live Thermal Analytics Dashboard Section
st.markdown("### 📊 Real-Time Thermal Telemetry & Analytics")

if run_sim:
    dashboard_placeholder = st.empty()
    
    time_steps = 30
    temps = []
    
    base_temp = ambient_temp + (server_load * 0.15)
    
    for i in range(time_steps):
        current_temp = base_temp * (1 + 0.45 * np.exp(-i / 5)) + np.random.normal(0, 0.4)
        temps.append(current_temp)
        
        with dashboard_placeholder.container():
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.markdown(f"""<div class="glass-metric"><h4>Evaporator Temp</h4><h2>{current_temp:.1f} °C</h2></div>""", unsafe_allow_html=True)
            with metric_col2:
                boiling_rate = server_load * 0.04
                st.markdown(f"""<div class="glass-metric"><h4>Vaporization Rate</h4><h2>{boiling_rate:.1f} g/s</h2></div>""", unsafe_allow_html=True)
            with metric_col3:
                efficiency = min(98.5, 82 + (server_load * 0.03))
                st.markdown(f"""<div class="glass-metric"><h4>Thermal Efficiency</h4><h2>{efficiency:.1f}%</h2></div>""", unsafe_allow_html=True)
            
            # Interactive Line Chart Display
            chart_data = pd.DataFrame({"Temperature Curve (°C)": temps})
            st.line_chart(chart_data, color="#3b82f6", height=280)
            time.sleep(0.07)
    
    st.markdown("""
        <div class="glass-card" style="border-color: rgba(34, 197, 94, 0.3); background: rgba(34, 197, 94, 0.03); text-align: center; padding: 20px;">
            <h3 style="color: #4ade80 !important; margin-bottom: 5px;">✅ Steady-State Thermal Equilibrium Achieved</h3>
            <p style="color: #cbd5e1; margin: 0;">The passive cooling cycle successfully stabilized component temperatures within optimal operating limits.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="glass-card" style="text-align: center; border-style: dashed; padding: 40px;">
            <p style="color: #94a3b8; font-size: 1.05rem; margin: 0;">
                Configure your desired thermal load parameters in the sidebar and click <b>'Initialize Thermal Cycle'</b> to run the real-time simulation.
            </p>
        </div>
    """, unsafe_allow_html=True)
