import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บ / Set page configuration
st.set_page_config(layout="wide", page_title="Euler Line & 9-Point Circle")

# โค้ดสำหรับซ่อนเมนู มุมขวาบน และ Footer ของ Streamlit (ป้องกันคนกดดูโค้ด)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Interactive Demonstration: Euler Line & Nine-Point Circle")
st.write("เอกสารประกอบการเรียนรู้ เรขาคณิตแบบโต้ตอบ (Interactive Geometry Demo)")

# --- โค้ด HTML/JS สำหรับการโต้ตอบ + รองรับจอมือถือ (Touch) + Zoom/Pan + Description + Metrics + Watermark ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; background-color: white; touch-action: pan-y; }
        
        /* กล่องคำอธิบาย (Description Box) */
        .info-container { width: 100%; max-width: 950px; background: #e3f2fd; border-left: 5px solid #0d6efd; padding: 15px 20px; margin: 10px 0 15px 0; border-radius: 4px; color: #333; font-size: 14.5px; box-sizing: border-box; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
        .info-container h3 { margin: 0 0 8px 0; color: #0056b3; font-size: 18px; display: flex; align-items: center; gap: 8px;}
        .info-container p { margin: 5px 0; line-height: 1.5;}
        .info-container ul { margin: 5px 0 0 0; padding-left: 25px;}
        .info-container li { margin-bottom: 6px; line-height: 1.4;}

        /* แผงควบคุม (Controls) */
        .controls-container { display: flex; flex-wrap: wrap; gap: 15px; margin: 0 0 15px 0; justify-content: center; width: 100%; max-width: 950px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6; box-sizing: border-box;}
        .control-group { display: flex; flex-direction: column; gap: 8px; min-width: 210px;}
        
        canvas { border: 1px solid #ccc; border-radius: 8px; background-color: #ffffff; cursor: crosshair; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; max-width: 100%; touch-action: none;}
        
        /* แผงตัวเลข (Metrics) */
        .metrics-container { display: flex; flex-wrap: wrap; justify-content: space-around; gap: 10px; width: 100%; max-width: 950px; margin-bottom: 15px; padding: 15px; background: #e9ecef; border-radius: 8px; border: 1px solid #ced4da; color: #212529; box-sizing: border-box;}
        .metric-col { display: flex; flex-direction: column; gap: 6px; font-size: 15px; font-family: 'Courier New', Courier, monospace;}
        .metric-title { font-family: 'Segoe UI', sans-serif; font-weight: bold; border-bottom: 1px solid #adb5bd; padding-bottom: 4px; margin-bottom: 4px; color: #495057;}
        
        .label { cursor: pointer; user-select: none; font-size: 13px; color: #333;}
        h4 { margin: 0 0 8px 0; font-size: 14px; color: #111; border-bottom: 2px solid #ddd; padding-bottom: 4px;}
        input[type="checkbox"] { margin-right: 6px; cursor: pointer;}
        
        .zoom-controls { display: flex; flex-direction: column; background: #e3f2fd; padding: 10px; border-radius: 6px; border: 1px solid #90caf9; }
        .reset-btn { margin-top: 8px; padding: 4px 8px; border-radius: 4px; border: 1px solid #aaa; background: white; cursor: pointer; font-size: 12px; }
        .reset-btn:hover { background: #eee; }
    </style>
</head>
<body>

    <div class="info-container">
        <h3>💡 คำแนะนำ & ทฤษฎีบท (Instructions & Concepts)</h3>
        <p><strong>การใช้งาน (How to use):</strong> ใช้เมาส์หรือ<strong>นิ้วสัมผัส</strong>ลากที่จุดยอด <strong>A, B, หรือ C</strong> เพื่อเปลี่ยนรูปทรงของสามเหลี่ยมอย่างอิสระ (Drag vertices to change the triangle shape). ลองเปิด-ปิดตัวเลือกด้านล่างเพื่อสังเกตการสร้างเส้นและจุดตัดต่างๆ</p>
        <ul>
            <li><strong>เส้นออยเลอร์ (Euler Line):</strong> ไม่ว่าสามเหลี่ยมจะเปลี่ยนรูปไปอย่างไร จุดศูนย์กลางวงกลมล้อมรอบ (O), เซนทรอยด์ (G), และจุดออร์โทเซนเตอร์ (H) จะเรียงตัวเป็นเส้นตรงเดียวกันเสมอ</li>
            <li><strong>วงกลมเก้าจุด (9-Point Circle):</strong> วงกลมที่จุดศูนย์กลาง (N) อยู่บนเส้นออยเลอร์ และจะลากผ่านจุดสำคัญ 9 จุดพอดี ได้แก่: จุดกึ่งกลางด้าน (3), จุดโคนเส้นส่วนสูง (3), และจุดออยเลอร์ (3)</li>
            <li><strong>จุดออยเลอร์ (Euler Points):</strong> คือ <strong>"จุดกึ่งกลาง"</strong> ของเส้นตรงที่ลากเชื่อมระหว่าง <strong>จุดออร์โทเซนเตอร์ (H)</strong> ไปยัง <strong>จุดยอดทั้งสาม (A, B, C)</strong></li>
        </ul>
    </div>

    <div class="controls-container">
        <div class="control-group zoom-controls">
            <h4>🔍 มุมมอง / View Control</h4>
            <label class="label">ซูม (Zoom): <input type="range" id="zoomSlider" min="0.1" max="4" step="0.05" value="1" oninput="updateZoomFromSlider()"></label>
            <span style="font-size: 11px; color: #555;">* เลื่อนล้อเมาส์เพื่อซูม (Scroll to zoom)</span>
            <span style="font-size: 11px; color: #555;">* ลากที่ว่างเพื่อแพนจอ (Drag background to pan)</span>
            <button class="reset-btn" onclick="resetView()">รีเซ็ตมุมมอง / Reset View</button>
        </div>
        <div class="control-group">
            <h4>1. เส้นโครงสร้าง / Lines</h4>
            <label class="label"><input type="checkbox" id="showAlt" onchange="draw()"> เส้นส่วนสูง / Altitudes</label>
            <label class="label"><input type="checkbox" id="showMed" onchange="draw()"> เส้นมัธยฐาน / Medians</label>
            <label class="label"><input type="checkbox" id="showPerp" onchange="draw()"> เส้นแบ่งครึ่งตั้งฉาก / Perp. Bisectors</label>
            <label class="label"><input type="checkbox" id="showEuler" checked onchange="draw()"> <strong>เส้นออยเลอร์ / Euler Line</strong></label>
        </div>
        <div class="control-group">
            <h4>2. วงกลมหลัก / Circles</h4>
            <label class="label"><input type="checkbox" id="showH" checked onchange="draw()"> จุด H (Orthocenter)</label>
            <label class="label"><input type="checkbox" id="showG" checked onchange="draw()"> จุด G (Centroid)</label>
            <label class="label"><input type="checkbox" id="showCircum" checked onchange="draw()"> วงกลมล้อมรอบ / Circumcircle</label>
            <label class="label"><input type="checkbox" id="showNineCirc" checked onchange="draw()"> <strong>วงกลมเก้าจุด / 9-Point Circle</strong></label>
        </div>
        <div class="control-group">
            <h4>3. องค์ประกอบ 9 จุด / 9 Points</h4>
            <label class="label"><input type="checkbox" id="showMid" checked onchange="draw()"> จุดกึ่งกลางด้าน / 3 Midpoints</label>
            <label class="label"><input type="checkbox" id="showFeet" checked onchange="draw()"> จุดโคนเส้นส่วนสูง / 3 Altitude Feet</label>
            <label class="label"><input type="checkbox" id="showEulerPts" checked onchange="draw()"> จุดออยเลอร์ / 3 Euler Points</label>
        </div>
    </div>

    <canvas id="canvas" width="950" height="550"></canvas>

    <div class="metrics-container" id="metricsPanel">
        </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const metricsPanel = document.getElementById('metricsPanel');
        
        let pts = [{x: 475, y: 150, label: 'A'}, {x: 275, y: 400, label: 'B'}, {x: 675, y: 400, label: 'C'}];
        
        let dragging = null;
        let isPanning = false;
        let scale = 1.0;
        let offsetX = 0;
        let offsetY = 0;
        let startPanX = 0;
        let startPanY = 0;

        // แปลงพิกัดหน้าจอ เป็นพิกัดโลก
        function toWorld(sx, sy) {
            return { x: (sx - offsetX) / scale, y: (sy - offsetY) / scale };
        }

        // --- MOUSE EVENTS ---
        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const sx = e.clientX - rect.left;
            const sy = e.clientY - rect.top;
            handleDown(sx, sy);
        });
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            handleMove(e.clientX - rect.left, e.clientY - rect.top);
        });
        canvas.addEventListener('mouseup', handleUp);
        canvas.addEventListener('mouseleave', handleUp);

        // --- TOUCH EVENTS (สำหรับจอมือถือ/แท็บเล็ต) ---
        canvas.addEventListener('touchstart', (e) => {
            if(e.touches.length === 1) {
                const rect = canvas.getBoundingClientRect();
                const sx = e.touches[0].clientX - rect.left;
                const sy = e.touches[0].clientY - rect.top;
                if(handleDown(sx, sy)) {
                    e.preventDefault(); // ป้องกันหน้าจอเลื่อนเวลาลากจุด
                }
            }
        }, {passive: false});

        canvas.addEventListener('touchmove', (e) => {
            if(dragging || isPanning) e.preventDefault(); // ป้องกันหน้าจอเลื่อน
            if(e.touches.length === 1) {
                const rect = canvas.getBoundingClientRect();
                handleMove(e.touches[0].clientX - rect.left, e.touches[0].clientY - rect.top);
            }
        }, {passive: false});
        
        canvas.addEventListener('touchend', handleUp);
        canvas.addEventListener('touchcancel', handleUp);

        // --- COMMON EVENT LOGIC ---
        function handleDown(sx, sy) {
            const w = toWorld(sx, sy);
            for (let p of pts) {
                // ขยายพื้นที่สัมผัส (Hitbox) ให้ใหญ่ขึ้นสำหรับนิ้วมือ (40 px)
                if (Math.hypot(p.x - w.x, p.y - w.y) < 40 / scale) { 
                    dragging = p; 
                    return true; 
                }
            }
            isPanning = true;
            startPanX = sx - offsetX;
            startPanY = sy - offsetY;
            return false;
        }

        function handleMove(sx, sy) {
            if (dragging) {
                const w = toWorld(sx, sy);
                dragging.x = w.x;
                dragging.y = w.y;
                draw();
            } else if (isPanning) {
                offsetX = sx - startPanX;
                offsetY = sy - startPanY;
                draw();
            }
        }

        function handleUp() {
            dragging = null;
            isPanning = false;
        }

        // Wheel Event สำหรับซูมผ่านลูกกลิ้งเมาส์
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const oldScale = scale;
            scale += e.deltaY * -0.001;
            scale = Math.min(Math.max(0.1, scale), 4.0);
            document.getElementById('zoomSlider').value = scale;
            
            const rect = canvas.getBoundingClientRect();
            const sx = e.clientX - rect.left;
            const sy = e.clientY - rect.top;
            offsetX = sx - (sx - offsetX) * (scale / oldScale);
            offsetY = sy - (sy - offsetY) * (scale / oldScale);
            draw();
        });

        function updateZoomFromSlider() {
            const oldScale = scale;
            scale = parseFloat(document.getElementById('zoomSlider').value);
            const cx = canvas.width / 2;
            const cy = canvas.height / 2;
            offsetX = cx - (cx - offsetX) * (scale / oldScale);
            offsetY = cy - (cy - offsetY) * (scale / oldScale);
            draw();
        }

        function resetView() {
            scale = 1.0; offsetX = 0; offsetY = 0;
            document.getElementById('zoomSlider').value = 1;
            draw();
        }

        // Math Functions
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
            ctx.beginPath(); ctx.arc(p.x, p.y, size/scale, 0, Math.PI*2);
            ctx.fillStyle = color; ctx.fill(); ctx.strokeStyle = "white"; ctx.lineWidth = 1/scale; ctx.stroke();
            if(label) {
                ctx.fillStyle = "#111"; 
                ctx.font = "bold " + Math.max(10, 13/scale) + "px Arial"; 
                ctx.fillText(label, p.x + 8/scale, p.y - 8/scale);
            }
        }

        function drawLine(p1, p2, color, dash=[], width=1) {
            ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = color; ctx.lineWidth = width/scale; 
            if(dash.length > 0) ctx.setLineDash(dash.map(d => d/scale)); 
            ctx.stroke(); ctx.setLineDash([]);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // --- DRAW WATERMARK ---
            ctx.save();
            ctx.globalAlpha = 0.08;
            ctx.font = "bold 45px Arial";
            ctx.fillStyle = "#333";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.rotate(-Math.PI / 8);
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

            // --- อัปเดตแผง Metrics ---
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

            const M_BC = {x: (B.x + C.x)/2, y: (B.y + C.y)/2};
            const M_AC = {x: (A.x + C.x)/2, y: (A.y + C.y)/2};
            const M_AB = {x: (A.x + B.x)/2, y: (A.y + B.y)/2};
            const F_A = getAltitude
