# Section 5: Empirical Findings & Experimental Results
add_styled_heading(doc, "5. Empirical Findings & Experimental Results", level=1)
p = doc.add_paragraph()
p.add_run(
    "To substantiate the strategic framework with quantitative evidence, the complete Python data pipeline was executed "
    "across a simulated dataset of 3,000 operational dispatches. The empirical results reveal striking insights into current "
    "performance vulnerabilities and the transformative potential of data science intervention."
)

add_styled_heading(doc, "5.1 Baseline Logistics Performance & KPI Diagnostics", level=2)
p = doc.add_paragraph()
p.add_run(
    "The overall baseline OTIF rate was measured at 91.73%, falling below the 96.0% corporate standard. "
    "Disaggregating performance across shipping tiers and fulfillment nodes highlights severe structural asymmetry:"
)

add_image_with_caption(
    doc,
    os.path.join("figures", "fig1_kpi_distribution.png"),
    "Figure 1: Comprehensive Logistics KPI Dashboard showing (A) OTIF Rate by Shipping Mode, (B) Late Delivery Rate by Warehouse Tier, (C) Delivery Cost Distribution, and (D) Transit Duration vs Distance Correlation."
)

p = doc.add_paragraph()
p.add_run(
    "Core findings from Figure 1:\n"
    "1. Shipping Tier Vulnerability: Standard Ground deliveries achieve a 97.31% OTIF rate with 0% late deliveries. In contrast, "
    "Same-Day Express displays an alarming 16.25% late delivery rate (OTIF 81.27%), identifying rapid fulfillment as the primary failure point.\n"
    "2. Fulfillment Node Advantage: Orders fulfilled from urban MFCs incur an average transit time of 3.68 hours and cost $32.35/drop, "
    "compared to 6.08 hours and $40.56/drop from regional RDCs—confirming a 20.2% cost advantage and 39.5% speed advantage for urban hubs.\n"
    "3. Cost Skewness: Average delivery cost is $36.40, with heavy right-tail outliers exceeding $65 due to failed attempts and congestion."
)

add_styled_heading(doc, "5.2 Machine Learning Delay Prediction & Feature Importance", level=2)
p = doc.add_paragraph()
p.add_run(
    "The Balanced Random Forest delay classifier demonstrated exceptional predictive accuracy on hold-out test dispatches: "
    "Accuracy: 98.83%, Precision: 96.30%, Recall: 81.25%, F1-Score: 88.14%, and an outstanding ROC-AUC of 0.9976."
)

add_image_with_caption(
    doc,
    os.path.join("figures", "fig2_feature_importance.png"),
    "Figure 2: Relative Feature Importance (Gini Impurity) for Late Delivery Risk Classification using Random Forest."
)

p = doc.add_paragraph()
p.add_run(
    "Figure 2 reveals that the number of Delivery Attempts is by far the single most decisive predictor of delay risk, "
    "accounting for 48.8% of model importance. When a delivery fails on its initial attempt, the probability of an SLA breach "
    "exceeds 85%. Promised SLA Hours (11.0%), Same-Day Express mode (9.9%), and Weather Severity (7.2%) represent the next key drivers. "
    "This confirms that first-attempt failure prevention is the highest-leverage intervention point for improving OTIF."
)
