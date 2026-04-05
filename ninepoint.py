import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บ / Set page configuration
st.set_page_config(layout="wide", page_title="Centroid, Orthocenter,Euler Line & 9-Point Circle")

# โค้ดสำหรับซ่อนเมนู มุมขวาบน และ Footer ของ Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Interactive Demonstration: Centroid, Orthocenter,Euler Line & 9-Point Circle")

# --- โค้ด HTML/JS ฉบับสมบูรณ์ พร้อมคำนิยามและระบบสัมผัส ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; background-color: white; touch-action: pan-y; }
        
        .info-container { width: 100%; max-width: 950px; background: #f0f7ff; border-left: 5px solid #0d6efd; padding: 20px; margin: 10px 0 20px 0; border-radius: 4px; color: #333; font-size: 14px; box-sizing: border-box; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
        .info-container h3 { margin: 0 0 10px 0; color: #0056b3; font-size: 18px; border-bottom: 1px solid #cce3ff; padding-bottom: 5px;}
        .info-container p { margin: 8px 0; line-height: 1.6;}
        .info-container ul { margin: 10px 0; padding-left: 20px;}
        .info-container li { margin-bottom: 10px; line-height: 1.5;}
        .en-text { color: #666; font-size: 13px; display: block; font-style: italic; margin-top: 2px;}
        .highlight { color: #d63384; font-weight: bold; }

        .controls-container { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 15px; justify-content: center; width: 100%; max-width: 950px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6; box-sizing: border-box;}
        .control-group { display: flex; flex-direction: column; gap: 8px; min-width: 210px;}
        
        canvas { border: 1px solid #ccc; border-radius: 8px; background-color: #ffffff; cursor: crosshair; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; max-width: 100%; touch-action: none;}
        
        .metrics-container { display: flex; flex-wrap: wrap; justify-content: space-around; gap: 10px; width: 100%; max-width: 950px; margin-bottom: 15px; padding: 15px; background: #f1f3f5; border-radius: 8px; border: 1px solid #ced4da; color: #212529; box-sizing: border-box;}
        .metric-col { display: flex; flex-direction: column; gap: 6px; font-size: 14px; font-family: 'Courier New', Courier, monospace;}
        .metric-title { font-family: 'Segoe UI', sans-serif; font-weight: bold; border-bottom: 1px solid #adb5bd; padding-bottom: 4px; margin-bottom: 4px; color: #495057;}
        
        .label { cursor: pointer; user-select: none; font-size: 13px; color: #333;}
        h4 { margin: 0 0 8px 0; font-size: 14px; color: #111; border-bottom: 2px solid #ddd; padding-bottom: 4px;}
        input[type="checkbox"] { margin-right: 6px; cursor: pointer;}
        
        .zoom-controls { background: #eefbff; border: 1px solid #b3e5fc; padding: 10px; border-radius: 6px; }
        .reset-btn { margin-top: 8px; padding: 5px 10px; border-radius: 4px; border: 1px solid #aaa; background: white; cursor: pointer; font-size: 12px; transition: 0.2s;}
        .reset-btn:hover { background: #f0f0f0; }
    </style>
</head>
<body>

    <div class="info-container">
        <h3>📚 คำนิยาม & คุณสมบัติ (Definitions & Properties)</h3>
        <ul>
            <li><strong>จุดศูนย์กลางวงกลมเก้าจุด (Nine-Point Center - N):</strong> 
                คือจุดกึ่งกลางของเส้นตรงที่เชื่อมระหว่างจุด Orthocenter (H) และ Circumcenter (O) โดยจะมีระยะห่าง <span class="highlight">HN = NO</span> เสมอ
                <span class="en-text">The midpoint of the segment connecting the Orthocenter (H) and Circumcenter (O).</span>
            </li>
            <li><strong>เส้นออยเลอร์ (Euler Line):</strong> 
                เส้นตรงที่ลากผ่านจุด O, G, และ H ในสามเหลี่ยมที่ไม่ใช่สามเหลี่ยมด้านเท่า  โดยมีความสัมพันธ์คือ <span class="highlight">HG = 2GO</span> และจุด N จะอยู่บนเส้นนี้ด้วย 
                <span class="en-text">The unique line passing through O, G, and H. The center N also lies on this line.</span>
            </li>
            <li><strong>รัศมีวงกลม (Radius):</strong> 
                รัศมีของวงกลมเก้าจุด (Rn) จะมีขนาดเป็น <strong>ครึ่งหนึ่ง</strong> ของรัศมีวงกลมล้อมรอบ (R) เสมอ  (<span class="highlight">Rn = R / 2</span>)
                <span class="en-text">The nine-point radius is always exactly half of the circumradius.</span>
            </li>
            <li><strong>จุดออยเลอร์ (Euler Points):</strong> 
                จุดกึ่งกลางของส่วนเส้นตรงที่เชื่อมระหว่างจุด Orthocenter (H) ไปยังจุดยอดทั้งสาม (A, B, C) 
                <span class="en-text">The midpoints of the segments connecting H to each vertex.</span>
            </li>
        </ul>
        <p style="font-size: 13px; color: #666; border-top: 1px dashed #ccc; padding-top: 8px;">
            * <strong>มือถือ (Mobile):</strong> แตะที่จุดยอดค้างไว้จนเปลี่ยนเป็นสีเหลืองแล้วจึงลาก / Tap and hold a vertex until it turns yellow, then drag.
        </p>
    </div>

    <div class="controls-container">
        <div class="control-group zoom-controls">
            <h4>🔍 มุมมอง / View Control</h4>
            <label class="label">ซูม (Zoom): <input type="range" id="zoomSlider" min="0.1" max="4" step="0.05" value="1" oninput="updateZoomFromSlider()"></label>
            <button class="reset-btn" onclick="resetView()">รีเซ็ตมุมมอง / Reset View</button>
        </div>
        <div class="control-group">
            <h4>1. เส้น / Lines</h4>
            <label class="label"><input type="checkbox" id="showAlt" onchange="draw()"> เส้นส่วนสูง / Altitudes</label>
            <label class="label"><input type="checkbox" id="showMed" onchange="draw()"> เส้นมัธยฐาน / Medians</label>
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
            <label class="label"><input type="checkbox" id="showMid" checked onchange="draw()"> กึ่งกลางด้าน / Midpoints</label>
            <label class="label"><input type="checkbox" id="showFeet" checked onchange="draw()"> โคนเส้นส่วนสูง / Feet</label>
            <label class="label"><input type="checkbox" id="showEulerPts" checked onchange="draw()"> จุดออยเลอร์ / Euler Points</label>
        </div>
    </div>

    <canvas id="canvas" width="950" height="550"></canvas>

    <div class="metrics-container" id="metricsPanel"></div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const metricsPanel = document.getElementById('metricsPanel');
        let pts = [{x: 475, y: 150, label: 'A'}, {x: 275, y: 400, label: 'B'}, {x: 675, y: 400, label: 'C'}];
        let dragging = null, isPanning = false, scale = 1.0, offsetX = 0, offsetY = 0, startPanX = 0, startPanY = 0;

        function toWorld(sx, sy) { return { x: (sx - offsetX) / scale, y: (sy - offsetY) / scale }; }

        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            handleDown(e.clientX - rect.left, e.clientY - rect.top);
        });
        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            handleMove(e.clientX - rect.left, e.clientY - rect.top);
        });
        canvas.addEventListener('mouseup', handleUp);
        canvas.addEventListener('mouseleave', handleUp);

        canvas.addEventListener('touchstart', (e) => {
            if(e.touches.length === 1) {
                const rect = canvas.getBoundingClientRect();
                if(handleDown(e.touches[0].clientX - rect.left, e.touches[0].clientY - rect.top)) e.preventDefault();
            }
        }, {passive: false});
        canvas.addEventListener('touchmove', (e) => {
            if(dragging || isPanning) e.preventDefault();
            if(e.touches.length === 1) {
                const rect = canvas.getBoundingClientRect();
                handleMove(e.touches[0].clientX - rect.left, e.touches[0].clientY - rect.top);
            }
        }, {passive: false});
        canvas.addEventListener('touchend', handleUp);

        function handleDown(sx, sy) {
            const w = toWorld(sx, sy);
            for (let p of pts) if (Math.hypot(p.x - w.x, p.y - w.y) < 40 / scale) { dragging = p; return true; }
            isPanning = true; startPanX = sx - offsetX; startPanY = sy - offsetY; return false;
        }
        function handleMove(sx, sy) {
            if (dragging) { const w = toWorld(sx, sy); dragging.x = w.x; dragging.y = w.y; draw(); }
            else if (isPanning) { offsetX = sx - startPanX; offsetY = sy - startPanY; draw(); }
        }
        function handleUp() { dragging = null; isPanning = false; }

        canvas.addEventListener('wheel', (e) => {
            e.preventDefault(); const oldScale = scale;
            scale = Math.min(Math.max(0.1, scale + e.deltaY * -0.001), 4.0);
            document.getElementById('zoomSlider').value = scale;
            const rect = canvas.getBoundingClientRect();
            offsetX = (e.clientX - rect.left) - ((e.clientX - rect.left) - offsetX) * (scale / oldScale);
            offsetY = (e.clientY - rect.top) - ((e.clientY - rect.top) - offsetY) * (scale / oldScale);
            draw();
        });

        function updateZoomFromSlider() {
            const oldScale = scale; scale = parseFloat(document.getElementById('zoomSlider').value);
            offsetX = (canvas.width/2) - ((canvas.width/2) - offsetX) * (scale / oldScale);
            offsetY = (canvas.height/2) - ((canvas.height/2) - offsetY) * (scale / oldScale);
            draw();
        }

        function resetView() { scale = 1.0; offsetX = 0; offsetY = 0; document.getElementById('zoomSlider').value = 1; draw(); }

        function getCircumcenter(A, B, C) {
            let D = 2 * (A.x * (B.y - C.y) + B.x * (C.y - A.y) + C.x * (A.y - B.y));
            if (Math.abs(D) < 0.001) return null;
            return {
                x: ((A.x**2 + A.y**2) * (B.y - C.y) + (B.x**2 + B.y**2) * (C.y - A.y) + (C.x**2 + C.y**2) * (A.y - B.y)) / D,
                y: ((A.x**2 + A.y**2) * (C.x - B.x) + (B.x**2 + B.y**2) * (A.x - C.x) + (C.x**2 + C.y**2) * (B.x - A.x)) / D
            };
        }

        function getAltitudeFoot(A, B, C) {
            let k = ((C.y - B.y) * (A.x - B.x) - (C.x - B.x) * (A.y - B.y)) / (Math.pow(C.y - B.y, 2) + Math.pow(C.x - B.x, 2));
            return { x: A.x - k * (C.y - B.y), y: A.y + k * (C.x - B.x) };
        }

        function drawPoint(p, color, label, size=5) {
            ctx.beginPath(); ctx.arc(p.x, p.y, size/scale, 0, Math.PI*2);
            ctx.fillStyle = color; ctx.fill(); ctx.strokeStyle = "white"; ctx.lineWidth = 1/scale; ctx.stroke();
            if(label) { ctx.fillStyle = "#111"; ctx.font = "bold " + Math.max(10, 13/scale) + "px Arial"; ctx.fillText(label, p.x + 8/scale, p.y - 8/scale); }
        }

        function drawLine(p1, p2, color, dash=[], width=1) {
            ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = color; ctx.lineWidth = width/scale; if(dash.length) ctx.setLineDash(dash.map(d => d/scale));
            ctx.stroke(); ctx.setLineDash([]);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.save(); ctx.globalAlpha = 0.08; ctx.font = "bold 40px Arial"; ctx.fillStyle = "#333"; ctx.textAlign = "center";
            ctx.translate(canvas.width/2, canvas.height/2); ctx.rotate(-Math.PI/8); ctx.fillText("by Dr.Che @ Math Mission Thailand", 0, 0); ctx.restore();

            const A = pts[0], B = pts[1], C = pts[2], O = getCircumcenter(A, B, C);
            if (!O) { metricsPanel.innerHTML = "<b style='color:red;'>Collinear points!</b>"; return; }
            
            const G = {x: (A.x + B.x + C.x)/3, y: (A.y + B.y + C.y)/3}, H = {x: 3*G.x - 2*O.x, y: 3*G.y - 2*O.y};
            const N = {x: (O.x + H.x)/2, y: (O.y + H.y)/2}, R = Math.hypot(O.x - A.x, O.y - A.y), Rn = R/2;

            const dHG = Math.hypot(H.x - G.x, H.y - G.y).toFixed(1), dGO = Math.hypot(G.x - O.x, G.y - O.y).toFixed(1);
            const dHN = Math.hypot(H.x - N.x, H.y - N.y).toFixed(1), dNO = Math.hypot(N.x - O.x, N.y - O.y).toFixed(1);
            
            metricsPanel.innerHTML = `
                <div class="metric-col"><div class="metric-title">Euler Line Distances</div><span>HG: ${dHG}</span><span>HN: ${dHN}</span><span>NO: ${dNO}</span><span>GO: ${dGO}</span></div>
                <div class="metric-col"><div class="metric-title">Radii</div><span>R (Circum): ${R.toFixed(1)}</span><span>Rn (9-Point): ${Rn.toFixed(1)}</span></div>
                <div class="metric-col"><div class="metric-title">Logic Check</div><span>HN ≈ NO (midpoint)</span><span>HG ≈ 2 × GO</span><span>R ≈ 2 × Rn</span></div>`;

            ctx.save(); ctx.translate(offsetX, offsetY); ctx.scale(scale, scale);
            const M1 = {x:(B.x+C.x)/2, y:(B.y+C.y)/2}, M2 = {x:(A.x+C.x)/2, y:(A.y+C.y)/2}, M3 = {x:(A.x+B.x)/2, y:(A.y+B.y)/2};
            const F1 = getAltitudeFoot(A, B, C), F2 = getAltitudeFoot(B, A, C), F3 = getAltitudeFoot(C, A, B);
            const E1 = {x:(A.x+H.x)/2, y:(A.y+H.y)/2}, E2 = {x:(B.x+H.x)/2, y:(B.y+H.y)/2}, E3 = {x:(C.x+H.x)/2, y:(C.y+H.y)/2};

            if(document.getElementById('showMed').checked) [ [A,M1],[B,M2],[C,M3] ].forEach(l => drawLine(l[0],l[1],"rgba(0,128,0,0.3)"));
            if(document.getElementById('showAlt').checked) [ [A,F1],[B,F2],[C,F3] ].forEach(l => drawLine(l[0],l[1],"rgba(255,0,0,0.3)"));
            
            ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.lineTo(C.x, C.y); ctx.closePath();
            ctx.strokeStyle = "#000"; ctx.lineWidth = 2/scale; ctx.stroke();

            if(document.getElementById('showCircum').checked) {
                ctx.beginPath(); ctx.arc(O.x, O.y, R, 0, Math.PI*2); ctx.strokeStyle = "rgba(0,0,255,0.2)"; ctx.setLineDash([5/scale, 5/scale]); ctx.stroke(); ctx.setLineDash([]);
                drawPoint(O, "blue", "O");
            }
            if(document.getElementById('showNineCirc').checked) {
                ctx.beginPath(); ctx.arc(N.x, N.y, Rn, 0, Math.PI*2); ctx.strokeStyle = "rgba(128,0,128,0.7)"; ctx.lineWidth = 2/scale; ctx.stroke();
                drawPoint(N, "purple", "N");
            }
            if(document.getElementById('showEuler').checked) drawLine({x:O.x-(H.x-O.x), y:O.y-(H.y-O.y)}, {x:H.x+(H.x-O.x), y:H.y+(H.y-O.y)}, "orange", [], 2);

            if(document.getElementById('showMid').checked) [M1,M2,M3].forEach(p => drawPoint(p, "green", "", 6));
            if(document.getElementById('showFeet').checked) [F1,F2,F3].forEach(p => drawPoint(p, "orange", "", 6));
            if(document.getElementById('showEulerPts').checked) [E1,E2,E3].forEach(p => drawPoint(p, "#00cccc", "", 6));
            if(document.getElementById('showG').checked) drawPoint(G, "green", "G");
            if(document.getElementById('showH').checked) drawPoint(H, "red", "H", 6);

            pts.forEach(p => {
                ctx.beginPath(); ctx.arc(p.x, p.y, 9/scale, 0, Math.PI*2); ctx.fillStyle = dragging === p ? "#fc0" : "#333"; ctx.fill();
                ctx.fillStyle = "#000"; ctx.font = "bold "+Math.max(12, 16/scale)+"px Arial"; ctx.fillText(p.label, p.x-6/scale, p.y-13/scale);
            });
            ctx.restore();
            ctx.fillStyle = "#888"; ctx.font = "11px Arial"; ctx.textAlign = "right"; ctx.fillText("© 2026 Dr.Che @ Math Mission Thailand", canvas.width-15, canvas.height-15);
        }
        draw();
    </script>
</body>
</html>
"""

components.html(html_code, height=1400, scrolling=True)
