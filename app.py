import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Pump-Free Liquid Server Cooling",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean modern styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #94a3b8; margin-bottom: 25px; }
    .card { background-color: #1e293b; border-radius: 10px; padding: 20px; border: 1px solid #334155; margin-bottom: 20px; }
    .step-num { background-color: #3b82f6; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; margin-right: 8px; }
    .formula-box { background-color: #0f172a; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 6px; font-family: monospace; color: #38bdf8; margin: 10px 0px; }
</style>
""", unsafe_allow_allowed_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="main-header">⚡ Pump-Free Liquid Server Cooling System</div>', unsafe_allow_allowed_html=True)
st.markdown('<div class="sub-header">A complete visual guide to zero-power server cooling using heat convection & evaporation physics</div>', unsafe_allow_allowed_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🎛️ Live System Controls")
st.sidebar.markdown("Adjust these sliders to see how the cooling loop reacts in real-time:")

cpu_wattage = st.sidebar.slider("CPU Heat Power (Watts)", min_value=50, max_value=300, value=180, step=10)
room_temp = st.sidebar.slider("Room Temperature (°C)", min_value=15, max_value=40, value=25, step=1)
liquid_choice = st.sidebar.radio("Cooling Liquid Used", ["Low-Boiling Fluid (Boils at 61°C)", "Pure Water (Boils at 100°C)"])

# Fluid Properties
if "61°C" in liquid_choice:
    boil_pt = 61.0
    latent_heat = 112  # kJ/kg
    resistance = 0.16
else:
    boil_pt = 100.0
    latent_heat = 2260 # kJ/kg
    resistance = 0.28

# Physics Calculations
cpu_temp = room_temp + (cpu_wattage * resistance)
is_boiling = cpu_temp >= boil_pt
flow_speed = int(np.clip(cpu_wattage / 35, 2, 10)) if is_boiling else 1

# --- TOP STATS ROW ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Current CPU Temp", f"{cpu_temp:.1f} °C", f"{cpu_temp - room_temp:.1f}°C above room")
col_m2.metric("Boiling Temperature", f"{boil_pt}°C")
col_m3.metric("Cooling Mode", "Natural Evaporation" if is_boiling else "Liquid Expansion")
col_m4.metric("Pump Power Used", "0 Watts (100% Passive)")

st.divider()

# --- MAIN TWO-COLUMN LAYOUT ---
col_left, col_right = st.columns([1.1, 0.9])

with col_left:
    st.subheader("🖥️ Interactive System Schematic")
    st.caption("Modeled after server cold-plates with red hot-line and blue cold-return line.")
    
    # HTML5 Canvas Diagram
    canvas_code = f"""
    <div style="text-align: center; background-color: #0f172a; padding: 15px; border-radius: 12px; border: 1px solid #334155;">
        <canvas id="coolingCanvas" width="580" height="380"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('coolingCanvas');
        const ctx = canvas.getContext('2d');
        
        let hotY = 280;
        let coldY = 80;
        const isBoiling = {str(is_boiling).lower()};
        const speed = {flow_speed};
        const watts = {cpu_wattage};

        function drawSchematic() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. TOP HEAT EXCHANGER / RADIATOR
            ctx.fillStyle = '#1e293b';
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 2;
            ctx.fillRect(120, 30, 340, 50);
            ctx.strokeRect(120, 30, 340, 50);
            ctx.fillStyle = '#38bdf8';
            ctx.font = 'bold 13px Arial';
            ctx.fillText('TOP HEAT EXCHANGER / RADIATOR', 180, 50);
            ctx.font = '11px Arial';
            ctx.fillText('Rejects heat out to ambient room air', 200, 68);

            // 2. SERVER CHIP & COLD PLATE (At Bottom)
            // Server Tray
            ctx.fillStyle = '#334155';
            ctx.fillRect(140, 280, 300, 70);
            // Copper Cold Plate (Directly touching CPU)
            ctx.fillStyle = '#b45309'; // Copper color
            ctx.fillRect(200, 290, 180, 25);
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 12px Arial';
            ctx.fillText('COPPER COLD PLATE', 230, 307);
            ctx.font = 'bold 13px Arial';
            ctx.fillStyle = isBoiling ? '#ef4444' : '#f8fafc';
            ctx.fillText('SERVER CPU (Heat: ' + watts + 'W)', 220, 338);

            // 3. PIPING LOOP
            ctx.lineWidth = 14;
            
            // RED LINE (Hot vapor/liquid leaving cold plate)
            ctx.strokeStyle = isBoiling ? '#dc2626' : '#94a3b8';
            ctx.beginPath();
            ctx.moveTo(200, 290);
            ctx.lineTo(200, 80);
            ctx.stroke();

            // BLUE LINE (Cool liquid returning from radiator)
            ctx.strokeStyle = '#2563eb';
            ctx.beginPath();
            ctx.moveTo(380, 80);
            ctx.lineTo(380, 290);
            ctx.stroke();

            // 4. ANIMATED FLOW PARTICLES
            if (isBoiling) {{
                // Rising Hot Bubbles (Red Line)
                ctx.fillStyle = '#fca5a5';
                ctx.beginPath();
                ctx.arc(200, hotY, 7, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(200, (hotY + 70) % 210 + 80, 5, 0, Math.PI * 2);
                ctx.fill();

                hotY -= speed;
                if (hotY < 80) hotY = 280;
            }}

            // Falling Cool Drops (Blue Line)
            ctx.fillStyle = '#93c5fd';
            ctx.beginPath();
            ctx.arc(380, coldY, 6, 0, Math.PI * 2);
            ctx.fill();

            coldY += speed * 0.8;
            if (coldY > 280) coldY = 80;

            requestAnimationFrame(drawSchematic);
        }}
        drawSchematic();
    </script>
    """
    components.html(canvas_code, height=410)

with col_right:
    st.subheader("📊 Live Thermal Graph")
    st.caption("Shows CPU temperature stabilizing safely over time.")
    
    t = np.linspace(0, 60, 100)
    temp_curve = room_temp + (cpu_temp - room_temp) * (1 - np.exp(-t / 10))
    
    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')
    
    ax.plot(t, temp_curve, color="#ef4444", linewidth=3, label="CPU Temperature (°C)")
    ax.axhline(boil_pt, color="#f59e0b", linestyle="--", label=f"Boiling Threshold ({boil_pt}°C)")
    ax.axhline(room_temp, color="#10b981", linestyle=":", label=f"Room Temp ({room_temp}°C)")
    
    ax.set_xlabel("Time (seconds)", color="#94a3b8")
    ax.set_ylabel("Temperature (°C)", color="#94a3b8")
    ax.tick_params(colors='#94a3b8')
    ax.set_ylim(10, 115)
    ax.legend(loc="lower right", facecolor="#0f172a", edgecolor="#334155", labelcolor="white")
    ax.grid(True, alpha=0.15)
    st.pyplot(fig)

st.divider()

# --- SECTION 1: STEP-BY-STEP EXPLANATION (FOR COMPLETE BEGINNERS) ---
st.subheader("🔍 Step-by-Step: How This Cools a Server Without a Pump")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="card">
        <h4><span class="step-num">1</span> Heat Created</h4>
        <p>Electricity passing through the computer processor generates intense heat. A metallic copper <b>Cold Plate</b> sits directly on top of the CPU to collect this heat energy.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h4><span class="step-num">2</span> Liquid Evaporates</h4>
        <p>The liquid inside the cold plate absorbs the CPU's heat and boils into light, low-density vapor. Because gas is lighter than liquid, it naturally rushes upwards through the red pipe.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h4><span class="step-num">3</span> Heat Released</h4>
        <p>The hot vapor reaches the top radiator. Cool air from the room blows over the radiator, removing the heat and turning the gas back into dense liquid droplets.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="card">
        <h4><span class="step-num">4</span> Gravity Return</h4>
        <p>Gravity pulls the heavy cool liquid down through the blue pipe back into the CPU cold plate. The cycle repeats continuously with <b>zero mechanical pumps or electricity</b>.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- SECTION 2: FORMULAS EXPLAINED SIMPLY ---
st.subheader("📐 The Physics Formulas Made Simple")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("""
    <div class="card">
        <h4>1. Heat Generation (Joule Heating)</h4>
        <div class="formula-box">P = I² × R</div>
        <p><b>What it means:</b> Electrical current (<i>I</i>) pushed through micro-transistor resistance (<i>R</i>) generates heat waste (<i>P</i>) in Watts.</p>
    </div>
    """, unsafe_allow_html=True)

with col_f2:
    st.markdown("""
    <div class="card">
        <h4>2. Heat Absorption (Latent Heat)</h4>
        <div class="formula-box">Q = m × Lᵥ</div>
        <p><b>What it means:</b> When liquid boils into gas, it absorbs massive amounts of heat (<i>Q</i>) without rising in temperature during the phase transformation.</p>
    </div>
    """, unsafe_allow_html=True)

with col_f3:
    st.markdown("""
    <div class="card">
        <h4>3. Pump-Free Movement (Buoyancy)</h4>
        <div class="formula-box">F_b = (ρ_liquid - ρ_vapor) × g × V</div>
        <p><b>What it means:</b> Hot gas density (<i>ρ_vapor</i>) is far lower than cool liquid density (<i>ρ_liquid</i>). This density difference creates natural upward push force (<i>F_b</i>).</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- SECTION 3: EXAMINER / VIVA CHEAT SHEET ---
st.subheader("💡 Examiner & Viva Questions (Quick Answers)")

q1, q2 = st.columns(2)

with q1:
    st.markdown("""
    * **Q: Why does this system require NO electric pump?**  
      * *Answer:* Heating changes liquid into gas, making it much lighter than the surrounding liquid. Natural buoyancy pushes gas up, and gravity pulls condensed cool liquid back down automatically.
    
    * **Q: Which Class 11 Physics topic does this demonstrate?**  
      * *Answer:* Thermal Properties of Matter (Latent Heat of Vaporization) and Fluid Dynamics (Natural Convection & Density Differences).
    """)

with q2:
    st.markdown("""
    * **Q: Why is liquid cooling better than a regular computer air fan?**  
      * *Answer:* Liquids can store and move over 1,000 times more heat per volume than air, making liquid cooling vastly more efficient for dense server rooms.
    
    * **Q: Which Class 12 Physics topic applies here?**  
      * *Answer:* Current Electricity & Joule's Heating Law ($P = I^2 R$), which causes processors to heat up in the first place.
    """)
