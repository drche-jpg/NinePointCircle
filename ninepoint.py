import streamlit as st
import streamlit.components.v1 as components

# --- PRESENTATION SLIDES (MARKDOWN) ---
st.set_page_config(layout="wide", page_title="Euler Line & Nine-Point Circle")

st.title("The Euler Line, Orthocenter, and Nine-Point Circle")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.header("Slide 1: Triangle Centers")
    st.markdown("""
    * **The Circumcenter (O):** จุดศูนย์กลางวงกลมล้อมรอบ (เกิดจากเส้นแบ่งครึ่งตั้งฉาก)
    * **The Centroid (G):** จุดเซนทรอยด์ หรือจุดศูนย์ถ่วง (เกิดจากเส้นมัธยฐาน)
    * **The Orthocenter (H):** จุดออร์โทเซนเตอร์ (เกิดจากเส้นส่วนสูง)
    """)
    
    st.header("Slide 2: The Euler Line")
    st.markdown("""
    นักคณิตศาสตร์ Leonhard Euler ค้นพบว่าในสามเหลี่ยมใดๆ ที่ไม่ใช่สามเหลี่ยมด้านเท่า **จุด O, G, และ H จะเรียงตัวกันเป็นเส้นตรงเสมอ** เรียกว่า "เส้นออยเลอร์" 
    และระยะห่างจาก H ไป G จะเป็น 2 เท่าของระยะจาก G ไป O เสมอ
    """)

with col2:
    st.header("Slide 3: The Nine-Point Circle")
    st.markdown("""
    วงกลมมหัศจรรย์ที่จะลากผ่านจุด 9 จุดนี้เสมอ:
    1. **จุดกึ่งกลางด้าน** 3 จุด
    2. **จุดโคนเส้นส่วนสูง** 3 จุด
    3. **จุดออยเลอร์** 3 จุด (จุดกึ่งกลางระหว่างจุดยอดกับ H)
    """)
    st.header("Slide 4: Properties of the Circle")
    st.markdown("""
    * **จุดศูนย์กลาง (N):** จะอยู่กึ่งกลางพอดีระหว่างจุด H และจุด O บนเส้นออยเลอร์
    * **รัศมี:** จะมีขนาดเป็น "ครึ่งหนึ่ง" ของรัศมีวงกลมล้อมรอบพอดี
    """)

st.write("---")
st.header("Interactive Demonstration")
st.write("ลองลากจุด A, B, C และทดลองเปิด-ปิดเมนูด้านล่าง เพื่อศึกษาที่มาของจุดต่างๆ บนวงกลมเก้าจุด")

# --- SMOOTH INTERACTIVE HTML/JS WIDGET ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; background-color: white;}
        .controls-container { display: flex; flex-wrap: wrap; gap: 20px; margin: 10px 0 20px 0; justify-content: center; width: 100%; max-width: 850px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;}
        .control-group { display: flex; flex-direction: column; gap: 8px; min-width: 220px;}
        canvas { border: 1px solid #ccc; border-radius: 8px; background-color: #ffffff; cursor: crosshair;}
        .label { cursor: pointer; user-select: none; font-size: 14px; color: #444;}
        h4 { margin: 0 0 8px 0; font-size: 15px; color: #222; border-bottom: 2px solid #ddd; padding-bottom: 4px;}
        input[type="checkbox"] { margin-right: 6px; }
    </style>
</head>
<body>
    <div class="controls-container">
        <div class="control-group">
            <h4>เส้นโครงสร้าง (Lines)</h4>
            <label class="label"><input type="checkbox" id="showAlt" onchange="draw()"> เส้นส่วนสูง (Altitudes -> H)</label>
            <label class="label"><input type="checkbox" id="showMed" onchange="draw()"> เส้นมัธยฐาน (Medians -> G)</label>
            <label class="label"><input type="checkbox" id="showPerp" onchange="draw()"> เส้นแบ่งครึ่งตั้งฉาก (Perp. Bisect -> O)</label>
            <label class="label"><input type="checkbox" id="showEuler" checked onchange="draw()"> เส้นออยเลอร์ (Euler Line)</label>
        </div>
        <div class="control-group">
            <h4>จุดตัด & วงกลมหลัก</h4>
            <label class="label"><input type="checkbox" id="showH" checked onchange="draw()"> จุด H (Orthocenter)</label>
            <label class="label"><input type="checkbox" id="showG" checked onchange="draw()"> จุด G (Centroid)</label>
            <label class="label"><input type="checkbox" id="showCircum" checked onchange="draw()"> วงกลมล้อมรอบ + จุด O</label>
            <label class="label"><input type="checkbox" id="showNineCirc" checked onchange="draw()"> วงกลมเก้าจุด + จุด N</label>
        </div>
        <div class="control-group">
            <h4>องค์ประกอบของ 9 จุด</h4>
            <label class="label"><input type="checkbox" id="showMid" checked onchange="draw()"> 1. จุดกึ่งกลางด้าน (3 จุด)</label>
            <label class="label"><input type="checkbox" id="showFeet" checked onchange="draw()"> 2. จุดโคนเส้นส่วนสูง (3 จุด)</label>
            <label class="label"><input type="checkbox" id="showEulerPts" checked onchange="draw()"> 3. จุดออยเลอร์ (3 จุด)</label>
        </div>
    </div>
    <canvas id="canvas" width="850" height="550"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        let pts = [{x: 425, y: 120, label: 'A'}, {x: 200, y: 450, label: 'B'}, {x: 650, y: 450, label: 'C'}];
        let dragging = null;

        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left; const my = e.clientY - rect.top;
            for (let p of pts) if (Math.hypot(p.x - mx, p.y - my) < 15) { dragging = p; return; }
        });
        canvas.addEventListener('mousemove', (e) => {
            if (!dragging) return;
            const rect = canvas.getBoundingClientRect();
            dragging.x = e.clientX - rect.left; dragging.y = e.clientY - rect.top; draw();
        });
        canvas.addEventListener('mouseup', () => { dragging = null; });
        canvas.addEventListener('mouseleave', () => { dragging = null; });

        function getCircumcenter(A, B, C) {
            let D = 2 * (A.x * (B.y - C.y) + B.x * (C.y - A.y) + C.x * (A.y - B.y));
            if (Math.abs(D) < 0.001) return null;
            let Ux = ((A.x**2 + A.y**2) * (B.y - C.y) + (B.x**2 + B.y**2) * (C.y - A.y) + (C.x**2 + C.y**2) * (A.y - B.y)) / D;
            let Uy = ((A.x**2 + A.y**2) * (C.x - B.x) + (B.x**2 + B.y**2) * (A.x - C.x) + (C.x**2 + C.y**2) * (B.x - A.x)) / D;
            return {x: Ux, y: Uy};
        }

        function getAltitudeFoot(A, B, C) {
            let k = ((C.y - B.y) * (A.x - B.x) - (C.x - B.x) * (A.y - B.y)) / (Math.pow(C.y - B.y, 2) + Math.pow(C.x - B.x, 2));
            return { x: A.x - k * (C.y - B.y), y: A.y + k * (C.x - B.x) };
        }

        function drawPoint(p, color, label, size=5) {
            ctx.beginPath(); ctx.arc(p.x, p.y, size, 0, Math.PI*2);
            ctx.fillStyle = color; ctx.fill(); ctx.strokeStyle = "white"; ctx.lineWidth = 1; ctx.stroke();
            if(label) {
                ctx.fillStyle = "#111"; ctx.font = "13px Arial"; ctx.fillText(label, p.x + 8, p.y - 8);
            }
        }

        function drawLine(p1, p2, color, dash=[]) {
            ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = color; ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const A = pts[0], B = pts[1], C = pts[2];

            const O = getCircumcenter(A, B, C);
            if (!O) return; // Collinear protection
            
            const G = {x: (A.x + B.x + C.x) / 3, y: (A.y + B.y + C.y) / 3};
            const H = {x: 3*G.x - 2*O.x, y: 3*G.y - 2*O.y};
            const N = {x: (O.x + H.x) / 2, y: (O.y + H.y) / 2};
            const R = Math.hypot(O.x - A.x, O.y - A.y);

            // 1. Midpoints
            const M_BC = {x: (B.x + C.x)/2, y: (B.y + C.y)/2};
            const M_AC = {x: (A.x + C.x)/2, y: (A.y + C.y)/2};
            const M_AB = {x: (A.x + B.x)/2, y: (A.y + B.y)/2};

            // 2. Altitude Feet
            const F_A = getAltitudeFoot(A, B, C);
            const F_B = getAltitudeFoot(B, A, C);
            const F_C = getAltitudeFoot(C, A, B);

            // 3. Euler Points
            const E_A = {x: (A.x + H.x)/2, y: (A.y + H.y)/2};
            const E_B = {x: (B.x + H.x)/2, y: (B.y + H.y)/2};
            const E_C = {x: (C.x + H.x)/2, y: (C.y + H.y)/2};

            // --- DRAW STRUCTURAL LINES ---
            if (document.getElementById('showMed').checked) {
                drawLine(A, M_BC, "rgba(0,128,0,0.4)"); drawLine(B, M_AC, "rgba(0,128,0,0.4)"); drawLine(C, M_AB, "rgba(0,128,0,0.4)");
            }
            if (document.getElementById('showAlt').checked) {
                drawLine(A, F_A, "rgba(255,0,0,0.4)"); drawLine(B, F_B, "rgba(255,0,0,0.4)"); drawLine(C, F_C, "rgba(255,0,0,0.4)");
            }
            if (document.getElementById('showPerp').checked) {
                drawLine(M_BC, O, "rgba(0,0,255,0.4)"); drawLine(M_AC, O, "rgba(0,0,255,0.4)"); drawLine(M_AB, O, "rgba(0,0,255,0.4)");
            }

            // --- DRAW TRIANGLE ---
            ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.lineTo(C.x, C.y); ctx.closePath();
            ctx.strokeStyle = "black"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;

            // --- DRAW CIRCLES ---
            if (document.getElementById('showCircum').checked) {
                ctx.beginPath(); ctx.arc(O.x, O.y, R, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(0, 0, 255, 0.4)"; ctx.setLineDash([5, 5]); ctx.stroke(); ctx.setLineDash([]);
            }
            if (document.getElementById('showNineCirc').checked) {
                ctx.beginPath(); ctx.arc(N.x, N.y, R/2, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(128, 0, 128, 0.8)"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;
            }

            // --- DRAW EULER LINE ---
            if (document.getElementById('showEuler').checked) {
                let dx = H.x - O.x, dy = H.y - O.y;
                drawLine({x: O.x - dx, y: O.y - dy}, {x: H.x + dx, y: H.y + dy}, "rgba(255, 165, 0, 0.7)");
            }

            // --- DRAW CENTERS ---
            if (document.getElementById('showCircum').checked) drawPoint(O, "blue", "O");
            if (document.getElementById('showG').checked) drawPoint(G, "green", "G");
            if (document.getElementById('showH').checked) drawPoint(H, "red", "H", 6);
            if (document.getElementById('showNineCirc').checked) drawPoint(N, "purple", "N");

            // --- DRAW THE 9 POINTS ---
            if (document.getElementById('showMid').checked) {
                drawPoint(M_BC, "green", "", 6); drawPoint(M_AC, "green", "", 6); drawPoint(M_AB, "green", "", 6);
            }
            if (document.getElementById('showFeet').checked) {
                drawPoint(F_A, "orange", "", 6); drawPoint(F_B, "orange", "", 6); drawPoint(F_C, "orange", "", 6);
            }
            if (document.getElementById('showEulerPts').checked) {
                // Draw connecting line to show how Euler points are found
                if (document.getElementById('showH').checked) {
                    drawLine(A, H, "rgba(0,0,255,0.2)", [3,3]); drawLine(B, H, "rgba(0,0,255,0.2)", [3,3]); drawLine(C, H, "rgba(0,0,255,0.2)", [3,3]);
                }
                drawPoint(E_A, "blue", "", 6); drawPoint(E_B, "blue", "", 6); drawPoint(E_C, "blue", "", 6);
            }

            // --- DRAW VERTICES ---
            for (let p of pts) {
                ctx.beginPath(); ctx.arc(p.x, p.y, 9, 0, Math.PI*2);
                ctx.fillStyle = dragging === p ? "#ffcc00" : "#333"; ctx.fill();
                ctx.fillStyle = "black"; ctx.font = "bold 16px Arial"; ctx.fillText(p.label, p.x - 6, p.y - 13);
            }
        }
        draw(); // Initial Render
    </script>
</body>
</html>
"""

components.html(html_code, height=800)
