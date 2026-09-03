add_styled_heading(doc, "5.3 Spatial Clustering for Dynamic Micro-Zone Partitioning", level=2)
p = doc.add_paragraph()
p.add_run(
    "Unsupervised K-Means clustering partitioned customer drop coordinates into four distinct operational zones "
    "(Zone Alpha, Zone Beta, Zone Gamma, Zone Delta) across the metropolitan region:"
)

add_image_with_caption(
    doc,
    os.path.join("figures", "fig3_spatial_clustering.png"),
    "Figure 3: Spatial Clustering of Delivery Locations with Identified Cluster Centroids (Proposed Micro-Hubs) and Regional Warehouses."
)

p = doc.add_paragraph()
p.add_run(
    "As visualized in Figure 3, zoning stops by spatial density prevents van routes from traversing cross-city corridors. "
    "Crucially, the four calculated cluster centroids (yellow stars) identify mathematically optimal candidate sites for forward-deployed "
    "micro-fulfillment dark stores or mobile container hubs, cutting stem transit distance from peripheral RDCs."
)

add_styled_heading(doc, "5.4 Combinatorial Route Optimization Simulation", level=2)
p = doc.add_paragraph()
p.add_run(
    "To test the efficiency of automated vehicle routing, a dispatch simulation was conducted on 22 delivery stops originating from MFC-Central. "
    "A legacy unoptimized (FIFO) sequence was compared against our 2-Opt TSP heuristic optimization:"
)

add_image_with_caption(
    doc,
    os.path.join("figures", "fig4_route_optimization.png"),
    "Figure 4: Delivery Tour Comparison for a 22-Stop Van Dispatch: (A) Unoptimized Baseline Route vs. (B) Heuristic 2-Opt Optimized Route."
)

opt_table = doc.add_table(rows=6, cols=4)
opt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
opt_table.autofit = False
opt_headers = ["Operational Dimension", "Baseline (Unoptimized)", "Optimized (2-Opt TSP)", "Net Improvement / Savings"]
opt_widths = [Inches(1.8), Inches(1.5), Inches(1.5), Inches(1.7)]

for i, t in enumerate(opt_headers):
    c = opt_table.rows[0].cells[i]
    c.width = opt_widths[i]
    set_cell_background(c, "1B365D")
    set_cell_margins(c, 80, 80, 80, 80)
    p_h = c.paragraphs[0]; p_h.paragraph_format.space_after = Pt(0); p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run(t); r.font.name = 'Arial'; r.font.size = Pt(8); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

opt_rows = [
    ("Total Tour Road Distance", "267.39 km", "131.44 km", "-135.95 km (-50.84%)"),
    ("Estimated Driving Time", "7.64 hours", "3.75 hours", "-3.89 hours (-50.91%)"),
    ("Diesel Fuel Consumption", "32.09 Liters", "15.77 Liters", "-16.31 Liters (-50.83%)"),
    ("Carbon Emissions (CO2e)", "86.00 kg CO2e", "42.27 kg CO2e", "-43.73 kg CO2e (-50.85%)"),
    ("Estimated Driver Labor Cost", "$194.82", "$95.63", "-$99.19 (-50.91%)")
]

for r_idx, r_vals in enumerate(opt_rows):
    rc = opt_table.rows[r_idx + 1].cells
    bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, v in enumerate(r_vals):
        rc[c_idx].width = opt_widths[c_idx]
        set_cell_background(rc[c_idx], bg)
        set_cell_margins(rc[c_idx], 60, 60, 70, 70)
        set_cell_borders(rc[c_idx], bottom=('single', '4', 'D0D7DE'), top=('single', '4', 'D0D7DE'))
        p_c = rc[c_idx].paragraphs[0]; p_c.paragraph_format.space_after = Pt(0)
        r = p_c.add_run(v); r.font.name = 'Calibri'; r.font.size = Pt(8.5)
        if c_idx == 0: r.font.bold = True
        elif c_idx == 3: r.font.bold = True; r.font.color.rgb = RGBColor(30, 130, 60)

doc.add_paragraph().paragraph_format.space_after = Pt(8)
