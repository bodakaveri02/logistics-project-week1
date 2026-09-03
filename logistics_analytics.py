"""
logistics_analytics.py
Performs end-to-end data exploration, KPI evaluation, machine learning
predictive modeling for delivery delays, spatial clustering for dispatch zones,
and route optimization simulation. Exports high-resolution analytical figures.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.cluster import KMeans

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#eeeeee'
plt.rcParams['grid.linestyle'] = '--'

def run_pipeline():
    os.makedirs('figures', exist_ok=True)
    data_path = os.path.join('data', 'logistics_operational_data.csv')
    df = pd.read_csv(data_path)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # ==========================================
    # 1. KPI Calculation & Exploratory Analysis
    # ==========================================
    otif_rate = df['OTIF_Flag'].mean() * 100
    late_rate = df['Is_Late'].mean() * 100
    avg_cost = df['Delivery_Cost_USD'].mean()
    median_cost = df['Delivery_Cost_USD'].median()
    avg_distance = df['Route_Distance_km'].mean()
    fadr = (df['Delivery_Attempts'] == 1).mean() * 100

    print("\n--- EXECUTIVE LOGISTICS KPIS ---")
    print(f"On-Time In-Full (OTIF) Rate: {otif_rate:.2f}% (Target >= 96.0%)")
    print(f"Late Delivery Rate: {late_rate:.2f}%")
    print(f"First-Attempt Delivery Rate (FADR): {fadr:.2f}% (Target >= 95.0%)")
    print(f"Average Delivery Cost: ${avg_cost:.2f} (Median: ${median_cost:.2f})")
    print(f"Average Route Distance: {avg_distance:.2f} km")

    # Breakdown by Shipping Mode
    mode_perf = df.groupby('Shipping_Mode').agg(
        Order_Count=('Order_ID', 'count'),
        OTIF_Rate=('OTIF_Flag', lambda x: x.mean() * 100),
        Late_Rate=('Is_Late', lambda x: x.mean() * 100),
        Avg_Cost=('Delivery_Cost_USD', 'mean'),
        Avg_Distance=('Route_Distance_km', 'mean')
    ).reset_index()
    print("\nPerformance by Shipping Mode:")
    print(mode_perf.to_string(index=False))

    # Breakdown by Warehouse Type
    wh_perf = df.groupby('Origin_Warehouse_Type').agg(
        Order_Count=('Order_ID', 'count'),
        OTIF_Rate=('OTIF_Flag', lambda x: x.mean() * 100),
        Late_Rate=('Is_Late', lambda x: x.mean() * 100),
        Avg_Cost=('Delivery_Cost_USD', 'mean'),
        Avg_Transit_Hours=('Actual_Transit_Hours', 'mean')
    ).reset_index()
    print("\nPerformance by Warehouse Type (RDC vs MFC):")
    print(wh_perf.to_string(index=False))

    # ==========================================
    # FIGURE 1: Comprehensive KPI Dashboard
    # ==========================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # Subplot 1: OTIF Rate by Shipping Mode
    colors_mode = ['#2b5c8f', '#3690c0', '#67a9cf']
    bars1 = axes[0, 0].bar(mode_perf['Shipping_Mode'], mode_perf['OTIF_Rate'], color=colors_mode, width=0.55, edgecolor='#1b3c5f', linewidth=1.2)
    axes[0, 0].axhline(96.0, color='#d95f02', linestyle='--', linewidth=1.8, label='Target OTIF Threshold (96%)')
    axes[0, 0].set_title('A. On-Time In-Full (OTIF) Rate by Shipping Mode', fontsize=12, fontweight='bold', pad=10)
    axes[0, 0].set_ylabel('OTIF Percentage (%)', fontsize=10, fontweight='bold')
    axes[0, 0].set_ylim(80, 100)
    axes[0, 0].legend(loc='lower right', frameon=True, facecolor='white')
    for bar in bars1:
        yval = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f"{yval:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Subplot 2: Late Delivery Rate by Warehouse Tier
    colors_wh = ['#41b6c4', '#253494']
    bars2 = axes[0, 1].bar(wh_perf['Origin_Warehouse_Type'], wh_perf['Late_Rate'], color=colors_wh, width=0.45, edgecolor='#1b2c4f', linewidth=1.2)
    axes[0, 1].set_title('B. Late Delivery Risk: RDC vs Urban MFC Hubs', fontsize=12, fontweight='bold', pad=10)
    axes[0, 1].set_ylabel('Late Delivery Rate (%)', fontsize=10, fontweight='bold')
    axes[0, 1].set_ylim(0, max(wh_perf['Late_Rate']) * 1.4)
    for bar in bars2:
        yval = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2.0, yval + 0.2, f"{yval:.2f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Subplot 3: Distribution of Delivery Cost
    sns.histplot(df['Delivery_Cost_USD'], bins=35, kde=True, ax=axes[1, 0], color='#2b5c8f', edgecolor='white', alpha=0.7)
    axes[1, 0].axvline(avg_cost, color='#e41a1c', linestyle='-', linewidth=2, label=f'Mean: ${avg_cost:.2f}')
    axes[1, 0].axvline(median_cost, color='#4daf4a', linestyle=':', linewidth=2, label=f'Median: ${median_cost:.2f}')
    axes[1, 0].set_title('C. Distribution of Last-Mile Delivery Cost ($ USD)', fontsize=12, fontweight='bold', pad=10)
    axes[1, 0].set_xlabel('Cost per Delivery ($ USD)', fontsize=10, fontweight='bold')
    axes[1, 0].set_ylabel('Order Frequency', fontsize=10, fontweight='bold')
    axes[1, 0].legend(loc='upper right', frameon=True, facecolor='white')

    # Subplot 4: Route Distance vs Transit Hours colored by Status
    scatter = axes[1, 1].scatter(
        df['Route_Distance_km'], df['Actual_Transit_Hours'],
        c=df['Is_Late'], cmap='coolwarm', alpha=0.55, edgecolors='none', s=24
    )
    axes[1, 1].set_title('D. Transit Duration vs Distance (Red = Late Deliveries)', fontsize=12, fontweight='bold', pad=10)
    axes[1, 1].set_xlabel('Route Road Distance (km)', fontsize=10, fontweight='bold')
    axes[1, 1].set_ylabel('Actual Transit Time (Hours)', fontsize=10, fontweight='bold')
    cbar = plt.colorbar(scatter, ax=axes[1, 1], ticks=[0, 1])
    cbar.ax.set_yticklabels(['On-Time', 'Late'])

    plt.tight_layout()
    fig1_path = os.path.join('figures', 'fig1_kpi_distribution.png')
    plt.savefig(fig1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved Figure 1 to {fig1_path}")

    # ==========================================
    # 2. Predictive Machine Learning Modeling
    # ==========================================
    # Feature engineering for delay classification
    feature_cols = [
        'Route_Distance_km', 'Direct_Distance_km', 'Traffic_Congestion_Index',
        'Weather_Severity_Index', 'Package_Weight_kg', 'Package_Volume_m3',
        'Driver_Experience_Years', 'Delivery_Attempts', 'Order_Value_USD', 'Promised_SLA_Hours'
    ]
    
    # Categorical encoding
    df_encoded = pd.get_dummies(df[feature_cols + ['Shipping_Mode', 'Origin_Warehouse_Type']], drop_first=True)
    X = df_encoded
    y = df['Is_Late']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

    # Train Random Forest with class weighting
    clf = RandomForestClassifier(n_estimators=150, max_depth=8, class_weight='balanced', random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)

    print("\n--- PREDICTIVE MODEL EVALUATION (RANDOM FOREST) ---")
    print(f"Accuracy:  {acc*100:.2f}%")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print(f"Precision: {prec*100:.2f}%")
    print(f"Recall:    {rec*100:.2f}%")
    print(f"F1-Score:  {f1*100:.2f}%")

    # Feature Importance
    importances = clf.feature_importances_
    feat_names = X.columns
    feat_imp = pd.DataFrame({'Feature': feat_names, 'Importance': importances}).sort_values('Importance', ascending=False)
    print("\nTop 8 Most Predictive Features for Late Delivery:")
    print(feat_imp.head(8).to_string(index=False))

    # ==========================================
    # FIGURE 2: Predictive Feature Importance
    # ==========================================
    plt.figure(figsize=(10, 6), dpi=300)
    top_feats = feat_imp.head(10).sort_values('Importance', ascending=True)
    bars = plt.barh(top_feats['Feature'], top_feats['Importance'], color='#2b5c8f', edgecolor='#1b3c5f', height=0.6)
    plt.title('Feature Importance: Key Drivers of Late Delivery Risk (Random Forest)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Gini Importance (Relative Predictive Power)', fontsize=11, fontweight='bold')
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.003, bar.get_y() + bar.get_height()/2.0, f"{w*100:.1f}%", va='center', fontsize=10, fontweight='bold', color='#111111')
    plt.xlim(0, max(top_feats['Importance']) * 1.15)
    plt.tight_layout()
    fig2_path = os.path.join('figures', 'fig2_feature_importance.png')
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved Figure 2 to {fig2_path}")

    # ==========================================
    # 3. Spatial Clustering for Dispatch Zones
    # ==========================================
    coords = df[['Dest_Latitude', 'Dest_Longitude']].values
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Spatial_Cluster'] = kmeans.fit_predict(coords)
    centroids = kmeans.cluster_centers_

    # ==========================================
    # FIGURE 3: Spatial Clusters & Micro-Hubs
    # ==========================================
    plt.figure(figsize=(11, 8), dpi=300)
    cluster_colors = ['#1f78b4', '#33a02c', '#fb9a99', '#e31a1c']
    labels = ['Zone Alpha (North)', 'Zone Beta (Central)', 'Zone Gamma (West)', 'Zone Delta (East)']

    for c_id in range(4):
        c_mask = df['Spatial_Cluster'] == c_id
        plt.scatter(
            df.loc[c_mask, 'Dest_Longitude'], df.loc[c_mask, 'Dest_Latitude'],
            color=cluster_colors[c_id], alpha=0.45, s=28, label=f'{labels[c_id]} (n={c_mask.sum()})'
        )

    # Plot Cluster Centroids (Optimal Urban Staging / Micro-Hubs)
    plt.scatter(
        centroids[:, 1], centroids[:, 0],
        marker='*', s=260, color='#ffff33', edgecolors='#000000', linewidth=1.5,
        label='Cluster Centroids (Proposed Micro-Hubs)', zorder=5
    )

    # Plot Existing Regional Warehouses
    wh_df = df[['Origin_Warehouse_ID', 'Origin_Warehouse_Type']].drop_duplicates()
    wh_coords = {
        'RDC-NORTH': (40.8500, -73.9200),
        'RDC-SOUTH': (40.6500, -74.1500),
        'MFC-CENTRAL': (40.7580, -73.9855),
        'MFC-EAST': (40.7282, -73.7949)
    }
    for wid, (wlat, wlon) in wh_coords.items():
        plt.scatter(
            wlon, wlat, marker='s', s=180, color='#e41a1c' if 'RDC' in wid else '#984ea3',
            edgecolors='black', linewidth=1.5, zorder=6
        )
        plt.text(wlon + 0.008, wlat + 0.004, wid, fontsize=9, fontweight='bold', color='#222222')

    plt.title('Spatial Clustering of Delivery Drops for Dynamic Micro-Zone Partitioning', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Longitude', fontsize=11, fontweight='bold')
    plt.ylabel('Latitude', fontsize=11, fontweight='bold')
    plt.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.95, fontsize=9)
    plt.tight_layout()
    fig3_path = os.path.join('figures', 'fig3_spatial_clustering.png')
    plt.savefig(fig3_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved Figure 3 to {fig3_path}")

    # ==========================================
    # 4. Route Optimization Simulation (TSP / VRP)
    # ==========================================
    # Select 25 stops from Cluster 1 (Central dense area)
    cluster_sample = df[df['Spatial_Cluster'] == 1].head(22).copy().reset_index(drop=True)
    mfc_lat, mfc_lon = 40.7580, -73.9855  # MFC-CENTRAL depot

    # Coordinates list starting and ending at depot
    stop_lats = [mfc_lat] + cluster_sample['Dest_Latitude'].tolist()
    stop_lons = [mfc_lon] + cluster_sample['Dest_Longitude'].tolist()
    n_stops = len(stop_lats)

    # Compute pairwise Euclidean distance matrix (approx km)
    dist_matrix = np.zeros((n_stops, n_stops))
    for i in range(n_stops):
        for j in range(n_stops):
            dlat = (stop_lats[i] - stop_lats[j]) * 111.0
            dlon = (stop_lons[i] - stop_lons[j]) * 85.0
            dist_matrix[i, j] = np.sqrt(dlat**2 + dlon**2) * 1.35  # urban circuity

    # Baseline: Unoptimized sequential order (first-in first-out dispatch)
    baseline_tour = list(range(n_stops)) + [0]
    baseline_dist = sum(dist_matrix[baseline_tour[k], baseline_tour[k+1]] for k in range(len(baseline_tour)-1))

    # Optimization: Greedy Nearest Neighbor heuristic + 2-Opt local search
    unvisited = set(range(1, n_stops))
    optimized_tour = [0]
    curr = 0
    while unvisited:
        nxt = min(unvisited, key=lambda node: dist_matrix[curr, node])
        optimized_tour.append(nxt)
        unvisited.remove(nxt)
        curr = nxt
    optimized_tour.append(0)  # return to depot

    # Simple 2-Opt improvement
    improved = True
    while improved:
        improved = False
        for i in range(1, len(optimized_tour) - 2):
            for j in range(i + 1, len(optimized_tour) - 1):
                cur_seg = dist_matrix[optimized_tour[i-1], optimized_tour[i]] + dist_matrix[optimized_tour[j], optimized_tour[j+1]]
                new_seg = dist_matrix[optimized_tour[i-1], optimized_tour[j]] + dist_matrix[optimized_tour[i], optimized_tour[j+1]]
                if new_seg < cur_seg - 1e-4:
                    optimized_tour[i:j+1] = reversed(optimized_tour[i:j+1])
                    improved = True

    opt_dist = sum(dist_matrix[optimized_tour[k], optimized_tour[k+1]] for k in range(len(optimized_tour)-1))
    distance_savings = (baseline_dist - opt_dist) / baseline_dist * 100
    fuel_saved_liters = (baseline_dist - opt_dist) * 0.12  # 12L / 100km for delivery van
    co2_saved_kg = fuel_saved_liters * 2.68  # kg CO2 per liter diesel

    print("\n--- ROUTE OPTIMIZATION SIMULATION (22 STOPS + DEPOT) ---")
    print(f"Baseline Unoptimized Tour Distance: {baseline_dist:.2f} km")
    print(f"Optimized Heuristic Tour Distance:  {opt_dist:.2f} km")
    print(f"Total Mileage Reduction:            {distance_savings:.2f}%")
    print(f"Estimated Fuel Saved:               {fuel_saved_liters:.2f} Liters")
    print(f"Estimated Carbon Avoided:           {co2_saved_kg:.2f} kg CO2e")

    # ==========================================
    # FIGURE 4: Baseline vs Optimized Route
    # ==========================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # Plot Baseline
    for k in range(len(baseline_tour)-1):
        p1, p2 = baseline_tour[k], baseline_tour[k+1]
        ax1.plot([stop_lons[p1], stop_lons[p2]], [stop_lats[p1], stop_lats[p2]], color='#e41a1c', linestyle='-', linewidth=1.4, alpha=0.7)
    ax1.scatter([stop_lons[i] for i in range(1, n_stops)], [stop_lats[i] for i in range(1, n_stops)], color='#377eb8', s=60, zorder=4, label='Delivery Stops')
    ax1.scatter(mfc_lon, mfc_lat, marker='*', s=350, color='#ffff33', edgecolors='black', linewidth=1.5, zorder=5, label='Fulfillment Depot (MFC)')
    ax1.set_title(f'A. Unoptimized Dispatch Route\nTotal Distance: {baseline_dist:.1f} km', fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel('Longitude', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Latitude', fontsize=10, fontweight='bold')
    ax1.legend(loc='lower right', frameon=True, facecolor='white')

    # Plot Optimized
    for k in range(len(optimized_tour)-1):
        p1, p2 = optimized_tour[k], optimized_tour[k+1]
        ax2.plot([stop_lons[p1], stop_lons[p2]], [stop_lats[p1], stop_lats[p2]], color='#2ca02c', linestyle='-', linewidth=1.8, alpha=0.85)
        # Add small arrow indicating direction
        mid_x = (stop_lons[p1] + stop_lons[p2]) / 2.0
        mid_y = (stop_lats[p1] + stop_lats[p2]) / 2.0
    ax2.scatter([stop_lons[i] for i in range(1, n_stops)], [stop_lats[i] for i in range(1, n_stops)], color='#377eb8', s=60, zorder=4, label='Delivery Stops')
    ax2.scatter(mfc_lon, mfc_lat, marker='*', s=350, color='#ffff33', edgecolors='black', linewidth=1.5, zorder=5, label='Fulfillment Depot (MFC)')
    ax2.set_title(f'B. Optimized Heuristic Tour (TSP/2-Opt)\nTotal Distance: {opt_dist:.1f} km (Savings: {distance_savings:.1f}%)', fontsize=12, fontweight='bold', pad=10, color='#1b7837')
    ax2.set_xlabel('Longitude', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Latitude', fontsize=10, fontweight='bold')
    ax2.legend(loc='lower right', frameon=True, facecolor='white')

    plt.tight_layout()
    fig4_path = os.path.join('figures', 'fig4_route_optimization.png')
    plt.savefig(fig4_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved Figure 4 to {fig4_path}")

    # Return key summary dictionary for reporting
    metrics = {
        'total_orders': len(df),
        'otif_rate': otif_rate,
        'late_rate': late_rate,
        'fadr': fadr,
        'avg_cost': avg_cost,
        'median_cost': median_cost,
        'avg_distance': avg_distance,
        'model_acc': acc,
        'model_roc_auc': roc_auc,
        'model_precision': prec,
        'model_recall': rec,
        'model_f1': f1,
        'top_features': feat_imp.head(6)['Feature'].tolist(),
        'top_importances': (feat_imp.head(6)['Importance'] * 100).tolist(),
        'baseline_dist': baseline_dist,
        'opt_dist': opt_dist,
        'distance_savings': distance_savings,
        'fuel_saved_liters': fuel_saved_liters,
        'co2_saved_kg': co2_saved_kg
    }
    return metrics

if __name__ == '__main__':
    metrics = run_pipeline()
    print("\nPipeline execution complete! Summary metrics successfully calculated.")
