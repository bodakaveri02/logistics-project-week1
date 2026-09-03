# Section 2: Literature Review & Data Research
add_styled_heading(doc, "2. Literature Review & Data Science Research", level=1)
add_styled_heading(doc, "2.1 Benchmark Public Datasets", level=2)
p = doc.add_paragraph()
p.add_run(
    "Our analytical framework is grounded in empirical research using three prominent public datasets:\n"
    "1. Amazon Last-Mile Routing Research Challenge Dataset (MIT/Amazon, 2021): Contains over 6,000 actual delivery routes "
    "with GPS coordinates, transit times, package dimensions, service times, and road circuity distributions (1.28 - 1.55).\n"
    "2. DataCo Global Supply Chain Intelligence Dataset: A repository of 180,000+ omnichannel order transactions detailing delivery "
    "status, late delivery risk factors, order geography, and shipping modes.\n"
    "3. US DOT BTS Freight Analysis Framework (FAF5): Multimodal freight flow data and highway speed indices across major metro corridors."
)

add_styled_heading(doc, "2.2 Applied Data Science Methodologies", level=2)
p = doc.add_paragraph()
p.add_run(
    "The project integrates four complementary data science paradigms:\n"
    "- Supervised Regression & Time-Series: LightGBM and XGBoost models for localized SKU-level demand forecasting, incorporating "
    "rolling sales lags, calendar factors, and promotional seasonality.\n"
    "- Supervised Classification: Balanced Random Forest classifiers predicting pre-dispatch Late Delivery Risk at order manifestation, "
    "enabling proactive SLA intervention.\n"
    "- Unsupervised Spatial Clustering: K-Means and DBSCAN algorithms partitioning delivery drops into compact urban micro-zones and "
    "identifying optimal centroid locations for urban micro-hubs.\n"
    "- Prescriptive Operations Research: Heuristic Capacitated Vehicle Routing Problem with Time Windows (CVRPTW) combining Clarke-Wright "
    "Savings, Greedy Nearest Neighbor, and 2-Opt local search."
)

# Section 3: Strategic Roadmap
add_styled_heading(doc, "3. Strategic Roadmap: End-to-End Analytical Pipeline", level=1)
p = doc.add_paragraph()
p.add_run(
    "The analytical transformation is structured across an end-to-end 7-phase implementation roadmap:"
)

road_table = doc.add_table(rows=8, cols=5)
road_table.alignment = WD_TABLE_ALIGNMENT.CENTER
road_table.autofit = False
road_headers = ["Phase", "Operational Scope", "Key Technical Activities", "Primary Deliverable", "Timeline"]
road_widths = [Inches(1.0), Inches(1.3), Inches(2.2), Inches(1.2), Inches(0.8)]

for i, t in enumerate(road_headers):
    c = road_table.rows[0].cells[i]
    c.width = road_widths[i]
    set_cell_background(c, "1B365D")
    set_cell_margins(c, 80, 80, 80, 80)
    p_h = c.paragraphs[0]; p_h.paragraph_format.space_after = Pt(0); p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run(t); r.font.name = 'Arial'; r.font.size = Pt(8); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

road_rows = [
    ("Phase 1: Scoping & Governance", "Requirements & Alignment", "Define SLAs, map warehouse tiers, establish KPI formulas, audit data compliance.", "Project Charter & KPI Matrix", "Weeks 1-2"),
    ("Phase 2: Ingestion Architecture", "Data Infrastructure", "Build Kafka/Airflow streaming pipelines linking ERP (SAP), WMS, and TMS GPS telematics.", "Automated Ingestion Lakehouse", "Weeks 3-4"),
    ("Phase 3: Cleansing & Feature Eng.", "Data Wrangling", "Geocoding, handling address errors, computing road circuity, building lag and traffic features.", "Clean Analytical Feature Store", "Weeks 5-6"),
    ("Phase 4: Exploratory Analysis", "Diagnostic Insights", "Spatial failure heatmaps, bottleneck correlation matrices, lead-time variance decomposition.", "Interactive Streamlit Dashboards", "Weeks 7-8"),
    ("Phase 5: ML & Optimization", "Model Development", "Train LightGBM forecasters, Random Forest delay classifiers, and 2-Opt CVRPTW routing engines.", "Trained & Validated Model Weights", "Weeks 9-11"),
    ("Phase 6: Simulation & Pilot", "Backtesting & Validation", "Simulate historical routing replays, conduct rolling cross-validation, run 10-van live pilot.", "Simulation & Pilot Audit Report", "Weeks 12-13"),
    ("Phase 7: Deployment & MLOps", "Enterprise Rollout", "Containerize inference microservices (FastAPI/Docker), integrate with driver mobile apps, drift monitors.", "Production Dispatch Engine", "Weeks 14-16")
]

for r_idx, r_data in enumerate(road_rows):
    rc = road_table.rows[r_idx + 1].cells
    bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, val in enumerate(r_data):
        rc[c_idx].width = road_widths[c_idx]
        set_cell_background(rc[c_idx], bg)
        set_cell_margins(rc[c_idx], 60, 60, 70, 70)
        set_cell_borders(rc[c_idx], bottom=('single', '4', 'D0D7DE'), top=('single', '4', 'D0D7DE'))
        p_c = rc[c_idx].paragraphs[0]; p_c.paragraph_format.space_after = Pt(0)
        r = p_c.add_run(val); r.font.name = 'Calibri'; r.font.size = Pt(8)
        if c_idx in [0, 4]: r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)
