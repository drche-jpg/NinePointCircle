import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Euler Line & Nine-Point Circle")

st.title("The Euler Line, Orthocenter, and Nine-Point Circle")
st.write("---")

# ... (ส่วนของข้อความ Slide 1-4 เหมือนเดิมครับ) ...

st.write("---")
st.header("Interactive Demonstration")
st.write("ลองลากจุด A, B, C และทดลองเปิด-ปิดเส้นต่างๆ เพื่อดูว่าจุดศูนย์กลางแต่ละจุดเกิดจากอะไร")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .controls-container { display: flex; flex-wrap: wrap; gap: 15px; margin: 10px 0 20px 0; justify-content: center; max-width: 800px; padding: 10px; background: #f0f0f0; border-radius: 8px;}
        .control-group { display: flex; flex-direction: column; gap: 5px; }
        canvas { border: 1px solid #ccc; border-radius: 8px; background-color: #fafafa; cursor: crosshair;}
        .label { cursor: pointer; user-select: none; font-size: 14px;}
        h4 { margin: 0 0 5px 0; font-size: 15px; color: #333; }
    </style>
</head>
<body>
    <div class="controls-container">
        <div class="control-group">
            <h4>เส้น (Lines)</h4>
            <label class="label"><input type="checkbox" id="showAlt" onchange="draw()"> เส้นส่วนสูง (Altitudes -> H)</label>
            <label class="label"><input type="checkbox" id="showMed" onchange="draw()"> เส้นมัธยฐาน (Medians -> G)</label>
            <label class="label"><input type="checkbox" id="showPerp" onchange="draw()"> เส้นแบ่งครึ่งตั้งฉาก (Perp. Bisectors -> O)</label>
            <label class="label"><input type="checkbox" id="showEuler" checked onchange="draw()"> เส้นออยเลอร์ (Euler Line)</label>
        </div>
        <div class="control-group">
            <h4>จุดตัด (Centers)</h4>
            <label class="label"><input type="checkbox" id="showH" checked onchange="draw()"> จุด H (Orthocenter)</label>
            <label class="label"><input type="checkbox" id="showG" checked onchange="draw()"> จุด G (Centroid)</label>
            <label class="label"><input type="checkbox" id="showO" checked onchange="draw()"> จุด O (Circumcenter)</label>
            <label class="label"><input type="checkbox" id="showN" checked onchange="draw()"> จุด N (9-Point Center)</label>
        </div>
        <div class="control-group">
            <h4>วงกลม (Circles)</h4>
            <label class="label"><input type="checkbox" id="showCircum" checked onchange="draw()"> วงกลมล้อมรอบ (Circumcircle)</label>
            <label class="label"><input type="checkbox" id="showNine" checked onchange="draw()"> วงกลมเก้าจุด (Nine-Point Circle)</label>
        </div>
    </div>
    <canvas id="canvas" width="800" height="500"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        let pts = [{x: 400, y: 100, label: 'A'}, {x: 200, y: 400, label: 'B'}, {x: 600, y: 400, label: 'C'}];
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

        function drawLine(p1, p2, color, dash=[]) {
            ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = color; ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
        }

        function drawPoint(p, color, label) {
            ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, Math.PI*2);
            ctx.fillStyle = color; ctx.fill();
            ctx.fillStyle = "black"; ctx.font = "14px Arial"; ctx.fillText(label, p.x + 8, p.y - 8);
        }

        function getAltitudeFoot(A, B, C) {
            let k = ((C.y - B.y) * (A.x - B.x) - (C.x - B.x) * (A.y - B.y)) / (Math.pow(C.y - B.y, 2) + Math.pow(C.x - B.x, 2));
            return { x: A.x - k * (C.y - B.y), y: A.y + k * (C.x - B.x) };
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const A = pts[0], B = pts[1], C = pts[2];

            const O = getCircumcenter(A, B, C);
            if (!O) return;
            
            const G = {x: (A.x + B.x + C.x) / 3, y: (A.y + B.y + C.y) / 3};
            const H = {x: 3*G.x - 2*O.x, y: 3*G.y - 2*O.y};
            const N = {x: (O.x + H.x) / 2, y: (O.y + H.y) / 2};
            
            const M_BC = {x: (B.x + C.x)/2, y: (B.y + C.y)/2};
            const M_AC = {x: (A.x + C.x)/2, y: (A.y + C.y)/2};
            const M_AB = {x: (A.x + B.x)/2, y: (A.y + B.y)/2};

            const R = Math.hypot(O.x - A.x, O.y - A.y);

            // Lines
            if (document.getElementById('showMed').checked) {
                drawLine(A, M_BC, "rgba(0,128,0,0.5)"); drawLine(B, M_AC, "rgba(0,128,0,0.5)"); drawLine(C, M_AB, "rgba(0,128,0,0.5)");
            }
            if (document.getElementById('showAlt').checked) {
                drawLine(A, getAltitudeFoot(A, B, C), "rgba(255,0,0,0.5)"); 
                drawLine(B, getAltitudeFoot(B, A, C), "rgba(255,0,0,0.5)"); 
                drawLine(C, getAltitudeFoot(C, A, B), "rgba(255,0,0,0.5)");
            }
            if (document.getElementById('showPerp').checked) {
                drawLine(M_BC, O, "rgba(0,0,255,0.5)"); drawLine(M_AC, O, "rgba(0,0,255,0.5)"); drawLine(M_AB, O, "rgba(0,0,255,0.5)");
            }

            // Triangle
            ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.lineTo(C.x, C.y); ctx.closePath();
            ctx.strokeStyle = "black"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;

            // Circles
            if (document.getElementById('showCircum').checked) {
                ctx.beginPath(); ctx.arc(O.x, O.y, R, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(0, 0, 255, 0.4)"; ctx.setLineDash([5, 5]); ctx.stroke(); ctx.setLineDash([]);
            }
            if (document.getElementById('showNine').checked) {
                ctx.beginPath(); ctx.arc(N.x, N.y, R/2, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(128, 0, 128, 0.8)"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;
            }

            // Euler Line
            if (document.getElementById('showEuler').checked) {
                let dx = H.x - O.x, dy = H.y - O.y;
                drawLine({x: O.x - dx, y: O.y - dy}, {x: H.x + dx, y: H.y + dy}, "rgba(255, 165, 0, 0.6)");
            }

            // Points
            if (document.getElementById('showO').checked) drawPoint(O, "blue", "O");
            if (document.getElementById('showG').checked) drawPoint(G, "green", "G");
            if (document.getElementById('showH').checked) drawPoint(H, "red", "H");
            if (document.getElementById('showN').checked) drawPoint(N, "purple", "N");

            // Vertices
            for (let p of pts) {
                ctx.beginPath(); ctx.arc(p.x, p.y, 8, 0, Math.PI*2);
                ctx.fillStyle = dragging === p ? "#ffcc00" : "#333"; ctx.fill();
                ctx.fillStyle = "black"; ctx.font = "bold 16px Arial"; ctx.fillText(p.label, p.x - 5, p.y - 12);
            }
        }
        draw();
    </script>
</body>
</html>
"""

components.html(html_code, height=800)
