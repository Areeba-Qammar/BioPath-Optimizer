import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
# This line connects the UI to the math in your 'core' folder
from core.optimizer import BioPathOptimizerFast

def main():
    st.set_page_config(page_title="BioPath Optimizer", layout="wide")
    
    # Simple, humanized header
    st.title("🐜 BioPath: Nature-Inspired Route Planning")
    st.markdown("### Optimizing delivery routes to minimize fuel and carbon emissions.")

    # Sidebar for Algorithm Parameters
    with st.sidebar:
        st.header("⚙️ Settings")
        num_cities = st.slider("Number of Cities", 5, 20, 10)
        num_ants = st.slider("Number of Ants", 10, 100, 30)
        iterations = st.slider("Iterations", 50, 500, 150)
        
        st.info("Higher 'Alpha' makes ants follow trails, while 'Beta' makes them focus on short distances.")
        alpha = st.slider("Pheromone Importance (α)", 0.5, 3.0, 1.0)
        beta = st.slider("Distance Importance (β)", 0.5, 3.0, 2.0)

    # Generate random city positions for the demo
    if 'positions' not in st.session_state or st.button("🔄 Regenerate Cities"):
        st.session_state.positions = np.random.rand(num_cities, 2) * 100
        # Create a fuel matrix based on distances
        pos = st.session_state.positions
        dist_matrix = np.linalg.norm(pos[:, np.newaxis] - pos[np.newaxis, :], axis=2)
        st.session_state.fuel_matrix = dist_matrix * (1 + np.random.uniform(-0.1, 0.1, size=dist_matrix.shape))

    if st.button("🚀 Run Optimization", type="primary", use_container_width=True):
        optimizer = BioPathOptimizerFast(
            st.session_state.fuel_matrix, num_ants, iterations, alpha, beta
        )
        
        # UI Placeholders for live updates
        progress_bar = st.progress(0)
        status_text = st.empty()
        chart_container = st.empty()

        # Run the logic with a callback for the progress bar
        def update_ui(i, cost):
            progress_bar.progress((i + 1) / iterations)
            status_text.text(f"Iteration {i+1}/{iterations} - Current Best Cost: {cost:.2f
