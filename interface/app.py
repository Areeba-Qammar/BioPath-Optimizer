import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from core.optimizer import BioPathOptimizerFast

st.set_page_config(page_title="BioPath Optimizer", page_icon="🍃", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    .bio-box { background: #1a2e1a; border-left: 4px solid #00cc88;
               padding: 12px 16px; border-radius: 6px; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🍃 BioPath Optimizer")
st.markdown("### Nature-Inspired Logistics for Carbon-Neutral Deliveries")

st.markdown("""
<div class="bio-box">
<strong>🐜 Biomimicry Principle:</strong> Ant colonies find the shortest food paths using pheromone trails —
stronger trails attract more ants, weaker ones fade. BioPath applies this exact mechanism
(Ant Colony Optimization) to minimize fuel cost across delivery networks.
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Simulation Config")
    cities_count = st.slider("Total Cities", 5, 25, 12)
    ants_count = st.slider("Ant Population", 10, 50, 20)
    iter_count = st.slider("Generations", 20, 200, 50)
    alpha_val = st.slider("Pheromone Weight (α)", 0.5, 3.0, 1.0, 0.1)
    beta_val = st.slider("Heuristic Weight (β)", 0.5, 5.0, 2.0, 0.1)

    st.markdown("---")
    st.markdown("**How to read results:**")
    st.markdown("- Lower fuel cost = better route")
    st.markdown("- Watch convergence chart flatten = algorithm found optimal path")
    st.markdown("- Green line = ant's optimized route")

    if st.button("🔄 Regenerate Map"):
        for key in ['cities', 'dist_matrix', 'best_path', 'best_cost', 'history']:
            st.session_state.pop(key, None)
        st.rerun()

# Data Generation
if 'cities' not in st.session_state or len(st.session_state.cities) != cities_count:
    st.session_state.cities = np.random.rand(cities_count, 2) * 100
    dist = np.linalg.norm(
        st.session_state.cities[:, None] - st.session_state.cities, axis=2
    )
    st.session_state.dist_matrix = dist
    st.session_state.pop('best_path', None)
    st.session_state.pop('best_cost', None)
    st.session_state.pop('history', None)

# Run button
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("#### Run Optimization")
    if st.button("▶ Run Bio-Optimization", type="primary"):
        optimizer = BioPathOptimizerFast(
            st.session_state.dist_matrix,
            ants_count,
            iter_count,
            alpha=alpha_val,
            beta=beta_val
        )

        progress = st.progress(0)
        status = st.empty()
        history = []

        def update_progress(i, cost):
            history.append(cost)
            progress.progress((i + 1) / iter_count)
            status.metric("Current Best Fuel Cost", f"{cost:.2f} km")

        best_path, best_cost = optimizer.optimize(update_progress)
        st.session_state.best_path = best_path
        st.session_state.best_cost = best_cost
        st.session_state.history = history
        st.rerun()

    # Metrics panel
    if 'best_cost' in st.session_state:
        st.markdown("---")
        st.metric("✅ Best Route Cost", f"{st.session_state.best_cost:.2f} km")
        naive_cost = st.session_state.dist_matrix.sum() / cities_count
        improvement = ((naive_cost - st.session_state.best_cost) / naive_cost) * 100
        st.metric("📉 vs. Random Route", f"{abs(improvement):.1f}% better")
        st.metric("🐜 Ants Used", f"{ants_count}")
        st.metric("🔁 Generations", f"{iter_count}")

        st.markdown("---")
        st.markdown("**Optimal Visit Order:**")
        path = st.session_state.best_path
        route_str = " → ".join([f"C{i}" for i in path]) + f" → C{path[0]}"
        st.code(route_str)

with col2:
    if 'best_path' in st.session_state:
        coords = st.session_state.cities
        path = st.session_state.best_path

        # --- Route map ---
        fig = go.Figure()

        # Draw all edges faintly
        for i in range(cities_count):
            for j in range(i + 1, cities_count):
                fig.add_trace(go.Scatter(
                    x=[coords[i, 0], coords[j, 0]],
                    y=[coords[i, 1], coords[j, 1]],
                    mode='lines',
                    line=dict(color='rgba(100,100,100,0.15)', width=1),
                    hoverinfo='none', showlegend=False
                ))

        # Draw optimized route
        px = [coords[i, 0] for i in path] + [coords[path[0], 0]]
        py = [coords[i, 1] for i in path] + [coords[path[0], 1]]
        fig.add_trace(go.Scatter(
            x=px, y=py, mode='lines+markers',
            line=dict(color='#00FFCC', width=3),
            marker=dict(size=12, color='white', line=dict(color='#00FFCC', width=2)),
            name='Optimized Route'
        ))

        # City labels
        fig.add_trace(go.Scatter(
            x=coords[:, 0], y=coords[:, 1],
            mode='text',
            text=[f'C{i}' for i in range(cities_count)],
            textposition='top center',
            textfont=dict(color='#aaffcc', size=11),
            showlegend=False
        ))

        fig.update_layout(
            template="plotly_dark",
            title="🗺️ Optimized Delivery Network",
            xaxis_visible=False, yaxis_visible=False,
            height=420,
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- Convergence chart ---
        if 'history' in st.session_state and st.session_state.history:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                y=st.session_state.history,
                mode='lines',
                line=dict(color='#00FFCC', width=2),
                fill='tozeroy',
                fillcolor='rgba(0,255,204,0.08)',
                name='Best Cost per Generation'
            ))
            fig2.update_layout(
                template="plotly_dark",
                title="📉 Convergence — Ant Colony Learning Over Time",
                xaxis_title="Generation",
                yaxis_title="Fuel Cost (km)",
                height=250,
                margin=dict(t=40, b=30, l=40, r=10)
            )
            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("🐜 Adjust the settings on the left and click **▶ Run Bio-Optimization** to start.")
        # Show empty city scatter as preview
        coords = st.session_state.cities
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=coords[:, 0], y=coords[:, 1],
            mode='markers+text',
            marker=dict(size=12, color='#00FFCC',
                        line=dict(color='white', width=1)),
            text=[f'C{i}' for i in range(cities_count)],
            textposition='top center',
            textfont=dict(color='#aaffcc', size=11),
            name='Cities'
        ))
        fig.update_layout(
            template="plotly_dark",
            title="🗺️ City Map (not yet optimized)",
            xaxis_visible=False, yaxis_visible=False,
            height=420
        )
        st.plotly_chart(fig, use_container_width=True)
