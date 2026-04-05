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
    * **The Circumcenter (O):** Center of the circle enclosing the triangle.
    * **The Centroid (G):** The center of mass (intersection of medians).
    * **The Orthocenter (H):** The intersection of the three altitudes.
    """)
    
    st.header("Slide 2: The Euler Line")
    st.markdown("""
    Swiss mathematician Leonhard Euler discovered that in any non-equilateral triangle, **O, G, and H perfectly align on a single straight line**. 
    Furthermore, the distance from H to G is exactly twice the distance from G to O.
    """)

with col2:
    st.header("Slide 3: The Nine-Point Circle")
    st.markdown("""
    There is a magic circle that weaves through 9 specific points:
    1. The 3 midpoints of the sides.
    2. The 3 feet of the altitudes.
    3. The 3 "Euler points" (midpoints between H and the vertices).
    """)
    st.header("Slide 4: Properties of the Circle")
    st.markdown("""
    * **The Center (N):** Sits exactly halfway between the Orthocenter (H) and Circumcenter (O).
    * **The Radius:** Exactly half the size of the large circumcircle.
    """)

st.write("---")
st.header("Interactive Demonstration")
st.write("Click and drag the vertices (A, B, or C) below to see the geometry recalculate smoothly in real-time.")

# --- SMOOTH INTERACTIVE HTML/JS WIDGET ---
# We inject an HTML5 Canvas to handle the smooth mouse dragging that Plotly cannot do natively.
html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; }
        .controls { margin-top: 15px; display: flex; gap: 20px; font-size: 16px; }
        canvas { border: 1px solid #ccc; border-radius: 8px; background-color: #fafafa; cursor: crosshair; margin-top: 10px;}
        .label { cursor: pointer; user-select: none;}
    </style>
</head>
<body>
    <div class="controls">
        <label class="label"><input type="checkbox" id="showCircum" checked> Circumcircle</label>
        <label class="label"><input type="checkbox" id="showNine" checked> Nine-Point Circle</label>
        <label class="label"><input type="checkbox" id="showEuler" checked> Euler Line</label>
    </div>
    <canvas id="canvas" width="700" height="500"></canvas>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        // Initial Triangle Vertices
        let pts = [
            {x: 350, y: 100, label: 'A'},
            {x: 150, y: 400, label: 'B'},
            {x: 600, y: 400, label: 'C'}
        ];

        // Interaction logic
        let dragging = null;

        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;
            for (let p of pts) {
                if (Math.hypot(p.x - mx, p.y - my) < 15) {
                    dragging = p;
                    return;
                }
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!dragging) return;
            const rect = canvas.getBoundingClientRect();
            dragging.x = e.clientX - rect.left;
            dragging.y = e.clientY - rect.top;
            draw();
        });

        canvas.addEventListener('mouseup', () => { dragging = null; });
        canvas.addEventListener('mouseleave', () => { dragging = null; });

        // Checkbox listeners
        document.getElementById('showCircum').addEventListener('change', draw);
        document.getElementById('showNine').addEventListener('change', draw);
        document.getElementById('showEuler').addEventListener('change', draw);

        // Math functions
        function getCircumcenter(A, B, C) {
            let D = 2 * (A.x * (B.y - C.y) + B.x * (C.y - A.y) + C.x * (A.y - B.y));
            if (Math.abs(D) < 0.001) return null; // Collinear
            let Ux = ((A.x**2 + A.y**2) * (B.y - C.y) + (B.x**2 + B.y**2) * (C.y - A.y) + (C.x**2 + C.y**2) * (A.y - B.y)) / D;
            let Uy = ((A.x**2 + A.y**2) * (C.x - B.x) + (B.x**2 + B.y**2) * (A.x - C.x) + (C.x**2 + C.y**2) * (B.x - A.x)) / D;
            return {x: Ux, y: Uy};
        }

        // Main Drawing Loop
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const A = pts[0], B = pts[1], C = pts[2];

            // Calculate Centers
            const O = getCircumcenter(A, B, C);
            if (!O) {
                ctx.fillStyle = "red";
                ctx.fillText("Vertices are collinear!", 20, 30);
                return;
            }
            
            const G = {x: (A.x + B.x + C.x) / 3, y: (A.y + B.y + C.y) / 3};
            const H = {x: 3*G.x - 2*O.x, y: 3*G.y - 2*O.y};
            const N = {x: (O.x + H.x) / 2, y: (O.y + H.y) / 2};
            
            const R = Math.hypot(O.x - A.x, O.y - A.y);
            const Rn = R / 2;

            // Get UI states
            const showCircum = document.getElementById('showCircum').checked;
            const showNine = document.getElementById('showNine').checked;
            const showEuler = document.getElementById('showEuler').checked;

            // Draw Triangle
            ctx.beginPath();
            ctx.moveTo(A.x, A.y); ctx.lineTo(B.x, B.y); ctx.lineTo(C.x, C.y); ctx.closePath();
            ctx.strokeStyle = "black"; ctx.lineWidth = 2; ctx.stroke();

            // Draw Circumcircle
            if (showCircum) {
                ctx.beginPath(); ctx.arc(O.x, O.y, R, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(0, 0, 255, 0.4)"; ctx.setLineDash([5, 5]); ctx.stroke(); ctx.setLineDash([]);
            }

            // Draw Nine-Point Circle
            if (showNine) {
                ctx.beginPath(); ctx.arc(N.x, N.y, Rn, 0, Math.PI*2);
                ctx.strokeStyle = "rgba(128, 0, 128, 0.8)"; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;
            }

            // Draw Euler Line (extended past O and H slightly)
            if (showEuler) {
                ctx.beginPath(); 
                // Draw a long line through O and H
                let dx = H.x - O.x, dy = H.y - O.y;
                ctx.moveTo(O.x - dx*2, O.y - dy*2); ctx.lineTo(H.x + dx*2, H.y + dy*2);
                ctx.strokeStyle = "rgba(255, 165, 0, 0.6)"; ctx.lineWidth = 3; ctx.stroke(); ctx.lineWidth = 1;
            }

            // Helper to draw points
            function drawPoint(p, color, label) {
                ctx.beginPath(); ctx.arc(p.x, p.y, 5, 0, Math.PI*2);
                ctx.fillStyle = color; ctx.fill();
                ctx.fillStyle = "black"; ctx.font = "14px Arial";
                ctx.fillText(label, p.x + 8, p.y - 8);
            }

            drawPoint(O, "blue", "O");
            drawPoint(G, "green", "G");
            drawPoint(H, "red", "H");
            drawPoint(N, "purple", "N");

            // Draw interactive vertices
            for (let p of pts) {
                ctx.beginPath(); ctx.arc(p.x, p.y, 8, 0, Math.PI*2);
                ctx.fillStyle = dragging === p ? "#ffcc00" : "#333";
                ctx.fill();
                ctx.fillStyle = "black"; ctx.font = "bold 16px Arial";
                ctx.fillText(p.label, p.x - 5, p.y - 12);
            }
        }

        draw(); // Initial call
    </script>
</body>
</html>
"""

components.html(html_code, height=600)
