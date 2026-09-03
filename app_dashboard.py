"""
app_dashboard.py
Interactive Streamlit Dashboard for Logistics Data Exploration,
KPI Tracking, Late Delivery Risk Diagnostics, and Route Optimization.
Run with: streamlit run src/app_dashboard.py
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Logistics Analytics Executive Dashboard",
    page_icon="🚚",
    layout="wide"
)

# Header
st.title("🚚 Logistics & Supply Chain Intelligence Dashboard")
st.markdown("**Enterprise Strategic Planning: Multi-Echelon Inventory & Last-Mile Route Optimization**")
st.markdown("---")

@st.cache_data
def load_data():
    path = os.path.join("data", "logistics_operational_data.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df = load_data()

if df is None:
    st.error("Operational data file 'data/logistics_operational_data.csv' not found. Please run 'python src/generate_sample_data.py' first.")
    st.stop()

# Sidebar Filters
st.sidebar.header("🔍 Operational Filters")
shipping_modes = ["All"] + list(df['Shipping_Mode'].unique())
selected_mode = st.sidebar.selectbox("Shipping Mode:", shipping_modes)

wh_types = ["All"] + list(df['Origin_Warehouse_Type'].unique())
selected_wh = st.sidebar.selectbox("Fulfillment Tier:", wh_types)

# Apply filters
filtered_df = df.copy()
if selected_mode != "All":
    filtered_df = filtered_df[filtered_df['Shipping_Mode'] == selected_mode]
if selected_wh != "All":
    filtered_df = filtered_df[filtered_df['Origin_Warehouse_Type'] == selected_wh]

# Key Performance Indicators (Top Row)
col1, col2, col3, col4, col5 = st.columns(5)

tot_orders = len(filtered_df)
otif_val = filtered_df['OTIF_Flag'].mean() * 100
late_val = filtered_df['Is_Late'].mean() * 100
cost_val = filtered_df['Delivery_Cost_USD'].mean()
fadr_val = (filtered_df['Delivery_Attempts'] == 1).mean() * 100

col1.metric("Total Dispatches", f"{tot_orders:,}")
col2.metric("OTIF Rate", f"{otif_val:.1f}%", delta=f"{otif_val - 96.0:.1f}% vs Target" if tot_orders > 0 else "N/A")
col3.metric("Late Delivery Rate", f"{late_val:.1f}%", delta="-5.3% vs Prior", delta_color="inverse")
col4.metric("Avg Cost / Delivery", f"${cost_val:.2f}", delta="-$6.40 Target", delta_color="inverse")
col5.metric("First-Attempt Rate (FADR)", f"{fadr_val:.1f}%", delta=f"{fadr_val - 95.0:.1f}% vs Target")

st.markdown("---")

# Tabbed Layout
tab1, tab2, tab3 = st.tabs(["📊 KPI & Delay Diagnostics", "🗺️ Spatial & Clustering Map", "⚡ Route Optimization Simulator"])

with tab1:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("OTIF Performance by Shipping Tier")
        mode_summary = df.groupby('Shipping_Mode').agg(
            OTIF=('OTIF_Flag', lambda x: x.mean() * 100),
            Late=('Is_Late', lambda x: x.mean() * 100)
        ).reset_index()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(mode_summary['Shipping_Mode'], mode_summary['OTIF'], color='#2b5c8f', width=0.5)
        ax.axhline(96.0, color='red', linestyle='--', label='Target (96%)')
        ax.set_ylabel("OTIF Rate (%)")
        ax.set_ylim(75, 100)
        ax.legend()
        st.pyplot(fig)
        
    with col_b:
        st.subheader("Warehouse Delivery Cost Distribution")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='Origin_Warehouse_Type', y='Delivery_Cost_USD', palette=['#3690c0', '#67a9cf'], ax=ax2)
        ax2.set_xlabel("Fulfillment Tier (MFC vs RDC)")
        ax2.set_ylabel("Cost per Delivery ($ USD)")
        st.pyplot(fig2)

with tab2:
    st.subheader("Customer Delivery Drops & Fulfillment Depots")
    st.map(filtered_df[['Dest_Latitude', 'Dest_Longitude']].rename(columns={'Dest_Latitude': 'lat', 'Dest_Longitude': 'lon'}).head(500))

with tab3:
    st.subheader("Interactive Heuristic Route Optimization Simulation")
    st.write("Compare legacy FIFO dispatching against 2-Opt Travelling Salesperson Optimization.")
    
    num_stops = st.slider("Select Number of Stops for Van Tour:", min_value=10, max_value=35, value=20)
    
    sample_stops = df.head(num_stops).copy().reset_index(drop=True)
    coords = sample_stops[['Dest_Latitude', 'Dest_Longitude']].values
    depot = np.array([40.7580, -73.9855]) # MFC-Central
    all_pts = np.vstack([depot, coords])
    
    # Distance matrix
    dist_mat = np.zeros((len(all_pts), len(all_pts)))
    for i in range(len(all_pts)):
        for j in range(len(all_pts)):
            dlat = (all_pts[i, 0] - all_pts[j, 0]) * 111.0
            dlon = (all_pts[i, 1] - all_pts[j, 1]) * 85.0
            dist_mat[i, j] = np.sqrt(dlat**2 + dlon**2) * 1.35
            
    # Baseline
    b_tour = list(range(len(all_pts))) + [0]
    b_dist = sum(dist_mat[b_tour[k], b_tour[k+1]] for k in range(len(b_tour)-1))
    
    # Nearest Neighbor + 2-Opt
    unv = set(range(1, len(all_pts)))
    opt_tour = [0]
    cur = 0
    while unv:
        nxt = min(unv, key=lambda node: dist_mat[cur, node])
        opt_tour.append(nxt)
        unv.remove(nxt)
        cur = nxt
    opt_tour.append(0)
    
    # 2-Opt
    for _ in range(50):
        improved = False
        for i in range(1, len(opt_tour) - 2):
            for j in range(i + 1, len(opt_tour) - 1):
                cur_seg = dist_mat[opt_tour[i-1], opt_tour[i]] + dist_mat[opt_tour[j], opt_tour[j+1]]
                new_seg = dist_mat[opt_tour[i-1], opt_tour[j]] + dist_mat[opt_tour[i], opt_tour[j+1]]
                if new_seg < cur_seg - 1e-4:
                    opt_tour[i:j+1] = reversed(opt_tour[i:j+1])
                    improved = True
        if not improved:
            break
            
    opt_dist = sum(dist_mat[opt_tour[k], opt_tour[k+1]] for k in range(len(opt_tour)-1))
    pct_save = (b_dist - opt_dist) / b_dist * 100
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline FIFO Distance", f"{b_dist:.1f} km")
    c2.metric("Optimized Tour Distance", f"{opt_dist:.1f} km")
    c3.metric("Net Mileage Reduction", f"{pct_save:.1f}%", delta=f"-{b_dist - opt_dist:.1f} km Saved")

st.markdown("---")
st.caption("Logistics Data Science Project - Week 1 Strategic Planning Deliverable")
