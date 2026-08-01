import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Thermosyphon Cooling Simulation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- OVERRIDE STREAMLIT DEFAULT CSS ---
st.markdown("""
<style>
    /* Nuke standard padding and branding */
    .reportview-container .main .block-container { padding: 2rem 3rem; max-width: 1400px; }
    header, footer, #MainMenu { visibility: hidden; }
    body, .stApp { background-color: #06090e; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    
    /* Typography */
    h1, h2, h3 { color: #f8fafc; font-weight: 600; letter-spacing: -0.5px; }
    .section-title { border-bottom: 1px solid #1e293b; padding-bottom: 8px; margin-top: 40px; margin-bottom: 20px; color: #38bdf8; }
    
    /* Physics Cards */
    .physics-card { background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 24px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .physics-card h4 { color: #60a5fa; margin-top: 0; margin-bottom: 12px; font-size: 1.1rem; }
    .physics-card p { font-size: 0.95rem; line-height: 1.6; color: #cbd5e1; }
</style>
""", unsafe_allow_html=True)

st.title("Passive Thermosyphon Server Cooling Architecture")
st.markdown("A zero-power thermal management simulation utilizing latent heat and natural convection.")

# --- 60 FPS INTERACTIVE JAVASCRIPT ENGINE & UI ---
# We inject a custom web application entirely bypassing Streamlit's slider lag.
custom_sim_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #06090e; color: #f8fafc; }
        .container { display: flex; gap: 24px; padding: 20px; background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; }
        
        /* Controls Panel */
        .controls { flex: 1; display: flex; flex-direction: column; gap: 20px; }
        .control-group { background: #1e293b; padding: 16px; border-radius: 8px; }
        .control-group label { font-size: 0.9rem; font-weight: 600; color: #94a3b8; display: block; margin-bottom: 8px; }
        
        /* Sliders */
        input[type=range] { width: 100%; cursor: pointer; accent-color: #38bdf8; }
        .val-display { float: right; color: #38bdf8; font-weight: bold; }
        
        /* Radio Buttons */
        .radio-group { display: flex; gap: 15px; font-size: 0.9rem; }
        
        /* Metrics Panel */
        .metrics-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .metric-box { background: #1e293b; border-left: 3px solid #38bdf8; padding: 12px; border-radius: 6px; }
        .metric-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; }
        .metric-value { font-size: 1.4rem; font-weight: bold; color: #f8fafc; margin-top: 4px; }
        .metric-status { font-size: 0.8rem; margin-top: 4px; }
        
        /* Canvas */
        .canvas-container { flex: 1.2; background: #0b0f19; border: 1px solid #1e293b; border-radius: 8px; display: flex; justify-content: center; align-items: center; padding: 10px; }
        canvas { max-width: 100%; height: auto; }
    </style>
</head>
<body>

<div class="container">
    <div class="controls">
        <div class="control-group">
            <label>CPU Power Dissipation <span class="val-display" id="pwrVal">180 W</span></label>
            <input type="range" id="powerSlider" min="50" max="300" value="180" step="10">
        </div>
        
        <div class="control-group">
            <label>Ambient Room Temperature <span class="val-display" id="tempVal">25 °C</span></label>
            <input type="range" id="roomTempSlider" min="15" max="40" value="25" step="1">
        </div>
        
        <div class="control-group">
            <label>Working Fluid Selection</label>
            <div class="radio-group">
                <input type="radio" id="f1" name="fluid" value="dielectric" checked>
                <label for="f1">Dielectric Fluid (61°C)</label>
                <input type="radio" id="f2" name="fluid" value="water">
                <label for="f2">Pure Water (100°C)</label>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-box">
                <div class="metric-title">CPU Junction Temp</div>
                <div class="metric-value" id="cpuTempDisplay">--</div>
            </div>
            <div class="metric-box">
                <div class="metric-title">Thermal Gradient (ΔT)</div>
                <div class="metric-value" id="deltaTDisplay">--</div>
            </div>
            <div class="metric-box" style="border-left-color: #ef4444;">
                <div class="metric-title">System Status</div>
                <div class="metric-value" id="statusDisplay" style="font-size: 1.1rem; color: #ef4444;">--</div>
            </div>
            <div class="metric-box" style="border-left-color: #10b981;">
                <div class="metric-title">Pump Energy</div>
                <div class="metric-value" style="color: #10b981;">0 Watts</div>
            </div>
        </div>
    </div>
    
    <div class="canvas-container">
        <canvas id="simCanvas" width="480" height="380"></canvas>
    </div>
</div>

<script>
    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');
    
    // Inputs
    const powerSlider = document.getElementById('powerSlider');
    const roomTempSlider = document.getElementById('roomTempSlider');
    const fluids = document.getElementsByName('fluid');
    
    // Displays
    const pwrVal = document.getElementById('pwrVal');
    const tempVal = document.getElementById('tempVal');
    const cpuTempDisplay = document.getElementById('cpuTempDisplay');
    const deltaTDisplay = document.getElementById('deltaTDisplay');
    const statusDisplay = document.getElementById('statusDisplay');
    
    // Physics Constants
    const THETA_DIELECTRIC = 0.16;
    const THETA_WATER = 0.28;
    const BOIL_DIELECTRIC = 61.0;
    const BOIL_WATER = 100.0;
    
    // Animation State
    let particles = [];
    let isBoiling = false;

    function initParticles() {
        particles = [];
        for(let i=0; i<30; i++) {
            particles.push({
                yHot: Math.random() * 200 + 80,
                yCold: Math.random() * 200 + 80,
                speedOffset: Math.random() * 1.5
            });
        }
    }
    initParticles();

    function getGradient(x, y, w, h, c1, c2, c3) {
        let grad = ctx.createLinearGradient(x, y, x+w, y);
        grad.addColorStop(0, c1);
        grad.addColorStop(0.5, c2);
        grad.addColorStop(1, c3);
        return grad;
    }

    function draw() {
        // 1. Calculate Physics
        let P = parseFloat(powerSlider.value);
        let Tamb = parseFloat(roomTempSlider.value);
        let isWater = document.getElementById('f2').checked;
        
        let Rth = isWater ? THETA_WATER : THETA_DIELECTRIC;
        let BP = isWater ? BOIL_WATER : BOIL_DIELECTRIC;
        
        let Tcpu = Tamb + (P * Rth);
        isBoiling = Tcpu >= BP;
        let baseSpeed = isBoiling ? (P / 40) : 0;
        
        // Update DOM text
        pwrVal.innerText = P + " W";
        tempVal.innerText = Tamb + " °C";
        cpuTempDisplay.innerText = Tcpu.toFixed(1) + " °C";
        deltaTDisplay.innerText = (Tcpu - Tamb).toFixed(1) + " °C";
        
        if(isBoiling) {
            statusDisplay.innerText = "Active Phase Change";
            statusDisplay.style.color = "#10b981"; // Green
        } else {
            statusDisplay.innerText = "Liquid Conduction";
            statusDisplay.style.color = "#f59e0b"; // Yellow
        }

        // 2. Render Canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw Copper Cold Plate (Bottom)
        ctx.fillStyle = getGradient(140, 300, 200, 25, '#78350f', '#d97706', '#78350f');
        ctx.fillRect(140, 300, 200, 25);
        
        // Draw CPU Block
        let cpuColor = isBoiling ? '#dc2626' : '#475569';
        ctx.fillStyle = getGradient(170, 325, 140, 30, '#1e293b', cpuColor, '#1e293b');
        ctx.fillRect(170, 325, 140, 30);
        ctx.fillStyle = '#fff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('PROCESSOR', 240, 345);
        
        // Draw Radiator / Condenser (Top)
        ctx.fillStyle = getGradient(100, 30, 280, 50, '#0f172a', '#334155', '#0f172a');
        ctx.fillRect(100, 30, 280, 50);
        // Radiator Fins
        ctx.fillStyle = '#475569';
        for(let i=110; i<380; i+=15) ctx.fillRect(i, 20, 4, 70);
        ctx.fillStyle = '#fff';
        ctx.fillText('CONDENSER (THERMAL REJECTION)', 240, 95);

        // Draw Pipes (Glass Cylinders)
        // Left Pipe (Vapor)
        ctx.fillStyle = getGradient(160, 80, 30, 220, '#1e293b', isBoiling ? '#7f1d1d' : '#334155', '#1e293b');
        ctx.fillRect(160, 80, 30, 220);
        
        // Right Pipe (Liquid)
        ctx.fillStyle = getGradient(290, 80, 30, 220, '#1e293b', '#1e3a8a', '#1e293b');
        ctx.fillRect(290, 80, 30, 220);

        // Draw Animated Particles
        if(isBoiling) {
            particles.forEach(p => {
                // Hot Vapor Rises
                ctx.fillStyle = 'rgba(252, 165, 165, 0.8)';
                ctx.beginPath();
                ctx.arc(175, p.yHot, 4, 0, Math.PI*2);
                ctx.fill();
                
                p.yHot -= (baseSpeed + p.speedOffset);
                if(p.yHot < 80) p.yHot = 300;

                // Cold Liquid Falls
                ctx.fillStyle = 'rgba(147, 197, 253, 0.9)';
                ctx.beginPath();
                ctx.arc(305, p.yCold, 4, 0, Math.PI*2);
                ctx.fill();
                
                p.yCold += (baseSpeed * 0.8 + p.speedOffset);
                if(p.yCold > 300) p.yCold = 80;
            });
        }
        
        requestAnimationFrame(draw);
    }
    
    // Event Listeners to avoid lag
    powerSlider.addEventListener('input', () => {});
    roomTempSlider.addEventListener('input', () => {});
    fluids.forEach(f => f.addEventListener('change', () => {}));
    
    // Start loop
    draw();
</script>
</body>
</html>
"""
components.html(custom_sim_html, height=450)

# --- PHYSICS EXPLANATIONS (CBSE CLASS 11 & 12 ALIGNED) ---
st.markdown('<h2 class="section-title">Physics & Curriculum Integration</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="physics-card">
        <h4>Class 11: Thermal Properties of Matter</h4>
        <p><b>Latent Heat of Vaporization ($Q = mL_v$):</b><br>
        When the fluid reaches its boiling point, it absorbs massive thermal energy to change state from liquid to gas without increasing in temperature. This isothermal process protects the processor from crossing dangerous thermal limits.</p>
        
        <h4>Class 11: Mechanical Properties of Fluids</h4>
        <p><b>Buoyancy & Archimedes' Principle:</b><br>
        Phase change rapidly expands the fluid, drastically lowering its density ($\\rho_{\\text{vapor}} \\ll \\rho_{\\text{liquid}}$). The denser liquid falls due to gravity, displacing the lighter vapor upwards. This density differential provides the motive force ($F_b$), completely eliminating the need for an electrical water pump.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="physics-card">
        <h4>Class 12: Current Electricity</h4>
        <p><b>Joule Heating ($P = I^2R$):</b><br>
        Processors consist of billions of microscopic transistors. As electrical current ($I$) flows through the silicon lattice, internal electrical resistance ($R$) causes electrical energy to be unavoidably converted into waste heat. This is the root heat source of the server.</p>
        
        <h4>Class 12: Semiconductor Electronics</h4>
        <p><b>Junction Thermal Breakdown:</b><br>
        Intrinsic semiconductor charge carriers increase exponentially with temperature. If the silicon die exceeds $\\sim 95^\\circ\\text{C}$, thermal runaway occurs, breaking the depletion regions of p-n junctions and causing total system failure. The cooling system's sole purpose is to prevent this threshold.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<h2 class="section-title">The Role of Ambient Room Temperature</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="physics-card" style="margin-bottom: 40px;">
    <h4>Newton's Law of Cooling & System Efficacy</h4>
    <p>The entire cooling cycle relies on the top condenser's ability to reject heat into the surrounding server room. The rate of this heat loss ($\\frac{dQ}{dt}$) is governed by Newton's Law of Cooling:</p>
    
    <div style="text-align: center; margin: 15px 0;">
        <code style="font-size: 1.2rem; color: #38bdf8; background: #1e293b; padding: 10px; border-radius: 5px;">
            dQ/dt = -h · A · (T<sub>condenser</sub> - T<sub>ambient room</sub>)
        </code>
    </div>
    
    <p><b>Why Room Temperature (T<sub>ambient</sub>) is Critical:</b><br>
    The driving force of heat rejection is the temperature gradient ($\\Delta T$). If the air conditioner in the server room fails and the room temperature rises, the difference between the hot condenser and the room air shrinks. Consequently, heat rejection slows down, vapor fails to condense, pressure builds up, and the processor temperature spikes.</p>
</div>
""", unsafe_allow_html=True)
