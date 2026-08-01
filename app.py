import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Passive Thermosyphon Server Cooling Model",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL CSS STYLING ---
st.markdown("""
<style>
    .main { background-color: #0b0f19; }
    .block-container { padding-top: 1.8rem; padding-bottom: 3rem; }
    
    .main-title { font-size: 2.1rem; font-weight: 700; color: #f8fafc; letter-spacing: -0.5px; margin-bottom: 4px; }
    .main-subtitle { font-size: 1.0rem; color: #94a3b8; font-weight: 400; margin-bottom: 24px; }
    
    .section-title { font-size: 1.25rem; font-weight: 600; color: #38bdf8; margin-top: 20px; margin-bottom: 12px; border-bottom: 1px solid #1e293b; padding-bottom: 6px; }
    
    .card { background-color: #111827; border: 1px solid #1f2937; border-radius: 8px; padding: 18px; margin-bottom: 16px; }
    .card-accent { background-color: #111827; border-left: 4px solid #3b82f6; border-top: 1px solid #1f2937; border-right: 1px solid #1f2937; border-bottom: 1px solid #1f2937; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
    
    .card-heading { font-size: 1.05rem; font-weight: 600; color: #60a5fa; margin-bottom: 6px; }
    .card-body { font-size: 0.92rem; color: #cbd5e1; line-height: 1.5; margin: 0; }
    
    .math-highlight { font-family: 'Courier New', monospace; background-color: #1e293b; color: #38bdf8; padding: 2px 6px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-title">Passive Thermosyphon Server Cooling System</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">A zero-power heat transfer model demonstrating principles of Thermodynamics, Fluid Dynamics, and Current Electricity.</div>', unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("System Control Parameters")
st.sidebar.markdown("---")

cpu_power = st.sidebar.slider("CPU Power Dissipation (Watts)", min_value=50, max_value=300, value=180, step=10)
st.sidebar.caption("Controls electrical heat generation at the processor junction ($P = I^2 R$).")

st.sidebar.markdown("---")
room_temp = st.sidebar.slider("Ambient Room Temperature (°C)", min_value=15, max_value=40, value=25, step=1)
st.sidebar.caption("Determines the heat sink baseline for condenser thermal rejection.")

st.sidebar.markdown("---")
fluid_selection = st.sidebar.radio("Working Fluid", ["Dielectric Fluid (Boiling Pt: 61°C)", "Pure Water (Boiling Pt: 100°C)"])
st.sidebar.caption("Determines the phase-change temperature threshold and latent heat properties.")

# Fluid Physics Parameters
if "61°C" in fluid_selection:
    boiling_pt = 61.0
    latent_heat_val = 112  # kJ/kg
    thermal_resistance = 0.16  # °C/W
else:
    boiling_pt = 100.0
    latent_heat_val = 2260 # kJ/kg
    thermal_resistance = 0.28  # °C/W

# Calculated State
steady_state_temp = room_temp + (cpu_power * thermal_resistance)
delta_t = steady_state_temp - room_temp
is_boiling = steady_state_temp >= boiling_pt
flow_velocity = int(np.clip(cpu_power / 35, 2, 10)) if is_boiling else 1

# --- TOP METRICS ROW ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Equilibrium CPU Temp", f"{steady_state_temp:.1f} °C")
m2.metric("Thermal Gradient (ΔT)", f"{delta_t:.1f} °C", "Above Room Temp")
m3.metric("Fluid Boiling Point", f"{boiling_pt} °C")
m4.metric("Pump Power Required", "0.0 Watts", "Passive Circulation")

st.divider()

# --- MAIN SECTION 1: SCHEMATIC & THERMAL GRAPH ---
st.markdown('<div class="section-title">1. System Architecture & Thermal Behavior</div>', unsafe_allow_html=True)

col_schematic, col_graph = st.columns([1.1, 0.9])

with col_schematic:
    st.markdown("##### Interactive Loop Diagram")
    canvas_html = f"""
    <div style="text-align: center; background-color: #0d1117; padding: 12px; border-radius: 8px; border: 1px solid #21262d;">
        <canvas id="thermosyphonCanvas" width="540" height="360"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('thermosyphonCanvas');
        const ctx = canvas.getContext('2d');
        
        let vaporY = 270;
        let liquidY = 80;
        const isBoiling = {str(is_boiling).lower()};
        const speed = {flow_velocity};
        const power = {cpu_power};

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Top Condenser / Radiator
            ctx.fillStyle = '#161b22';
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 2;
            ctx.fillRect(120, 30, 300, 50);
            ctx.strokeRect(120, 30, 300, 50);
            ctx.fillStyle = '#38bdf8';
            ctx.font = 'bold 12px Arial';
            ctx.fillText('TOP CONDENSER / RADIATOR', 180, 52);
            ctx.font = '10px Arial';
            ctx.fillText('Rejects heat to ambient air via convection', 170, 68);

            // Bottom Evaporator / Cold Plate
            ctx.fillStyle = '#161b22';
            ctx.fillRect(150, 270, 240, 65);
            
            // Copper Plate
            ctx.fillStyle = '#b45309';
            ctx.fillRect(180, 280, 180, 20);
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 10px Arial';
            ctx.fillText('COPPER COLD PLATE', 220, 294);
            
            // CPU Block
            ctx.fillStyle = isBoiling ? '#dc2626' : '#475569';
            ctx.font = 'bold 12px Arial';
            ctx.fillText('SERVER PROCESSOR (' + power + ' W)', 195, 322);

            // Piping Loop
            ctx.lineWidth = 12;
            
            // Vapor Riser (Red Line)
            ctx.strokeStyle = isBoiling ? '#ef4444' : '#475569';
            ctx.beginPath();
            ctx.moveTo(180, 280);
            ctx.lineTo(180, 80);
            ctx.stroke();

            // Liquid Downcomer (Blue Line)
            ctx.strokeStyle = '#2563eb';
            ctx.beginPath();
            ctx.moveTo(360, 80);
            ctx.lineTo(360, 280);
            ctx.stroke();

            // Pipe Labels
            ctx.fillStyle = '#fca5a5';
            ctx.font = '10px Arial';
            ctx.fillText('Vapor Riser (Low Density)', 80, 175);
            
            ctx.fillStyle = '#93c5fd';
            ctx.fillText('Liquid Downcomer (High Density)', 375, 175);

            // Particle Animation
            if (isBoiling) {{
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(180, vaporY, 5, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(180, (vaporY + 60) % 190 + 80, 4, 0, Math.PI * 2);
                ctx.fill();

                vaporY -= speed;
                if (vaporY < 80) vaporY = 270;
            }}

            ctx.fillStyle = '#93c5fd';
            ctx.beginPath();
            ctx.arc(360, liquidY, 5, 0, Math.PI * 2);
            ctx.fill();

            liquidY += speed * 0.8;
            if (liquidY > 270) liquidY = 80;

            requestAnimationFrame(draw);
        }}
        draw();
    </script>
    """
    components.html(canvas_html, height=385)

with col_graph:
    st.markdown("##### Transient Thermal Response")
    
    t = np.linspace(0, 60, 100)
    temp_curve = room_temp + (steady_state_temp - room_temp) * (1 - np.exp(-t / 10))
    
    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')
    
    ax.plot(t, temp_curve, color="#ef4444", linewidth=2.5, label="CPU Junction Temp (°C)")
    ax.axhline(boiling_pt, color="#f59e0b", linestyle="--", linewidth=1.5, label=f"Fluid Boiling Pt ({boiling_pt}°C)")
    ax.axhline(room_temp, color="#10b981", linestyle=":", linewidth=1.5, label=f"Ambient Room Temp ({room_temp}°C)")
    
    ax.set_xlabel("Time (seconds)", color="#94a3b8", fontsize=9)
    ax.set_ylabel("Temperature (°C)", color="#94a3b8", fontsize=9)
    ax.tick_params(colors='#94a3b8', labelsize=8)
    ax.set_ylim(10, 115)
    ax.legend(loc="lower right", facecolor="#0d1117", edgecolor="#21262d", labelcolor="#e2e8f0", fontsize=8)
    ax.grid(True, color="#21262d", alpha=0.6)
    
    st.pyplot(fig)

st.divider()

# --- MAIN SECTION 2: WHY ROOM TEMPERATURE MATTERS ---
st.markdown('<div class="section-title">2. Physics of Room Temperature (Ambient Thermal Driving Force)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card-accent">
    <div class="card-heading">Why does Ambient Room Temperature directly control CPU cooling efficiency?</div>
    <div class="card-body">
        Heat transfer between the top condenser and the surrounding room is governed by <b>Newton's Law of Cooling</b>:
        <br><br>
        $$\\frac{dQ}{dt} = h \\cdot A \\cdot (T_{\\text{condenser}} - T_{\\text{ambient}})$$
        <br>
        Where $h$ is the heat transfer coefficient, $A$ is the surface area of the radiator, and $(T_{\\text{condenser}} - T_{\\text{ambient}})$ is the temperature gradient ($\Delta T$).
        <br><br>
        <b>Key Takeaways:</b>
        <ul>
            <li><b>The Thermal Sink:</b> The ambient air acts as the ultimate thermal reservoir. Heat naturally flows only from higher temperature to lower temperature (Second Law of Thermodynamics).</li>
            <li><b>Impact of Higher Room Temp:</b> If the room temperature increases, the temperature difference $\Delta T$ decreases. This reduces the rate of heat dissipation ($dQ/dt$) at the condenser.</li>
            <li><b>Condensation Stall:</b> If room temperature rises too close to the fluid boiling point, the vapor cannot condense back into liquid fast enough. The pressure inside the loop stabilizes at a higher temperature, causing the CPU operating temperature to rise.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- MAIN SECTION 3: CLASS 11 & CLASS 12 PHYSICS INTEGRATION ---
st.markdown('<div class="section-title">3. Syllabus Integration: Class 11 and Class 12 Physics</div>', unsafe_allow_html=True)

col_c11, col_c12 = st.columns(2)

with col_c11:
    st.markdown("### Class 11 Physics Concepts")
    
    st.markdown("""
    <div class="card">
        <div class="card-heading">1. Latent Heat of Vaporization ($Q = m L_v$)</div>
        <div class="card-body">
            <b>Topic: Thermal Properties of Matter</b><br>
            When liquid inside the copper cold plate reaches its boiling point, it absorbs energy ($Q$) to break intermolecular bonds and convert into gas without increasing in temperature. This phase change absorbs vast amounts of heat per unit mass ($L_v = 112\\text{ kJ/kg}$ for dielectric fluid vs $2260\\text{ kJ/kg}$ for water).
        </div>
    </div>
    
    <div class="card">
        <div class="card-heading">2. Buoyancy & Natural Convection ($F_b = \Delta \\rho \\cdot g \\cdot V$)</div>
        <div class="card-body">
            <b>Topic: Fluid Mechanics & Heat Transfer</b><br>
            When liquid turns into gas, its volume expands drastically, lowering its density ($\rho_{\\text{vapor}} \\ll \\rho_{\\text{liquid}}$). According to <b>Archimedes' Principle</b>, the buoyant force ($F_b$) pushes the light vapor upward through the riser pipe, driving fluid circulation without an external pump.
        </div>
    </div>

    <div class="card">
        <div class="card-heading">3. First Law of Thermodynamics ($\Delta Q = \Delta U + \Delta W$)</div>
        <div class="card-body">
            <b>Topic: Thermodynamics</b><br>
            Thermal energy input ($\Delta Q$) from the CPU increases the internal energy ($\Delta U$) of the working fluid causing phase change, and performs mechanical work ($\Delta W$) by pushing the fluid mass against gravity through the closed loop.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_c12:
    st.markdown("### Class 12 Physics Concepts")
    
    st.markdown("""
    <div class="card">
        <div class="card-heading">1. Joule's Heating Law ($P = I^2 R$)</div>
        <div class="card-body">
            <b>Topic: Current Electricity</b><br>
            Electric current ($I$) flowing through millions of microscopic semiconductor channels with internal electrical resistance ($R$) converts electrical energy into heat power ($P = I^2 R$). This waste heat is the root source that the cooling system must dissipate.
        </div>
    </div>
    
    <div class="card">
        <div class="card-heading">2. Thermal-Electrical Resistance Analogy</div>
        <div class="card-body">
            <b>Topic: Electrostatics & Ohm's Law Analogy</b><br>
            Heat transfer follows a mathematical formulation identical to Ohm's Law ($I = \\frac{V}{R}$):
            <br>
            $$\\dot{Q} = \\frac{\Delta T}{R_{\\text{thermal}}}$$
            Temperature difference ($\Delta T$) acts as <b>Voltage ($V$)</b>, Heat flow rate ($\dot{Q}$) acts as <b>Current ($I$)</b>, and conduction constraints act as <b>Thermal Resistance ($R_{\\text{thermal}}$)</b>.
        </div>
    </div>

    <div class="card">
        <div class="card-heading">3. Semiconductor Junction Temperature Limits</div>
        <div class="card-body">
            <b>Topic: Semiconductor Electronics</b><br>
            In p-n junctions, excessive heat causes thermal excitation of minority charge carriers, breaking down the junction's depletion region and leading to thermal runaway or silicon degradation above $85^\\circ\\text{C} - 105^\\circ\\text{C}$.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- MAIN SECTION 4: COMPONENT GLOSSARY ---
st.markdown('<div class="section-title">4. System Component Functionality</div>', unsafe_allow_html=True)

g1, g2, g3, g4 = st.columns(4)

with g1:
    st.markdown("""
    <div class="card">
        <div class="card-heading">Copper Cold Plate</div>
        <div class="card-body">High thermal conductivity ($k \\approx 400\\text{ W/m}\\cdot\\text{K}$) metal block that draws heat out of the CPU silicon die via direct thermal conduction.</div>
    </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown("""
    <div class="card">
        <div class="card-heading">Vapor Riser Pipe</div>
        <div class="card-body">Vertical channel that routes low-density, high-energy vapor bubbles upward to the condenser powered purely by buoyancy forces.</div>
    </div>
    """, unsafe_allow_html=True)

with g3:
    st.markdown("""
    <div class="card">
        <div class="card-heading">Top Condenser</div>
        <div class="card-body">Finned heat exchanger positioned above the CPU that transfers heat to room air, forcing vapor to condense back into liquid.</div>
    </div>
    """, unsafe_allow_html=True)

with g4:
    st.markdown("""
    <div class="card">
        <div class="card-heading">Liquid Downcomer</div>
        <div class="card-body">Return pipe that uses gravitational pull ($\mathbf{g}$) on high-density liquid to continuously feed cold fluid back into the evaporator.</div>
    </div>
    """, unsafe_allow_html=True)
