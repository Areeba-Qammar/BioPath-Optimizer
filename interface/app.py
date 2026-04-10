import streamlit as st
import numpy as np
import plotly.graph_objects as go
from core.optimizer import BioPathOptimizerFast

st.set_page_config(page_title="BioPath Optimizer", page_icon="🍃", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍃 BioPath Optimizer")
st.markdown("### Nature-Inspired Logistics for Carbon-Neutral Deliveries")

# Layout: Sidebar for controls, main area for visuals
with st.sidebar:
    st.header("Simulation Config")
    cities_count = st.slider("Total Cities", 5, 25, 12)
    ants_count = st.slider("Ant Population", 10, 50, 20)
    iter_count = st.slider("Generations", 20, 200, 50)
    
    if st.button("Regenerate Map"):
        st.rerun()

# Data Generation
if 'cities' not in st.session_state or len(st.session_state.cities) != cities_count:
    st.session_state.cities = np.random.rand(cities_count, 2) * 100
    dist = np.linalg.norm(st.session_state.cities[:, None] - st.session_state.cities, axis=2)
    st.session_state.dist_matrix = dist

# Execution
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Run Bio-Optimization", type="primary"):
        optimizer = BioPathOptimizerFast(st.session_state.dist_matrix, ants_count, iter_count)
        
        progress = st.progress(0)
        status = st.empty()
        
        def update_progress(i, cost):
            progress.progress((i + 1) / iter_count)
            status.metric("Current Best Fuel", f"{cost:.2f}L")

        best_path, best_cost = optimizer.optimize(update_progress)
        st.session_state.best_path = best_path
        st.session_state.best_cost = best_cost

with col2:
    if 'best_path' in st.session_state:
        # Build the Map Visualization
        fig = go.Figure()
        coords = st.session_state.cities
        path = st.session_state.best_path
        
        # Draw the connections
        px = [coords[i, 0] for i in path] + [coords[path[0], 0]]
        py = [coords[i, 1] for i in path] + [coords[path[0], 1]]
        
        fig.add_trace(go.Scatter(x=px, y=py, mode='lines+markers', 
                                 line=dict(color='#00FFCC', width=3),
                                 marker=dict(size=10, color='white')))
        
        fig.update_layout(template="plotly_dark", title="Optimized Logistics Network",
                          xaxis_visible=False, yaxis_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Adjust the settings and click 'Run' to visualize the optimization.")
