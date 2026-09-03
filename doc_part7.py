# Section 6: Business Impact & Strategic Recommendations
add_styled_heading(doc, "6. Business Impact, Risk Analysis & Recommendations", level=1)
add_styled_heading(doc, "6.1 Quantified Financial ROI & Value Creation", level=2)
p = doc.add_paragraph()
p.add_run(
    "Extrapolating these empirical findings across an enterprise fleet of 120 delivery vans executing 300,000 annual deliveries "
    "yields compelling economic returns:\n"
    "1. Fleet Fuel & Maintenance Savings: A 30% sustained mileage reduction across daily routes eliminates ~850,000 km of driving, "
    "saving an estimated $272,000 in fuel and avoiding 270 metric tons of CO2e annually.\n"
    "2. Overtime Elimination: Reducing driving hours per route by 3.8 hours cuts peak-season driver overtime by $480,000/year.\n"
    "3. First-Attempt Failure Avoidance: Predictive pre-dispatch intervention drops re-attempt rates from 13.4% to <5%, saving $165,000/year."
)

add_styled_heading(doc, "6.2 Risk Assessment & Governance Matrix", level=2)
risk_table = doc.add_table(rows=5, cols=4)
risk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
risk_table.autofit = False
risk_headers = ["Risk Domain", "Risk Description", "Severity / Likelihood", "Mitigation Strategy"]
risk_widths = [Inches(1.2), Inches(2.0), Inches(1.3), Inches(2.0)]

for i, t in enumerate(risk_headers):
    c = risk_table.rows[0].cells[i]
    c.width = risk_widths[i]
    set_cell_background(c, "1B365D")
    set_cell_margins(c, 80, 80, 80, 80)
    p_h = c.paragraphs[0]; p_h.paragraph_format.space_after = Pt(0); p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run(t); r.font.name = 'Arial'; r.font.size = Pt(8); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

risk_rows = [
    ("Data Latency & Quality", "WMS/TMS GPS dropouts, stale inventory counts.", "High / Medium", "Implement streaming validation (Great Expectations) with automatic fallback schemas."),
    ("Driver Non-Compliance", "Drivers bypass algorithmic routes due to perceived lack of nuance.", "High / High", "Driver mobile UI with real-time traffic overlay, turn-by-turn guidance, and gamified incentives."),
    ("Concept & Data Drift", "Holiday surges (Cyber Week) distort historical traffic and demand.", "Medium / High", "Continuous MLOps drift monitoring (Evidently AI) triggering automated bi-weekly retraining."),
    ("Model Overfitting", "Overly tight route optimization leaves no slack for urban delays.", "Medium / Medium", "Enforce dynamic buffer windows (10-15% slack factor) in the CVRPTW solver.")
]

for r_idx, r_vals in enumerate(risk_rows):
    rc = risk_table.rows[r_idx + 1].cells
    bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, v in enumerate(r_vals):
        rc[c_idx].width = risk_widths[c_idx]
        set_cell_background(rc[c_idx], bg)
        set_cell_margins(rc[c_idx], 60, 60, 70, 70)
        set_cell_borders(rc[c_idx], bottom=('single', '4', 'D0D7DE'), top=('single', '4', 'D0D7DE'))
        p_c = rc[c_idx].paragraphs[0]; p_c.paragraph_format.space_after = Pt(0)
        r = p_c.add_run(v); r.font.name = 'Calibri'; r.font.size = Pt(8)
        if c_idx == 0: r.font.bold = True

# Section 7: Conclusion & References
add_styled_heading(doc, "7. Conclusion & Strategic Next Steps", level=1)
p = doc.add_paragraph()
p.add_run(
    "The Week 1 strategic planning report demonstrates that an integrated machine learning and operations research architecture "
    "fundamentally transforms urban logistics economics. By combining early-warning delay prediction (0.9976 ROC-AUC), spatial micro-zoning, "
    "and heuristic route optimization (50.84% mileage reduction), the enterprise is primed to exceed the 96% OTIF threshold while saving nearly $1M annually."
)

add_callout(
    doc,
    "Immediate Action Items for Week 2:\n"
    "1. Productionize Kafka ingestion pipelines connecting WMS and TMS databases into the central lakehouse.\n"
    "2. Deploy a 10-van A/B operational pilot in Urban Zone Beta comparing 2-Opt dispatch against legacy FIFO routing.\n"
    "3. Incorporate live weather and OSRM real-time traffic distance matrices into the pre-dispatch scoring service.",
    title="WEEK 2 EXECUTION ROADMAP"
)

add_styled_heading(doc, "8. References & Academic Citations", level=1)
refs = [
    "Amazon Last-Mile Routing Research Challenge Dataset (2021). Amazon.com Inc. & MIT Center for Transportation & Logistics.",
    "DataCo Global Supply Chain Intelligence Dataset (2019). Kaggle Public Repository.",
    "Dantzig, G. B., & Ramser, J. H. (1959). The truck dispatching problem. Management Science, 6(1), 80-91.",
    "Toth, P., & Vigo, D. (Eds.). (2002). The vehicle routing problem. Society for Industrial and Applied Mathematics (SIAM).",
    "Silver, E. A., Pyke, D. F., & Peterson, R. (1998). Inventory management and production planning and scheduling. John Wiley & Sons.",
    "U.S. Department of Transportation, Bureau of Transportation Statistics (BTS). (2023). Freight Analysis Framework (FAF5).",
    "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. ACM SIGKDD (pp. 785-794)."
]
for rf in refs:
    p_rf = doc.add_paragraph(style='List Bullet'); p_rf.paragraph_format.space_after = Pt(2)
    r = p_rf.add_run(rf); r.font.name = 'Calibri'; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(60, 60, 60)

doc_path = "Logistics_Strategic_Planning_Report.docx"
doc.save(doc_path)
print(f"Document successfully compiled and saved to {doc_path}!")
