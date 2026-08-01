import streamlit as st
import numpy as np
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="How Pump-Free Liquid Cooling Works",
    page_icon="🔄",
    layout="wide"
)

# Clean CSS Styling
st.markdown("""
<style>
    .title-box { text-align: center; margin-bottom: 25px; }
    .title-main { font-size: 2.3rem; font-weight: 800; color: #f8fafc; }
    .title-sub { font-size: 1.1rem; color: #38bdf8; margin-top: 5px; }
    
    .why-box { background-color: #1e293b; border-left: 4px solid #38bdf8; padding: 14px 18px; border-radius: 6px; margin-bottom: 15px; }
    .why-title { font-weight: bold; color: #38bdf8; font-size: 0.95rem; margin-bottom: 4px; }
    .why-desc { font-size: 0.9rem; color: #cbd5e1; margin: 0; }
    
    .component-card { background-color: #0f172a; border: 1px solid #334155; padding: 18px; border-radius: 10px; height: 100%; }
    .component-title { font-weight: bold; font-size: 1.1rem; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="title-box">
    <div class="title-main">🔄 The Self-Running Liquid Cooling Loop</div>
    <div class="title-sub">An interactive guide showing how heat naturally circulates liquid without any electric pump</div>
</div>
""", unsafe_allow_html=True)

# --- TOP SUMMARY BAR ---
st.markdown("### 1️⃣ The Live Result")

# CONTROLS IN SIDEBAR WITH "WHY IS THIS HERE?" EXPLANATIONS
st.sidebar.header("🎛️ Interactive Controls")
st.sidebar.markdown("---")

# Slider 1
cpu_watts = st.sidebar.slider("CPU Heat Power (Watts)", 50, 300, 180, 10)
st.sidebar.caption("👉 **Why this slider?** Simulates computer work load. More work = more heat generated ($P = I^2 R$).")
st.sidebar.markdown("---")

# Slider 2
room_temp = st.sidebar.slider("Room Temperature (°C)", 15, 40, 25, 1)
st.sidebar.caption("👉 **Why this slider?** Shows ambient air temperature. The radiator needs room air to be cooler than the CPU to reject heat.")
st.sidebar.markdown("---")

# Choice
liquid = st.sidebar.radio("Cooling Liquid Choice", ["Low-Boiling Liquid (Boils at 61°C)", "Pure Water (Boils at 100°C)"])
st.sidebar.caption("👉 **Why choose liquid?** Demonstrates why engineered fluids are used—low boiling points evaporate faster at safe processor temperatures.")

# Calculate loop state
boil_pt = 61.0 if "61°C" in liquid else 100.0
resistance = 0.16 if "61°C" in liquid else 0.28
cpu_temp = room_temp + (cpu_watts * resistance)
is_loop_running = cpu_temp >= boil_pt
flow_speed = int(np.clip(cpu_watts / 35, 2, 10)) if is_loop_running else 1

# Display key status cards
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Processor Temp", f"{cpu_temp:.1f} °C")
m2.metric("Liquid Boiling Point", f"{boil_pt} °C")
m3.metric("Loop Movement Status", "⚡ Fast Self-Drive Loop" if is_loop_running else "💤 Idle / Heating Up")
m4.metric("Pump Power Consumption", "0 Watts (FREE)")

st.divider()

# --- MAIN INTERACTIVE SECTION ---
st.markdown("### 2️⃣ Watch the Continuous Loop in Action")

col_left, col_right = st.columns([1.2, 0.8])

with col_left:
    # ANIMATED LOOP SCHEMATIC
    loop_html = f"""
    <div style="text-align: center; background-color: #0b0f19; padding: 15px; border-radius: 12px; border: 1px solid #1e293b;">
        <canvas id="loopCanvas" width="560" height="380"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('loopCanvas');
        const ctx = canvas.getContext('2d');
        
        let hotY = 280;
        let coldY = 80;
        const isRunning = {str(is_loop_running).lower()};
        const speed = {flow_speed};
        const watts = {cpu_watts};

        function render() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. TOP RADIATOR
            ctx.fillStyle = '#1e293b';
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 2;
            ctx.fillRect(130, 30, 300, 50);
            ctx.strokeRect(130, 30, 300, 50);
            ctx.fillStyle = '#38bdf8';
            ctx.font = 'bold 13px Arial';
            ctx.fillText('TOP RADIATOR (Rejects Heat to Room)', 160, 60);

            // 2. BOTTOM COLD PLATE & CPU
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(160, 280, 240, 70);
            
            // Copper Block
            ctx.fillStyle = '#d97706';
            ctx.fillRect(190, 290, 180, 25);
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 11px Arial';
            ctx.fillText('COPPER COLD PLATE', 230, 307);
            
            // CPU Chip
            ctx.fillStyle = isRunning ? '#ef4444' : '#64748b';
            ctx.font = 'bold 13px Arial';
            ctx.fillText('HOT SERVER CPU (' + watts + 'W)', 210, 338);

            // 3. PIPES
            ctx.lineWidth = 14;
            
            // Upward Hot Red Pipe
            ctx.strokeStyle = isRunning ? '#dc2626' : '#475569';
            ctx.beginPath();
            ctx.moveTo(190, 290);
            ctx.lineTo(190, 80);
            ctx.stroke();

            // Downward Cool Blue Pipe
            ctx.strokeStyle = '#2563eb';
            ctx.beginPath();
            ctx.moveTo(370, 80);
            ctx.lineTo(370, 290);
            ctx.stroke();

            // Labels on Pipes
            ctx.fillStyle = '#fca5a5';
            ctx.font = '11px Arial';
            ctx.fillText('Hot Vapor Rises ▲', 95, 185);
            
            ctx.fillStyle = '#93c5fd';
            ctx.fillText('▼ Cool Liquid Falls', 385, 185);

            // 4. ANIMATED BUBBLES AND DROPS
            if (isRunning) {{
                // Red rising vapor
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(190, hotY, 6, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.arc(190, (hotY + 70) % 210 + 80, 5, 0, Math.PI * 2);
                ctx.fill();

                hotY -= speed;
                if (hotY < 80) hotY = 280;
            }}

            // Blue falling liquid
            ctx.fillStyle = '#93c5fd';
            ctx.beginPath();
            ctx.arc(370, coldY, 6, 0, Math.PI * 2);
            ctx.fill();

            coldY += speed * 0.8;
            if (coldY > 280) coldY = 80;

            requestAnimationFrame(render);
        }}
        render();
    </script>
    """
    components.html(loop_html, height=410)

with col_right:
    st.markdown("#### ❓ Why does this loop move by itself?")
    
    st.markdown("""
    <div class="why-box">
        <div class="why-title">1. The Heat Creates Gas</div>
        <div class="why-desc">The hot CPU boils the liquid inside the copper plate into vapor. Gas is much lighter (less dense) than liquid.</div>
    </div>
    
    <div class="why-box">
        <div class="why-title">2. Natural Buoyancy Pushes Gas Up</div>
        <div class="why-desc">Just like a helium balloon or bubble in water, light gas naturally rushes UP through the red pipe without needing any pump.</div>
    </div>
    
    <div class="why-box">
        <div class="why-title">3. Radiator Cools Gas Back to Liquid</div>
        <div class="why-desc">At the top radiator, room air cools the gas down, condensing it back into heavy liquid droplets.</div>
    </div>
    
    <div class="why-box">
        <div class="why-title">4. Gravity Pulls Heavy Liquid Down</div>
        <div class="why-desc">Gravity pulls the heavy cool liquid down the blue pipe back to the CPU, pushing more liquid into the copper plate to restart the cycle!</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- SECTION 3: COMPONENT BREAKDOWN ("WHY IS THIS ITEM HERE?") ---
st.markdown("### 3️⃣ Component Guide: Why Is Every Part Necessary?")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="component-card">
        <div class="component-title" style="color: #d97706;">🟨 Copper Cold Plate</div>
        <p><b>Why is it here?</b></p>
        <p>Copper conducts heat faster than almost any metal. It sits directly on top of the silicon processor chip to transfer heat straight into the internal liquid.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="component-card">
        <div class="component-title" style="color: #ef4444;">🟥 Red Pipe (Rising Line)</div>
        <p><b>Why is it red?</b></p>
        <p>It carries low-density hot vapor upwards. It must be vertical so buoyancy can push the light gas bubbles straight up to the radiator.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="component-card">
        <div class="component-title" style="color: #38bdf8;">🟦 Top Radiator</div>
        <p><b>Why is it at the top?</b></p>
        <p>It dumps absorbed heat into the room. It must sit <i>above</i> the CPU so gravity can naturally pull condensed liquid back down.</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="component-card">
        <div class="component-title" style="color: #3b82f6;">🟦 Blue Pipe (Return Line)</div>
        <p><b>Why is it blue?</b></p>
        <p>It carries cooled, dense liquid back down to the CPU. Gravity supplies 100% of the force needed to move this liquid.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- SECTION 4: THE 3 SIMPLE FORMULAS ---
st.markdown("### 4️⃣ Simple Formula Breakdown")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="component-card">
        <h4>⚡ 1. Where Heat Comes From</h4>
        <p><b>Joule Heating:</b> $P = I^2 \cdot R$</p>
        <p>Electric current ($I$) pushed through micro-resistors ($R$) produces heat ($P$). This is why computer chips get hot when working hard.</p>
    </div>
    """, unsafe_allow_math=True, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="component-card">
        <h4>💧 2. How Liquid Soaks Up Heat</h4>
        <p><b>Latent Heat:</b> $Q = m \cdot L_v$</p>
        <p>Liquid absorbs massive energy ($Q$) to turn into gas without getting hotter. This protects the CPU from overheating past safe limits.</p>
    </div>
    """, unsafe_allow_math=True, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="component-card">
        <h4>🎈 3. How the Loop Drives Itself</h4>
        <p><b>Buoyancy Force:</b> $F_b = (\Delta \\rho) \cdot g \cdot V$</p>
        <p>The density difference ($\Delta \\rho$) between light hot gas and heavy cool liquid creates an upward push force ($F_b$). Zero pump needed!</p>
    </div>
    """, unsafe_allow_math=True, unsafe_allow_html=True)
