import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(layout="wide", page_title="Advanced Solar System", page_icon="🪐")

# CSS to force a dark background for the true 'Space' feel
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: white; }
    .css-1d391kg { background-color: #0e1117; }
</style>
""", unsafe_allow_html=True)

system_data = {
    "Sun": {
        "type": "Star", "radius": 8, "dist": 0, "speed": 0, "color": "#FDB813",
        "texture": "Sun", "real_stats": {"Mass": "1.989 × 10^30 kg", "Temp": "5,500°C", "Diameter": "1.4M km"}
    },
    "Mercury": {
        "type": "Planet", "radius": 1.5, "dist": 14, "speed": 4.1, "color": "#A5A5A5",
        "real_stats": {"Mass": "3.285 × 10^23 kg", "Orbit Period": "88 days", "Moons": 0}
    },
    "Venus": {
        "type": "Planet", "radius": 3, "dist": 22, "speed": 1.6, "color": "#E3BB76",
        "real_stats": {"Mass": "4.867 × 10^24 kg", "Orbit Period": "225 days", "Moons": 0}
    },
    "Earth": {
        "type": "Planet", "radius": 3.2, "dist": 32, "speed": 1.0, "color": "#22A6B3",
        "real_stats": {"Mass": "5.972 × 10^24 kg", "Orbit Period": "365 days", "Moons": 1},
        "moons": [{"name": "Moon", "dist": 5, "speed": 12, "size": 0.8, "color": "#DDDDDD"}]
    },
    "Mars": {
        "type": "Planet", "radius": 2.8, "dist": 42, "speed": 0.53, "color": "#EB4D4B",
        "real_stats": {"Mass": "6.39 × 10^23 kg", "Orbit Period": "687 days", "Moons": 2},
        "moons": [{"name": "Phobos", "dist": 4, "speed": 15, "size": 0.4, "color": "#999999"}]
    },
    "Jupiter": {
        "type": "Gas Giant", "radius": 7, "dist": 70, "speed": 0.08, "color": "#D3A97C",
        "real_stats": {"Mass": "1.898 × 10^27 kg", "Orbit Period": "12 years", "Moons": 79},
        "moons": [{"name": "Io", "dist": 9, "speed": 8, "size": 1, "color": "#F4E06D"}, 
                  {"name": "Europa", "dist": 11, "speed": 6, "size": 0.9, "color": "#C4C9CE"}]
    },
    "Saturn": {
        "type": "Gas Giant", "radius": 6, "dist": 95, "speed": 0.03, "color": "#E0C898",
        "has_rings": True,
        "real_stats": {"Mass": "5.683 × 10^26 kg", "Orbit Period": "29 years", "Moons": 82},
        "moons": [{"name": "Titan", "dist": 10, "speed": 5, "size": 1.2, "color": "#D4AC4E"}]
    },
    "Uranus": {
        "type": "Ice Giant", "radius": 5, "dist": 120, "speed": 0.01, "color": "#7DE3F4",
        "real_stats": {"Mass": "8.681 × 10^25 kg", "Orbit Period": "84 years", "Moons": 27}
    },
    "Neptune": {
        "type": "Ice Giant", "radius": 4.8, "dist": 140, "speed": 0.006, "color": "#3C40C6",
        "real_stats": {"Mass": "1.024 × 10^26 kg", "Orbit Period": "165 years", "Moons": 14}
    }
}

def get_sphere_mesh(size, center_x, center_y, center_z, color):
    """Creates a 3D sphere mesh at a specific coordinate"""
    theta = np.linspace(0, 2 * np.pi, 20)
    phi = np.linspace(0, np.pi, 20)
    x = center_x + size * np.outer(np.cos(theta), np.sin(phi))
    y = center_y + size * np.outer(np.sin(theta), np.sin(phi))
    z = center_z + size * np.outer(np.ones(20), np.cos(phi))
    return x, y, z

def create_orbit_trace(dist, color="white"):
    """Creates the orbital ring lines"""
    theta = np.linspace(0, 2 * np.pi, 100)
    x = dist * np.cos(theta)
    y = dist * np.sin(theta)
    z = np.zeros_like(x)
    return go.Scatter3d(
        x=x, y=y, z=z, mode='lines', 
        line=dict(color=color, width=1), 
        hoverinfo='none', showlegend=False
    )

def create_asteroid_belt(num_asteroids=300):
    """Generates random debris between Mars and Jupiter"""
    r = np.random.uniform(50, 60, num_asteroids)  # Between Mars(42) and Jupiter(70)
    theta = np.random.uniform(0, 2*np.pi, num_asteroids)
    
    # Add some randomness to height (z-axis)
    z = np.random.uniform(-1, 1, num_asteroids)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    return go.Scatter3d(
        x=x, y=y, z=z, mode='markers',
        marker=dict(size=1.5, color='gray', opacity=0.6),
        name='Asteroid Belt', hoverinfo='none'
    )

def create_starfield(num_stars=500):
    """Generates distant background stars"""
    r = np.random.uniform(200, 300, num_stars)
    theta = np.random.uniform(0, 2*np.pi, num_stars)
    phi = np.random.uniform(0, np.pi, num_stars)
    
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    
    return go.Scatter3d(
        x=x, y=y, z=z, mode='markers',
        marker=dict(size=2, color='white', opacity=0.8),
        hoverinfo='none', showlegend=False
    )

# Sidebar Controls
st.sidebar.title("🚀 Flight Control")
time_value = st.sidebar.slider("Time (Earth Years)", 0.0, 100.0, 0.0, 0.5)
show_orbits = st.sidebar.checkbox("Show Orbits", True)
show_asteroids = st.sidebar.checkbox("Show Asteroid Belt", True)

# Data Panel
st.sidebar.markdown("---")
st.sidebar.subheader("🔭 Data Analyzer")
selected_planet = st.sidebar.selectbox("Inspect Celestial Body", list(system_data.keys()))
p_data = system_data[selected_planet]
st.sidebar.markdown(f"### {selected_planet}")
st.sidebar.caption(p_data['type'])
for k, v in p_data['real_stats'].items():
    st.sidebar.text(f"{k}: {v}")

fig = go.Figure()

# 1. Add Starfield
fig.add_trace(create_starfield())

# 2. Add Asteroid Belt
if show_asteroids:
    fig.add_trace(create_asteroid_belt())

# 3. Add Planets, Sun, and Moons
for name, body in system_data.items():
    # Calculate Planet Position
    angle = body['speed'] * time_value
    px = body['dist'] * np.cos(angle)
    py = body['dist'] * np.sin(angle)
    pz = 0
    
    # Draw Orbit
    if show_orbits and body['dist'] > 0:
        fig.add_trace(create_orbit_trace(body['dist']))
    
    # Draw Planet Sphere
    x, y, z = get_sphere_mesh(body['radius'], px, py, pz, body['color'])
    fig.add_trace(go.Surface(
        x=x, y=y, z=z, 
        colorscale=[[0, body['color']], [1, body['color']]], 
        showscale=False, opacity=1.0, name=name,
        hovertemplate=f"<b>{name}</b><br>Type: {body['type']}<extra></extra>"
    ))
    
    # Draw Saturn's Rings (Special Case)
    if 'has_rings' in body:
        # Create a flat donut using Scatter3d points or surface
        # Simplified as a filled circle trace slightly larger than planet
        ring_theta = np.linspace(0, 2*np.pi, 50)
        ring_r_inner = body['radius'] * 1.4
        ring_r_outer = body['radius'] * 2.2
        
        # We draw multiple lines to simulate a solid ring
        for r_ring in np.linspace(ring_r_inner, ring_r_outer, 6):
            rx = px + r_ring * np.cos(ring_theta)
            ry = py + r_ring * np.sin(ring_theta)
            fig.add_trace(go.Scatter3d(
                x=rx, y=ry, z=np.zeros_like(rx), mode='lines',
                line=dict(color='#A39276', width=2), showlegend=False, hoverinfo='skip'
            ))

    # Draw Moons (Hierarchical Orbit)
    if 'moons' in body:
        for moon in body['moons']:
            # Moon position relative to Planet
            m_angle = moon['speed'] * time_value * 5 # Moons move faster
            mx = px + moon['dist'] * np.cos(m_angle)
            my = py + moon['dist'] * np.sin(m_angle)
            mz = 0 + (moon['dist'] * 0.3) * np.sin(m_angle) # Slight tilt
            
            # Moon Sphere
            mx_surf, my_surf, mz_surf = get_sphere_mesh(moon['size'], mx, my, mz, moon['color'])
            fig.add_trace(go.Surface(
                x=mx_surf, y=my_surf, z=mz_surf,
                colorscale=[[0, moon['color']], [1, moon['color']]],
                showscale=False, name=moon['name']
            ))

# 4. Camera & Scene Config
fig.update_layout(
    title="Interactive Solar System Simulation",
    width=1000, height=800,
    scene=dict(
        xaxis=dict(visible=False, range=[-150, 150]),
        yaxis=dict(visible=False, range=[-150, 150]),
        zaxis=dict(visible=False, range=[-100, 100]),
        aspectratio=dict(x=1, y=1, z=0.6),
        bgcolor='#0e1117' # Matches Streamlit Dark Mode
    ),
    paper_bgcolor='#0e1117',
    margin=dict(l=0, r=0, b=0, t=40),
    showlegend=False
)

# Render
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("### 📝 Notes")
st.markdown("""
* **Scale:** Distances and sizes are **logarithmically scaled**. If real scales were used, the planets would be microscopic dots compared to the orbit distances.
* **Time:** Use the slider in the sidebar to move the planets forward in time.
* **Interaction:** You can **Zoom**, **Pan**, and **Rotate** the 3D model with your mouse.

""")
