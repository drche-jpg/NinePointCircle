html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .controls-container { display: flex; flex-wrap: wrap; gap: 20px; margin: 10px 0 20px 0; justify-content: center; max-width: 800px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;}
        .control-group { display: flex; flex-direction: column; gap: 8px; }
        canvas { border: 1px solid #ccc; border-radius: 8px; background-color: #ffffff; cursor: crosshair;}
        .label { cursor: pointer; user-select: none; font-size: 14px;}
        h4 { margin: 0 0 8px 0; font-size: 15px; color: #333; border-bottom: 2px solid #ddd; padding-bottom: 4px;}
    </style>
</head>
<body>
    <div class="controls-container">
        <div class="control-group">
            <h4>โครงสร้างหลัก (Base)</h4>
            <label class="label"><input type="checkbox" id="showNine" checked onchange="draw()"> แสดงวงกลมเก้าจุด</label>
            <label class="label"><input type="checkbox" id="showH" checked onchange="draw()"> จุด H (Orthocenter)</label>
        </div>
        <div class="control-group">
            <h4>9 จุดบนวงกลม (The 9 Points)</h4>
            <label class="label"><input type="checkbox" id="showMid" checked onchange="draw()"> 1. จุดกึ่งกลางด้าน 3 จุด</label>
            <label class="label"><input type="checkbox" id="showAlt" checked onchange="draw()"> 2. จุดโคนเส้นส่วนสูง 3 จุด</label>
            <label class="label"><input type="checkbox" id="showEuler" checked onchange="draw()"> 3. จุดออยเลอร์ 3 จุด</label>
        </div>
    </div>
    <canvas id="canvas" width="800" height="500"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        let pts = [{x: 400, y: 100, label: 'A'}, {x: 150, y: 400, label: 'B'}, {x: 650, y: 400, label: 'C'}];
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
                ctx.fillStyle = "#333"; ctx.font = "12px Arial"; ctx.fillText(label, p.x + 8, p.y - 8);
            }
        }

        function drawLine(p1, p2, color) {
            ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = color; ctx.setLineDash([3, 3]); ctx.stroke(); ctx.setLineDash([]);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const A = pts[0], B = pts[1], C = pts[2];

            const O = getCircumcenter(A, B, C);
            if (!O) return;
            
            const G = {x: (A.x + B.x + C.x) / 3, y: (A.y + B.y + C.y) / 3};
            const H = {x: 3*G.x - 2*O.x, y: 3*G.y - 2*O.y};
            const N = {x: (O.x + H.x) / 2, y: (O.y + H.y) / 2};
            const R = Math.hypot(O.x - A.x, O.y - A.y);

            // 1. Midpoints
            const M1 = {x: (B.x + C.x)/2, y: (B.y + C.y)/2};
            const M2 = {x: (A.x + C.x)/2, y: (A.y + C.y)/2};
            const M3 = {x: (A.x + B.x)/2, y: (A.y + B.y)/2};

            // 2. Altitude Feet
            const F1 = getAltitudeFoot(A, B, C);
            const F2 = getAltitudeFoot(B, A, C);
            const F3 = getAltitudeFoot(C, A, B);

            // 3. Euler Points (Midpoints of AH, BH, CH)
            const E1 = {x: (A.x + H.x)/2, y: (A.y + H.y)/2};
            const E2 = {x: (B.x + H.x)/2, y: (B.y + H.y)/2};
            const E3 = {x: (C.x + H.x)/2, y: (C.y + H.y)/2};

            // Draw Triangle
            ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.lineTo(C.x, C.y); ctx.closePath();
            ctx.strokeStyle = "black"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;

            // Draw Nine-Point Circle
            if (document.getElementById('showNine').checked) {
                ctx.beginPath(); ctx.arc(N.x, N.y, R/2, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(128, 0, 128, 0.6)"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;
                drawPoint(N, "purple", "N (Center)");
            }

            // Draw H
            if (document.getElementById('showH').checked) drawPoint(H, "red", "H", 6);

            // Draw 9 Points based on toggles
            if (document.getElementById('showMid').checked) {
                drawPoint(M1, "green", "M1", 6); drawPoint(M2, "green", "M2", 6); drawPoint(M3, "green", "M3", 6);
            }
            if (document.getElementById('showAlt').checked) {
                drawLine(A, F1, "rgba(255,0,0,0.3)"); drawLine(B, F2, "rgba(255,0,0,0.3)"); drawLine(C, F3, "rgba(255,0,0,0.3)");
                drawPoint(F1, "orange", "F1", 6); drawPoint(F2, "orange", "F2", 6); drawPoint(F3, "orange", "F3", 6);
            }
            if (document.getElementById('showEuler').checked) {
                if (document.getElementById('showH').checked) {
                    drawLine(A, H, "rgba(0,0,255,0.2)"); drawLine(B, H, "rgba(0,0,255,0.2)"); drawLine(C, H, "rgba(0,0,255,0.2)");
                }
                drawPoint(E1, "blue", "E1", 6); drawPoint(E2, "blue", "E2", 6); drawPoint(E3, "blue", "E3", 6);
            }

            // Draw Vertices
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
