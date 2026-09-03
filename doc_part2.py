# Executive Summary
add_styled_heading(doc, "Executive Summary", level=1)
p = doc.add_paragraph()
p.add_run(
    "Modern e-commerce and retail supply chains operate under relentless pressure to satisfy shrinking delivery windows "
    "while managing transportation costs, inventory imbalances, and urban gridlock. The last mile of logistics represents "
    "up to 53% of total supply chain operating expenses. This strategic planning report outlines a rigorous, data-driven "
    "framework designed to optimize multi-echelon inventory allocation and transform last-mile delivery operations through "
    "applied data science, machine learning, and operations research."
)

add_callout(
    doc,
    "By transitioning from static FIFO dispatching to an integrated predictive and prescriptive optimization engine, "
    "the enterprise can achieve an On-Time In-Full (OTIF) rate exceeding 96%, reduce last-mile mileage by over 50%, "
    "lower per-delivery operating costs by 15-20%, and significantly mitigate supply chain carbon intensity.",
    title="EXECUTIVE VALUE PROPOSITION"
)

p = doc.add_paragraph()
p.add_run(
    "This document establishes the strategic deliverables for Week 1: operational scenario scoping, literature and open data "
    "benchmarking (using the Amazon Last-Mile and DataCo Supply Chain corpora), mathematical KPI formulations, a 7-phase analytical "
    "roadmap, and modular Python implementation scripts. In our simulated 3,000-order trial, machine learning achieved a 0.9976 ROC-AUC "
    "in predicting delivery delay risk, while heuristic TSP routing demonstrated a 50.84% reduction in travel mileage."
)

# Section 1: Project Definition & Logistics Scenario
add_styled_heading(doc, "1. Project Definition & Logistics Scenario", level=1)
add_styled_heading(doc, "1.1 Network Context & Operational Scenario", level=2)
p = doc.add_paragraph()
p.add_run(
    "The target enterprise manages a multi-tier fulfillment logistics network servicing a high-density metropolitan area. "
    "The distribution network is organized into two primary tiers:\n"
    "1. Regional Distribution Centers (RDCs): Large-scale fulfillment hubs (RDC-North, RDC-South) carrying broad SKU catalogues, "
    "fulfilling standard bulk ground shipments, and managing long-haul supplier replenishment.\n"
    "2. Urban Micro-Fulfillment Centers (MFCs): Localized urban dark stores (MFC-Central, MFC-East) situated near dense customer "
    "clusters to service rapid Same-Day Express (under 6 hours) and Next-Day Priority (under 24 hours) orders."
)

add_styled_heading(doc, "1.2 Core Operational Challenges", level=2)
p = doc.add_paragraph()
p.add_run(
    "The enterprise currently experiences three acute operational pain points:\n"
    "- Inventory Misallocation & Stockouts: Phantom stockouts in urban MFCs force costly cross-region split dispatches from RDCs, "
    "increasing cost-per-drop by 25% and transit duration by 65%.\n"
    "- Same-Day SLA Vulnerability: Baseline Same-Day Express deliveries suffer an alarming 16.25% late delivery rate due to traffic "
    "congestion and multi-attempt failures.\n"
    "- Static Dispatch Routing: Unoptimized first-in first-out dispatch produces overlapping routes, high vehicle wear, excess fuel "
    "burn, and avoidable driver overtime."
)

add_styled_heading(doc, "1.3 Key Performance Indicators (KPIs)", level=2)
p = doc.add_paragraph()
p.add_run("The following five strategic KPIs establish quantitative baselines and target benchmarks:")

kpi_table = doc.add_table(rows=6, cols=6)
kpi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
kpi_table.autofit = False
kpi_headers = ["KPI Name", "Category", "Mathematical Formula", "Baseline", "Target", "Business Impact"]
kpi_widths = [Inches(1.2), Inches(0.9), Inches(1.8), Inches(0.7), Inches(0.7), Inches(1.2)]

for i, title in enumerate(kpi_headers):
    c = kpi_table.rows[0].cells[i]
    c.width = kpi_widths[i]
    set_cell_background(c, "1B365D")
    set_cell_margins(c, 80, 80, 80, 80)
    p_h = c.paragraphs[0]; p_h.paragraph_format.space_after = Pt(0); p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_h.add_run(title); r.font.name = 'Arial'; r.font.size = Pt(8); r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

kpi_rows = [
    ("1. On-Time In-Full (OTIF) Rate", "Service Quality", "(N_ontime_infull / N_total) * 100", "91.73%", ">= 96.0%", "Protects brand loyalty, eliminates SLA penalties."),
    ("2. Cost Per Delivery", "Financial Efficiency", "Total Last-Mile Cost / Total Stops", "$36.40 / stop", "<= $30.00 (-17.5%)", "Expands profit margin on rapid fulfillment."),
    ("3. Inventory Turnover Ratio", "Working Capital", "COGS / Average Inventory Value", "6.2x / yr", ">= 8.5x / yr", "Minimizes holding costs and inventory obsolescence."),
    ("4. First-Attempt Delivery Rate", "Operational Quality", "(N_single_attempt / N_total) * 100", "86.57%", ">= 95.0%", "Eliminates expensive re-delivery attempts ($6.50/re-attempt)."),
    ("5. Route Carbon Intensity", "ESG / Sustainability", "Total CO2e (kg) / Ton-km Delivered", "184 g/t-km", "<= 135 g/t-km (-26%)", "Ensures compliance with urban clean air regulations.")
]

for r_idx, r_data in enumerate(kpi_rows):
    rc = kpi_table.rows[r_idx + 1].cells
    bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
    for c_idx, val in enumerate(r_data):
        rc[c_idx].width = kpi_widths[c_idx]
        set_cell_background(rc[c_idx], bg)
        set_cell_margins(rc[c_idx], 60, 60, 70, 70)
        set_cell_borders(rc[c_idx], bottom=('single', '4', 'D0D7DE'), top=('single', '4', 'D0D7DE'))
        p_c = rc[c_idx].paragraphs[0]; p_c.paragraph_format.space_after = Pt(0)
        r = p_c.add_run(val); r.font.name = 'Calibri'; r.font.size = Pt(8)
        if c_idx in [0, 3, 4]: r.font.bold = True
        if c_idx == 3: r.font.color.rgb = RGBColor(180, 40, 40)
        elif c_idx == 4: r.font.color.rgb = RGBColor(30, 130, 60)

doc.add_paragraph().paragraph_format.space_after = Pt(8)
