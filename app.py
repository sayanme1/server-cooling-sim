import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# --- PAGE SETUP ---
st.set_page_config(page_title="Passive Server Cooling Model", layout="wide", page_icon="⚡")

st.title("⚡ Passive Server Cooling: Loop Thermosyphon Model")
st.caption("A Class 11 & Class 12 Physics Simulation: Convection, Latent Heat, and Joule Heating")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Simulation Controls")
cpu_power = st.sidebar.slider("CPU Heat Power (Watts)", min_value=50, max_value=300, value=180, step=10)
ambient_temp = st.sidebar.slider("Room / Ambient Temp (°C)", min_value=15, max_value=40, value=25, step=1)
fluid = st.sidebar.radio("Working Fluid", ["Novec 7100 (Boils @ 61°C)", "Pure Water (Boils @ 100°C)"])

# Physics Constants
if "Novec" in fluid:
    boil_pt = 61.0      # °C
    latent_heat = 112   # kJ/kg
    thermal_res = 0.16  # °C/W
else:
    boil_pt = 100.0     # °C
    latent_heat = 2260  # kJ/kg
    thermal_res = 0.28  # °C/W

# Calculated Physics Values
cpu_temp = ambient_temp + (cpu_power * thermal_res)
is_boiling = cpu_temp >= boil_pt
bubble_speed = int(np.clip(cpu_power / 30, 2, 10)) if is_boiling else 1

# Top Summary Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU Temperature", f"{cpu_temp:.1f} °C", delta=f"{cpu_temp - ambient_temp:.1f} °C over room")
col2.metric("Boiling Threshold", f"{boil_pt}°C")
col3.metric("Cooling Mechanism", "2-Phase (Boiling)" if is_boiling else "1-Phase (Liquid)")
col4.metric("Pump Electricity", "0 Watts (100% Passive)")

st.divider()

# --- MAIN INTERFACE TABS ---
tab1, tab2, tab3 = st.tabs(["🖼️ Live Visual Model", "📊 Thermal Graph", "📚 Class 11 & 12 Physics Theory"])

# ==================== TAB 1: VISUAL ANIMATION ====================
with tab1:
    st.subheader("🔄 Real-Time Fluid & Heat Flow Animation")
    
    # HTML5 Canvas Script for Fluid Animation
    animation_html = f"""
    <div style="text-align: center; background-color: #0e1117; padding: 15px; border-radius: 10px;">
        <canvas id="coolingCanvas" width="600" height="400" style="border: 2px solid #31333F; border-radius: 8px;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('coolingCanvas');
        const ctx = canvas.getContext('2d');
        
        let bubbleY = 310;
        let dropY = 90;
        const isBoiling = {str(is_boiling).lower()};
        const speed = {bubble_speed};
        const power = {cpu_power};

        function drawLoop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // --- 1. TOP RADIATOR / CONDENSER ---
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(150, 40, 300, 50);
            ctx.fillStyle = '#38bdf8';
            ctx.font = 'bold 14px Arial';
            ctx.fillText('TOP RADIATOR / CONDENSER (Heat Released to Room)', 160, 70);

            // --- 2. BOTTOM EVAPORATOR / CPU ---
            ctx.fillStyle = isBoiling ? '#7f1d1d' : '#334155';
            ctx.fillRect(200, 310, 200, 60);
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 15px Arial';
            ctx.fillText('SERVER CPU (Heat Source: ' + power + 'W)', 210, 345);

            // --- 3. PIPES ---
            ctx.lineWidth = 12;
            
            // Left Pipe (Vapor Line Up)
            ctx.strokeStyle = isBoiling ? '#ef4444' : '#64748b';
            ctx.beginPath();
            ctx.moveTo(200, 310);
            ctx.lineTo(200, 90);
            ctx.stroke();

            // Right Pipe (Liquid Return Down)
            ctx.strokeStyle = '#3b82f6';
            ctx.beginPath();
            ctx.moveTo(400, 90);
            ctx.lineTo(400, 310);
            ctx.stroke();

            // --- 4. ANIMATED PARTICLES ---
            if (isBoiling) {{
                // Rising Red Vapor Bubbles
                ctx.fillStyle = '#fca5a5';
                ctx.beginPath();
                ctx.arc(200, bubbleY, 8, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(200, (bubbleY + 80) % 220 + 90, 6, 0, Math.PI * 2);
                ctx.fill();

                bubbleY -= speed;
                if (bubbleY < 90) bubbleY = 310;
            }}

            // Falling Blue Liquid Drops
            ctx.fillStyle = '#93c5fd';
            ctx.beginPath();
            ctx.arc(400, dropY, 7, 0, Math.PI * 2);
            ctx.fill();

            dropY += speed * 0.8;
            if (dropY > 310) dropY = 90;

            requestAnimationFrame(drawLoop);
        }}
        drawLoop();
    </script>
    """
    components.html(animation_html, height=440)
    
    if is_boiling:
        st.success("🔥 **2-Phase Boiling Mode Active:** Heat energy from the CPU is turning liquid into vapor bubbles. As bubbles rise, they carry heat to the top radiator automatically without needing an electric pump!")
    else:
        st.info("💧 **Single-Phase Liquid Mode:** Temperature is below boiling point. Heat transfers purely through slow liquid expansion.")

# ==================== TAB 2: GRAPH ====================
with tab2:
    st.subheader("📊 CPU Temperature Stabilization Curve")
    
    t = np.linspace(0, 60, 100)
    temp_curve = ambient_temp + (cpu_temp - ambient_temp) * (1 - np.exp(-t / 10))
    
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(t, temp_curve, color="#ef4444", linewidth=3, label="CPU Temperature (°C)")
    ax.axhline(boil_pt, color="#f59e0b", linestyle="--", label=f"Boiling Pt ({boil_pt}°C)")
    ax.axhline(ambient_temp, color="#10b981", linestyle=":", label=f"Room Temp ({ambient_temp}°C)")
    
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_ylim(10, 115)
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.2)
    st.pyplot(fig)

# ==================== TAB 3: VIVA & PHYSICS THEORY ====================
with tab3:
    st.subheader("📖 Physics Syllabus Integration (Class 11 & Class 12)")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### 🔹 Class 11 Physics Concepts")
        st.markdown(f"""
        1. **Latent Heat of Vaporization ($Q = m L_v$):**
           * When the fluid reaches **{boil_pt}°C**, it absorbs a massive amount of hidden thermal energy (**{latent_heat} kJ/kg**) to change phase from liquid to gas without increasing temperature.
        
        2. **Buoyancy & Natural Convection ($F_b = \Delta \\rho \cdot g \cdot V$):**
           * Heating lowers the density of the fluid ($\Delta \\rho$). Low-density vapor naturally rises to the top condenser, while high-density liquid falls back down under gravity.
        
        3. **First Law of Thermodynamics ($\Delta Q = \Delta U + \Delta W$):**
           * Heat input $\Delta Q$ from the CPU increases the fluid's internal energy $\Delta U$ (causing phase change) and performs kinetic work $\Delta W$ moving fluid through the loop.
        """)
        
    with col_b:
        st.markdown("### 🔹 Class 12 Physics Concepts")
        st.markdown(f"""
        1. **Joule Heating ($P = I^2 R$):**
           * Electric current ($I$) passing through tiny silicon transistors in server CPUs encounters internal electrical resistance ($R$), converting electrical power into massive heat waste ($P$).
        
        2. **Semiconductor Thermal Limits:**
           * Transistors in microprocessors lose efficiency or fail permanently if temperatures exceed **85–90°C** due to thermal breakdown of semiconductor junctions.
        
        3. **Closed-Loop Fluid Analogy to Electric Circuits:**
           * The pressure difference ($\Delta P$) driving fluid flow acts like **Voltage ($V$)**, fluid flow rate acts like **Current ($I$)**, and pipe narrowness acts like **Resistance ($R$)**.
        """)
