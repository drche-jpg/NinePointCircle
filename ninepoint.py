import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- MATH HELPER FUNCTIONS ---
def get_triangle_centers(A, B, C):
    Ax, Ay = A; Bx, By = B; Cx, Cy = C
    
    # 1. Centroid (G) - Average of vertices
    Gx, Gy = (Ax + Bx + Cx) / 3, (Ay + By + Cy) / 3
    
    # 2. Circumcenter (O) - Intersection of perpendicular bisectors
    D = 2 * (Ax * (By - Cy) + Bx * (Cy - Ay) + Cx * (Ay - By))
    if D == 0: 
        return None # Vertices are collinear (not a triangle)
    
    Ox = ((Ax**2 + Ay**2)*(By - Cy) + (Bx**2 + By**2)*(Cy - Ay) + (Cx**2 + Cy**2)*(Ay - By)) / D
    Oy = ((Ax**2 + Ay**2)*(Cx - Bx) + (Bx**2 + By**2)*(Ax - Cx) + (Cx**2 + Cy**2)*(Bx - Ax)) / D
    
    # 3. Orthocenter (H) - Using the Euler Line property: H = 3G - 2O
    Hx, Hy = 3 * Gx - 2 * Ox, 3 * Gy - 2 * Oy
    
    # 4. Nine-Point Center (N) - Midpoint of O and H
    Nx, Ny = (Ox + Hx) / 2, (Oy + Hy) / 2
    
    # Radii
    circumradius = np.sqrt((Ax - Ox)**2 + (Ay - Oy)**2)
    nine_point_radius = circumradius / 2
    
    return (Gx, Gy), (Ox, Oy), (Hx, Hy), (Nx, Ny), circumradius, nine_point_radius

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
st.write("Adjust the coordinates of the triangle vertices below to see the Euler line and Nine-Point Circle dynamically recalculate.")

# --- INTERACTIVE CONTROLS ---
ctrl_col, plot_col = st.columns([1, 3])

with ctrl_col:
    st.subheader("Vertex A")
    ax = st.slider("A (x)", 0, 10, 5)
    ay = st.slider("A (y)", 0, 10, 9)
    
    st.subheader("Vertex B")
    bx = st.slider("B (x)", 0, 10, 1)
    by = st.slider("B (y)", 0, 10, 1)
    
    st.subheader("Vertex C")
    cx = st.slider("C (x)", 0, 10, 9)
    cy = st.slider("C (y)", 0, 10, 2)
    
    show_circumcircle = st.checkbox("Show Circumcircle", True)
    show_ninepoint = st.checkbox("Show Nine-Point Circle", True)
    show_euler = st.checkbox("Show Euler Line", True)

# --- PLOTTING ---
A, B, C = (ax, ay), (bx, by), (cx, cy)
centers = get_triangle_centers(A, B, C)

with plot_col:
    if not centers:
        st.error("Vertices are collinear! Please move them to form a triangle.")
    else:
        G, O, H, N, R, Rn = centers
        
        fig = go.Figure()
        
        # Draw Triangle
        fig.add_trace(go.Scatter(x=[ax, bx, cx, ax], y=[ay, by, cy, ay], 
                                 mode='lines+markers+text', text=["A", "B", "C", ""], 
                                 textposition="top center", name="Triangle",
                                 line=dict(color='black', width=3), marker=dict(size=8)))
        
        # Draw Centers
        centers_x = [O[0], G[0], H[0], N[0]]
        centers_y = [O[1], G[1], H[1], N[1]]
        labels = ["O (Circumcenter)", "G (Centroid)", "H (Orthocenter)", "N (9-Point Center)"]
        
        fig.add_trace(go.Scatter(x=centers_x, y=centers_y, mode='markers+text',
                                 text=["O", "G", "H", "N"], textposition="bottom right",
                                 marker=dict(color=['blue', 'green', 'red', 'purple'], size=10),
                                 name="Centers", textfont=dict(size=14, color="black")))
        
        # Draw Euler Line
        if show_euler:
            fig.add_trace(go.Scatter(x=[O[0], H[0]], y=[O[1], H[1]], mode='lines',
                                     line=dict(color='orange', width=2, dash='dash'), name="Euler Line"))
            
        # Helper function to generate circle points
        def make_circle(center_x, center_y, radius):
            theta = np.linspace(0, 2*np.pi, 100)
            return center_x + radius*np.cos(theta), center_y + radius*np.sin(theta)

        # Draw Circumcircle
        if show_circumcircle:
            cx_pts, cy_pts = make_circle(O[0], O[1], R)
            fig.add_trace(go.Scatter(x=cx_pts, y=cy_pts, mode='lines', 
                                     line=dict(color='blue', width=1, dash='dot'), name="Circumcircle"))
            
        # Draw Nine-Point Circle
        if show_ninepoint:
            nx_pts, ny_pts = make_circle(N[0], N[1], Rn)
            fig.add_trace(go.Scatter(x=nx_pts, y=ny_pts, mode='lines',
                                     line=dict(color='purple', width=2), name="Nine-Point Circle"))

        # Formatting
        fig.update_layout(
            xaxis=dict(range=[-2, 12], scaleanchor="y", scaleratio=1), 
            yaxis=dict(range=[-2, 12]),
            height=600, margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        st.plotly_chart(fig, use_container_width=True)