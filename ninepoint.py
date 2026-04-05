import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บ / Set page configuration
st.set_page_config(layout="wide", page_title="Euler Line & 9-Point Circle")

st.title("Interactive Demonstration: Euler Line & Nine-Point Circle")
st.write("ลากจุดยอด (Drag the vertices) A, B, C เพื่อดูการเปลี่ยนแปลงแบบเรียลไทม์ (to see real-time changes).")

# --- โค้ด HTML/JS สำหรับการโต้ตอบแบบลื่นไหลและแผงแสดงตัวเลข (Metrics) พร้อม Watermark ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; background-color: white;}
        .controls-container { display: flex; flex-wrap: wrap; gap: 20px; margin: 10px 0 10px 0; justify-content: center; width: 100%; max-width: 900px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;}
        .control-group { display: flex; flex-direction: column; gap: 8px; min-width: 260px;}
        
        /* สไตล์สำหรับแผงตัวเลข (Metrics Panel) */
        .metrics-container { display: flex; flex-wrap: wrap; justify-content: space-around; gap: 10px; width: 100%; max-width: 900px; margin-bottom: 20px; padding: 15px; background: #e9ecef; border-radius: 8px; border: 1px solid #ced4da; color: #212529;}
        .metric-col { display: flex; flex-direction: column; gap: 6px; font-size: 15px; font-family: 'Courier New', Courier, monospace;}
        .metric-title { font-family: 'Segoe UI', sans-serif; font-weight: bold; border-bottom: 1px solid #adb5bd; padding-bottom: 4px; margin-bottom: 4px; color: #495057;}
        
        canvas { border: 1px solid #ccc; border-radius: 8px; background-color: #ffffff; cursor: crosshair; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
        .label { cursor: pointer; user-select: none; font-size: 14px; color: #333;}
        h4 { margin: 0 0 8px 0; font-size: 15px; color: #111; border-bottom: 2px solid #ddd; padding-bottom: 4px;}
        input[type="checkbox"] { margin-right: 8px; cursor: pointer;}
    </style>
</head>
<body>
    <div class="controls-container">
        <div class="control-group">
            <h4>1. เส้นโครงสร้าง / Structural Lines</h4>
            <label class="label"><input type="checkbox" id="showAlt" onchange="draw()"> เส้นส่วนสูง / Altitudes (H)</label>
            <label class="label"><input type="checkbox" id="showMed" onchange="draw()"> เส้นมัธยฐาน / Medians (G)</label>
            <label class="label"><input type="checkbox" id="showPerp" onchange="draw()"> เส้นแบ่งครึ่งตั้งฉาก / Perp. Bisectors (O)</label>
            <label class="label"><input type="checkbox" id="showEuler" checked onchange="draw()"> <strong>เส้นออยเลอร์ / Euler Line</strong></label>
        </div>
        <div class="control-group">
            <h4>2. จุดตัด & วงกลม / Centers & Circles</h4>
            <label class="label"><input type="checkbox" id="showH" checked onchange="draw()"> จุด H (Orthocenter)</label>
            <label class="label"><input type="checkbox" id="showG" checked onchange="draw()"> จุด G (Centroid)</label>
            <label class="label"><input type="checkbox" id="showCircum" checked onchange="draw()"> วงกลมล้อมรอบ / Circumcircle (O)</label>
            <label class="label"><input type="checkbox" id="showNineCirc" checked onchange="draw()"> <strong>วงกลมเก้าจุด / 9-Point Circle (N)</strong></label>
        </div>
        <div class="control-group">
            <h4>3. องค์ประกอบ 9 จุด / The 9 Points</h4>
            <label class="label"><input type="checkbox" id="showMid" checked onchange="draw()"> จุดกึ่งกลางด้าน / 3 Midpoints</label>
            <label class="label"><input type="checkbox" id="showFeet" checked onchange="draw()"> จุดโคนเส้นส่วนสูง / 3 Altitude Feet</label>
            <label class="label"><input type="checkbox" id="showEulerPts" checked onchange="draw()"> จุดออยเลอร์ / 3 Euler Points</label>
        </div>
    </div>

    <div class="metrics-container" id="metricsPanel">
        </div>
    
    <canvas id="canvas" width="850" height="550"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const metricsPanel = document.getElementById('metricsPanel');
        
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
                ctx.fillStyle = "#111"; ctx.font = "bold 13px Arial"; 
                ctx.fillText(label, p.x + 8, p.y - 8);
            }
        }

        function drawLine(p1, p2, color, dash=[], width=1) {
            ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = color; ctx.lineWidth = width; ctx.setLineDash(dash); 
            ctx.stroke(); ctx.setLineDash([]); ctx.lineWidth = 1;
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // --- DRAW WATERMARK ---
            ctx.save();
            ctx.globalAlpha = 0.08; // ความโปร่งแสง
            ctx.font = "bold 40px Arial";
            ctx.fillStyle = "#333";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.rotate(-Math.PI / 8); // เอียงข้อความเล็กน้อย
            ctx.fillText("by Dr.Che @ Math Mission Thailand", 0, 0);
            ctx.restore();

            const A = pts[0], B = pts[1], C = pts[2];

            const O = getCircumcenter(A, B, C);
            if (!O) {
                metricsPanel.innerHTML = "<strong style='color:red;'>Vertices are collinear (จุดอยู่บนเส้นตรงเดียวกัน)</strong>";
                return; 
            }
            
            const G = {x: (A.x + B.x + C.x) / 3, y: (A.y + B.y + C.y) / 3};
            const H = {x: 3*G.x - 2*O.x, y: 3*G.y - 2*O.y};
            const N = {x: (O.x + H.x) / 2, y: (O.y + H.y) / 2};
            const R = Math.hypot(O.x - A.x, O.y - A.y);
            const Rn = R / 2;

            // --- อัปเดตตัวเลขระยะทาง (Update Metrics) ---
            const dHG = Math.hypot(H.x - G.x, H.y - G.y).toFixed(1);
            const dHN = Math.hypot(H.x - N.x, H.y - N.y).toFixed(1);
            const dNG = Math.hypot(N.x - G.x, N.y - G.y).toFixed(1);
            const dGO = Math.hypot(G.x - O.x, G.y - O.y).toFixed(1);
            const dNO = Math.hypot(N.x - O.x, N.y - O.y).toFixed(1);
            
            metricsPanel.innerHTML = `
                <div class="metric-col">
                    <div class="metric-title">ระยะบนเส้นออยเลอร์ (Euler Line)</div>
                    <span><strong>HG = ${dHG}</strong></span>
                    <span>HN = ${dHN}</span>
                    <span>NG = ${dNG}</span>
                    <span>GO = ${dGO}</span>
                    <span>NO = ${dNO}</span>
                </div>
                <div class="metric-col">
                    <div class="metric-title">รัศมีวงกลม (Radii)</div>
                    <span>R (Circumradius) = ${R.toFixed(1)}</span>
                    <span>Rn (9-Point Radius) = ${Rn.toFixed(1)}</span>
                </div>
                <div class="metric-col">
                    <div class="metric-title">ความสัมพันธ์ (Relationships)</div>
                    <span>HN ≈ NO (N is midpoint)</span>
                    <span>HG (${dHG}) ≈ 2 × GO (${(dGO * 2).toFixed(1)})</span>
                    <span>R ≈ 2 × Rn</span>
                </div>
            `;

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
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;

            // --- DRAW CIRCLES ---
            if (document.getElementById('showCircum').checked) {
                ctx.beginPath(); ctx.arc(O.x, O.y, R, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(0, 0, 255, 0.3)"; ctx.setLineDash([5, 5]); ctx.stroke(); ctx.setLineDash([]);
            }
            if (document.getElementById('showNineCirc').checked) {
                ctx.beginPath(); ctx.arc(N.x, N.y, Rn, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(128, 0, 128, 0.8)"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;
            }

            // --- DRAW EULER LINE ---
            if (document.getElementById('showEuler').checked) {
                let dx = H.x - O.x, dy = H.y - O.y;
                drawLine({x: O.x - dx, y: O.y - dy}, {x: H.x + dx, y: H.y + dy}, "rgba(255, 165, 0, 0.7)", [], 3);
            }

            // --- DRAW THE 9 POINTS ---
            if (document.getElementById('showMid').checked) {
                drawPoint(M_BC, "green", "", 6); drawPoint(M_AC, "green", "", 6); drawPoint(M_AB, "green", "", 6);
            }
            if (document.getElementById('showFeet').checked) {
                drawPoint(F_A, "orange", "", 6); drawPoint(F_B, "orange", "", 6); drawPoint(F_C, "orange", "", 6);
            }
            if (document.getElementById('showEulerPts').checked) {
                if (document.getElementById('showH').checked) {
                    drawLine(A, H, "rgba(0,0,255,0.2)", [3,3]); drawLine(B, H, "rgba(0,0,255,0.2)", [3,3]); drawLine(C, H, "rgba(0,0,255,0.2)", [3,3]);
                }
                drawPoint(E_A, "#00cccc", "", 6); drawPoint(E_B, "#00cccc", "", 6); drawPoint(E_C, "#00cccc", "", 6);
            }

            // --- DRAW CENTERS ---
            if (document.getElementById('showCircum').checked) drawPoint(O, "blue", "O");
            if (document.getElementById('showG').checked) drawPoint(G, "green", "G");
            if (document.getElementById('showH').checked) drawPoint(H, "red", "H", 6);
            if (document.getElementById('showNineCirc').checked) drawPoint(N, "purple", "N");

            // --- DRAW DRAGGABLE VERTICES ---
            for (let p of pts) {
                ctx.beginPath(); ctx.arc(p.x, p.y, 9, 0, Math.PI*2);
                ctx.fillStyle = dragging === p ? "#ffcc00" : "#333"; ctx.fill();
                ctx.fillStyle = "black"; ctx.font = "bold 16px Arial"; ctx.fillText(p.label, p.x - 6, p.y - 13);
            }

            // --- DRAW COPYRIGHT ---
            ctx.save();
            ctx.fillStyle = "#888"; // สีเทาอ่อน
            ctx.font = "12px Arial";
            ctx.textAlign = "right";
            ctx.fillText("© 2026 by Dr.Che @ Math Mission Thailand. All rights reserved.", canvas.width - 15, canvas.height - 15);
            ctx.restore();
        }
        
        draw(); // Initial Render
    </script>
</body>
</html>
"""

# แสดงหน้าจอ
components.html(html_code, height=850)
