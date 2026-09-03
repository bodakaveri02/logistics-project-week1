# Section 4: Python Code Illustration
add_styled_heading(doc, "4. Python Code Illustration & Technical Architecture", level=1)
p = doc.add_paragraph()
p.add_run(
    "To operationalize the analytical framework, production-grade Python scripts have been authored. "
    "Below are the core architectural modules illustrating feature engineering, delay risk modeling, and route optimization:"
)

add_styled_heading(doc, "4.1 Data Cleaning & Feature Engineering Pipeline", level=2)
code_f = """# Feature engineering: calculate spatial distances & temporal lags
def preprocess_logistics_data(df: pd.DataFrame) -> pd.DataFrame:
    d_lat = (df['Dest_Latitude'] - df['Origin_Latitude']) * 111.0
    d_lon = (df['Dest_Longitude'] - df['Origin_Longitude']) * 85.0
    df['Direct_Distance_km'] = np.sqrt(d_lat**2 + d_lon**2)
    df['Route_Distance_km'] = df['Direct_Distance_km'] * 1.38  # Urban circuity factor
    df['Order_Timestamp'] = pd.to_datetime(df['Order_Timestamp'])
    df['Hour_of_Day'] = df['Order_Timestamp'].dt.hour
    df['Is_Weekend'] = df['Order_Timestamp'].dt.dayofweek.isin([5, 6]).astype(int)
    return pd.get_dummies(df, columns=['Shipping_Mode', 'Origin_Warehouse_Type'], drop_first=True)
"""
add_code_block(doc, code_f, caption="feature_pipeline.py")

add_styled_heading(doc, "4.2 Supervised Machine Learning: Late Delivery Risk Classifier", level=2)
code_ml = """# Train Balanced Random Forest classifier for pre-dispatch delay prediction
def train_delay_classifier(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)
    clf = RandomForestClassifier(n_estimators=150, max_depth=8, class_weight='balanced', random_state=42)
    clf.fit(X_train, y_train)
    y_pred, y_prob = clf.predict(X_test), clf.predict_proba(X_test)[:, 1]
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    return clf, clf.feature_importances_
"""
add_code_block(doc, code_ml, caption="delay_risk_model.py")

add_styled_heading(doc, "4.3 Spatial Clustering & Heuristic Route Optimization (2-Opt TSP)", level=2)
code_opt = """# Cluster delivery drops & optimize stop sequence using Nearest Neighbor + 2-Opt
def optimize_cluster_routes(coords, depot_coord):
    kmeans = KMeans(n_clusters=4, random_state=42).fit(coords)
    all_stops = [depot_coord] + list(coords)
    dist_mat = np.linalg.norm(np.array(all_stops)[:, None] - np.array(all_stops), axis=2)
    # Nearest Neighbor construction
    unvisited, tour, curr = set(range(1, len(all_stops))), [0], 0
    while unvisited:
        nxt = min(unvisited, key=lambda i: dist_mat[curr, i])
        tour.append(nxt); unvisited.remove(nxt); curr = nxt
    tour.append(0)
    # 2-Opt local search refinement
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                if dist_mat[tour[i-1], tour[j]] + dist_mat[tour[i], tour[j+1]] < dist_mat[tour[i-1], tour[i]] + dist_mat[tour[j], tour[j+1]] - 1e-4:
                    tour[i:j+1] = reversed(tour[i:j+1]); improved = True
    return tour, dist_mat
"""
add_code_block(doc, code_opt, caption="route_optimization_engine.py")
