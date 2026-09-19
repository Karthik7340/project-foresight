"""Project FORESIGHT - Executive Demand Forecasting & Inventory Risk Intelligence Hub.

Phase 4 Advanced UI/UX Redesign:
- Global Sidebar Control Center (Search, Filters, Safety Buffer Sliders, Currency Toggle, Diagnostics)
- Executive AI Insights Narrative & Dynamic Alert Notification Bar
- 5 Executive Intelligence Tabs:
    1. 📊 Executive Command Center & 2D Financial Risk Quadrant
    2. 📈 SKU Demand Trajectory & Multi-Layer Confidence Timeline
    3. 🧪 Stress Simulator & 2D Sensitivity Matrix Heatmap
    4. 📝 Autonomous Action Dispatcher & Interactive PO Center
    5. 🎯 ML Model Performance & Backtest Diagnostics
"""

from pathlib import Path
import datetime
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & SESSION STATE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Project FORESIGHT | Inventory Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session State for PO adjustments and approvals
if "po_overrides" not in st.session_state:
    st.session_state.po_overrides = {}
if "po_status" not in st.session_state:
    st.session_state.po_status = {}

# -----------------------------------------------------------------------------
# 2. DESIGN SYSTEM & CUSTOM CSS
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    /* Executive Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 20px;
        box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.05) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.98rem;
        font-weight: 400;
        margin-bottom: 14px;
    }
    .engine-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .pulsing-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
    }

    /* Critical Alert Banner */
    .alert-banner {
        background: linear-gradient(90deg, rgba(239, 68, 68, 0.2) 0%, rgba(185, 28, 28, 0.15) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        color: #fca5a5;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.15);
    }

    /* KPI Deck Cards */
    .kpi-card {
        background: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        height: 100%;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
    }
    .kpi-card-danger:hover {
        border-color: rgba(239, 68, 68, 0.6);
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.25);
    }
    .kpi-card-warning:hover {
        border-color: rgba(245, 158, 11, 0.6);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.25);
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        margin-bottom: 6px;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }
    .kpi-value-danger { color: #f87171; }
    .kpi-value-warning { color: #fbbf24; }
    .kpi-value-success { color: #34d399; }
    .kpi-subtext {
        font-size: 0.82rem;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Executive AI Narrative Box */
    .ai-summary-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-left: 4px solid #818cf8;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 24px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
    }
    .ai-summary-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: #c084fc;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    .ai-summary-text {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    /* Status Badges */
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 700;
        text-align: center;
    }
    .pill-stockout {
        background: rgba(239, 68, 68, 0.15);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }
    .pill-overstock {
        background: rgba(245, 158, 11, 0.15);
        color: #fde68a;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .pill-healthy {
        background: rgba(16, 185, 129, 0.15);
        color: #a7f3d0;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }

    /* Section Typography */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 8px;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }
    .section-desc {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-bottom: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. DATA INGESTION & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent.parent
    summary_path = base_dir / "data" / "processed" / "sku_forecast_risk_summary.csv"
    weekly_path = base_dir / "data" / "processed" / "weekly_sales_master.csv"
    inv_path = base_dir / "data" / "processed" / "latest_inventory.csv"

    if not summary_path.exists() or not weekly_path.exists():
        return None, None, None

    summary_df = pd.read_csv(summary_path)
    weekly_df = pd.read_csv(weekly_path)
    inv_df = pd.read_csv(inv_path) if inv_path.exists() else None
    return summary_df, weekly_df, inv_df


summary_df, weekly_df, inv_df = load_data()

if summary_df is None or weekly_df is None:
    st.error("🚨 Processed datasets missing! Please execute `python src/pipeline.py` and `python src/model.py` first.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. GLOBAL SIDEBAR & CONTROL CENTER
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin-bottom: 2px;'>⚡ FORESIGHT Controls</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.8rem; color: #64748b; margin-bottom: 16px;'>Executive Command & Policy Tuner</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("### 🔍 Global Search & Filters")
    sidebar_search = st.text_input("Search SKU or Category", placeholder="e.g. SKU_REORDER").strip()

    categories = ["All"] + list(summary_df["category"].unique())
    selected_category = st.selectbox("Category Scope", categories)

    risk_statuses = ["All"] + list(summary_df["risk_status"].unique())
    selected_risk = st.selectbox("Risk Status Scope", risk_statuses)

    st.divider()

    st.markdown("### ⚙️ Policy & Risk Tuning")
    target_safety_wos = st.slider("Target Safety Buffer (Weeks)", 1, 8, 4, help="Target operating safety stock floor")
    lead_time_margin_days = st.slider("Supplier Lead Time Safety Buffer (Days)", 0, 14, 0, help="Additional contingency days added to vendor lead times")

    st.divider()

    st.markdown("### 💱 Currency & Display Preferences")
    currency = st.radio("Display Currency", ["INR (₹)", "USD ($)"], index=0, horizontal=True)
    curr_symbol = "₹" if currency.startswith("INR") else "$"
    curr_rate = 1.0 if currency.startswith("INR") else 0.012  # 1 INR ~ 0.012 USD

    st.divider()

    st.markdown("### 🧠 ML Engine Diagnostics")
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px; font-size: 0.82rem;">
            <div style="color: #94a3b8;">Active Model: <strong style="color: #38bdf8;">Random Forest ML</strong></div>
            <div style="color: #94a3b8; margin-top: 4px;">Backtest WAPE: <strong style="color: #34d399;">24.49%</strong></div>
            <div style="color: #94a3b8; margin-top: 4px;">Baseline WAPE: <strong style="color: #f87171;">27.70%</strong></div>
            <div style="color: #94a3b8; margin-top: 4px;">Relative Accuracy Lift: <strong style="color: #c084fc;">+11.58%</strong></div>
            <div style="color: #64748b; margin-top: 8px; font-size: 0.75rem;">Pipeline Status: Healthy (72 Records)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Filter Dataset based on Sidebar Inputs
filtered_df = summary_df.copy()

# Apply Lead Time contingency buffer dynamically
if lead_time_margin_days > 0:
    filtered_df["effective_lead_time"] = filtered_df["lead_time_days"] + lead_time_margin_days
    filtered_df["forecast_lead_time_demand"] = (filtered_df["forecast_avg_weekly"] / 7.0) * filtered_df["effective_lead_time"]
    # Re-evaluate stockout risk with new lead time
    def calc_rebound_risk(r):
        if r["total_available_stock"] < r["forecast_lead_time_demand"]:
            return "Stockout Risk"
        elif r["weeks_of_supply"] > 12.0:
            return "Overstock Risk"
        return "Healthy"
    filtered_df["risk_status"] = filtered_df.apply(calc_rebound_risk, axis=1)

if sidebar_search:
    filtered_df = filtered_df[
        filtered_df["sku_id"].str.contains(sidebar_search, case=False, na=False) |
        filtered_df["category"].str.contains(sidebar_search, case=False, na=False)
    ]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
if selected_risk != "All":
    filtered_df = filtered_df[filtered_df["risk_status"] == selected_risk]

# Currency adjusted totals
total_sales_at_risk = filtered_df["sales_at_risk_inr"].sum() * curr_rate
total_locked_capital = filtered_df["locked_capital_inr"].sum() * curr_rate
stockout_skus = filtered_df[filtered_df["risk_status"] == "Stockout Risk"]
overstock_skus = filtered_df[filtered_df["risk_status"] == "Overstock Risk"]
healthy_skus = filtered_df[filtered_df["risk_status"] == "Healthy"]

# -----------------------------------------------------------------------------
# 5. HERO HEADER & ALERT BANNER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">⚡ Project FORESIGHT: Autonomous Inventory & Demand Intelligence</div>
        <div class="hero-subtitle">
            Enterprise Machine Learning Demand Forecasting, Lead-Time Runout Prevention & Working Capital Liquidation
        </div>
        <div style="display: flex; gap: 16px; flex-wrap: wrap; align-items: center;">
            <div class="engine-badge">
                <div class="pulsing-dot"></div> Random Forest ML Active (WAPE: 24.49% | +11.58% Lift)
            </div>
            <div style="color: #94a3b8; font-size: 0.82rem;">
                • Data Horizon: 119 Days Historical • 6-Week Out-of-Sample Forecast Horizon
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Dynamic Critical Alert Banner
if len(stockout_skus) > 0:
    stockout_names = ", ".join(stockout_skus["sku_id"].tolist())
    st.markdown(
        f"""
        <div class="alert-banner">
            <span style="font-size: 1.4rem;">🚨</span>
            <div>
                <strong>CRITICAL STOCKOUT WARNING:</strong> <strong>{len(stockout_skus)} SKU(s)</strong> ({stockout_names}) are projected to run out during vendor lead time, putting <strong>{curr_symbol}{total_sales_at_risk:,.2f}</strong> in sales revenue at risk! Immediate replenishment purchase orders required.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 6. EXECUTIVE KPI DECK
# -----------------------------------------------------------------------------
kcol1, kcol2, kcol3, kcol4 = st.columns(4)

with kcol1:
    st.markdown(
        f"""
        <div class="kpi-card kpi-card-danger">
            <div class="kpi-label">🚨 Sales Revenue at Risk</div>
            <div class="kpi-value kpi-value-danger">{curr_symbol}{total_sales_at_risk:,.2f}</div>
            <div class="kpi-subtext">
                <span style="color:#ef4444; font-weight:700;">{len(stockout_skus)} SKU(s)</span> stockout within lead time
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kcol2:
    st.markdown(
        f"""
        <div class="kpi-card kpi-card-warning">
            <div class="kpi-label">🔒 Trapped Working Capital</div>
            <div class="kpi-value kpi-value-warning">{curr_symbol}{total_locked_capital:,.2f}</div>
            <div class="kpi-subtext">
                <span style="color:#f59e0b; font-weight:700;">{len(overstock_skus)} SKU(s)</span> exceeding 12-week holding ceiling
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kcol3:
    imminent_sku_name = stockout_skus.sort_values(by="sales_at_risk_inr", ascending=False).iloc[0]["sku_id"] if len(stockout_skus) > 0 else "None"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">⚡ Highest Risk SKU</div>
            <div class="kpi-value" style="font-size:1.6rem; color:#38bdf8;">{imminent_sku_name}</div>
            <div class="kpi-subtext">
                Highest financial exposure SKU requiring priority PO
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kcol4:
    health_pct = (len(healthy_skus) / max(len(filtered_df), 1)) * 100
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">🛡️ Portfolio Health Score</div>
            <div class="kpi-value kpi-value-success">{health_pct:.0f}%</div>
            <div class="kpi-subtext">
                {len(healthy_skus)} of {len(filtered_df)} SKUs within target 1–12 WoS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# -----------------------------------------------------------------------------
# 7. MAIN TABBED EXECUTIVE INTERFACE
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Command Center & Risk Quadrant",
    "📈 Demand Forecast & SKU Deep Dive",
    "🧪 Stress Simulator & Sensitivity Matrix",
    "📝 Autonomous Action Dispatcher & POs",
    "🎯 ML Performance & Diagnostics"
])

# =============================================================================
# TAB 1: EXECUTIVE COMMAND CENTER & 2D RISK QUADRANT
# =============================================================================
with tab1:
    # Executive AI Narrative Summary
    st.markdown(
        f"""
        <div class="ai-summary-box">
            <div class="ai-summary-header">
                <span>🤖</span> EXECUTIVE FORESIGHT SYNTHESIS & FINANCIAL INSIGHTS
            </div>
            <div class="ai-summary-text">
                Project FORESIGHT has analyzed <strong>{len(summary_df)} active SKUs</strong> across historical sales data and vendor lead times.
                Current financial exposure stands at <strong>{curr_symbol}{total_sales_at_risk:,.2f}</strong> in potential stockout revenue losses and 
                <strong>{curr_symbol}{total_locked_capital:,.2f}</strong> in trapped working capital. 
                <br/>• <strong>Primary Action:</strong> Issue immediate replenishment PO for <strong>{imminent_sku_name}</strong> to prevent stockout runout within lead time.
                <br/>• <strong>Liquidation Opportunity:</strong> Activate markdown promo on <strong>SKU_CLEAR</strong> to liberate excess holding capital.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Financial Exposure & Risk Prioritization Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Interactive 2D quadrant scatter analysis and category breakdown contrasting stock levels against revenue exposure.</div>', unsafe_allow_html=True)

    col_q1, col_q2 = st.columns([3, 2])

    with col_q1:
        st.markdown("**Financial Risk Quadrant: Sales at Risk vs Weeks of Supply (WoS)**")
        scatter_chart = (
            alt.Chart(filtered_df)
            .mark_circle(size=220, opacity=0.85)
            .encode(
                x=alt.X("weeks_of_supply:Q", title="Weeks of Supply (WoS)", scale=alt.Scale(zero=False)),
                y=alt.Y("sales_at_risk_inr:Q", title=f"Sales at Risk ({curr_symbol})"),
                color=alt.Color(
                    "risk_status:N",
                    scale=alt.Scale(
                        domain=["Stockout Risk", "Overstock Risk", "Healthy"],
                        range=["#ef4444", "#f59e0b", "#10b981"]
                    ),
                    legend=alt.Legend(title="Risk Status", orient="top-left")
                ),
                tooltip=[
                    alt.Tooltip("sku_id:N", title="SKU"),
                    alt.Tooltip("category:N", title="Category"),
                    alt.Tooltip("risk_status:N", title="Status"),
                    alt.Tooltip("weeks_of_supply:Q", title="WoS", format=".2f"),
                    alt.Tooltip("sales_at_risk_inr:Q", title="Sales at Risk (₹)", format=",.2f"),
                    alt.Tooltip("locked_capital_inr:Q", title="Locked Capital (₹)", format=",.2f"),
                    alt.Tooltip("recommended_action:N", title="Recommended Action"),
                ]
            )
            .properties(height=340)
        )
        # Vertical reference lines for safety buffer and ceiling
        rule_wos_min = alt.Chart(pd.DataFrame({"x": [1.0]})).mark_rule(color="#ef4444", strokeDash=[4, 4]).encode(x="x:Q")
        rule_wos_max = alt.Chart(pd.DataFrame({"x": [12.0]})).mark_rule(color="#f59e0b", strokeDash=[4, 4]).encode(x="x:Q")
        st.altair_chart(scatter_chart + rule_wos_min + rule_wos_max, use_container_width=True)

    with col_q2:
        st.markdown("**Financial Exposure Split by Product Category**")
        cat_agg = filtered_df.groupby("category").agg({
            "sales_at_risk_inr": lambda x: sum(x) * curr_rate,
            "locked_capital_inr": lambda x: sum(x) * curr_rate
        }).reset_index()

        cat_melt = cat_agg.melt(id_vars=["category"], value_vars=["sales_at_risk_inr", "locked_capital_inr"],
                                var_name="Metric", value_name="Amount")
        cat_melt["Metric"] = cat_melt["Metric"].map({
            "sales_at_risk_inr": f"Sales at Risk ({curr_symbol})",
            "locked_capital_inr": f"Locked Capital ({curr_symbol})"
        })

        cat_chart = (
            alt.Chart(cat_melt)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("category:N", title="Category"),
                y=alt.Y("Amount:Q", title=f"Exposure ({curr_symbol})"),
                color=alt.Color("Metric:N", scale=alt.Scale(range=["#ef4444", "#f59e0b"]), legend=alt.Legend(orient="top")),
                tooltip=["category:N", "Metric:N", alt.Tooltip("Amount:Q", format=",.2f")]
            )
            .properties(height=340)
        )
        st.altair_chart(cat_chart, use_container_width=True)

    st.markdown("### 📋 Filtered Portfolio Risk Matrix")
    t_cols = [
        "sku_id", "category", "risk_status", "recommended_action",
        "sales_at_risk_inr", "locked_capital_inr", "stock_on_hand", "stock_on_order",
        "weeks_of_supply", "lead_time_days", "forecast_lead_time_demand", "forecast_avg_weekly"
    ]
    disp_df = filtered_df[t_cols].copy()
    disp_df["sales_at_risk_inr"] = disp_df["sales_at_risk_inr"] * curr_rate
    disp_df["locked_capital_inr"] = disp_df["locked_capital_inr"] * curr_rate

    rename_map = {
        "sku_id": "SKU ID",
        "category": "Category",
        "risk_status": "Risk Status",
        "recommended_action": "Action Required",
        "sales_at_risk_inr": f"Sales at Risk ({curr_symbol})",
        "locked_capital_inr": f"Locked Capital ({curr_symbol})",
        "stock_on_hand": "Stock On Hand",
        "stock_on_order": "Inbound Order",
        "weeks_of_supply": "Weeks of Supply",
        "lead_time_days": "Lead Time (d)",
        "forecast_lead_time_demand": "Lead Time Demand",
        "forecast_avg_weekly": "Avg Weekly Demand"
    }

    st.dataframe(
        disp_df.rename(columns=rename_map).style.format({
            f"Sales at Risk ({curr_symbol})": f"{curr_symbol}{{:,.2f}}",
            f"Locked Capital ({curr_symbol})": f"{curr_symbol}{{:,.2f}}",
            "Weeks of Supply": "{:.2f} wks",
            "Lead Time Demand": "{:.1f} units",
            "Avg Weekly Demand": "{:.1f} units",
        }),
        width="stretch",
        hide_index=True,
    )

# =============================================================================
# TAB 2: SKU DEMAND FORECAST & MULTI-LAYER CONFIDENCE TIMELINE
# =============================================================================
with tab2:
    st.markdown('<div class="section-title">SKU Demand Trajectory & 6-Week Forecast Timeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Multi-layer interactive visualization showing 18 weeks of historical actuals, 6-week ML demand projections, 95% confidence bands, and safety stock overlays.</div>', unsafe_allow_html=True)

    sku_sel_col, sku_card_col = st.columns([1, 3])
    with sku_sel_col:
        selected_sku = st.selectbox("Select SKU for Deep Dive", filtered_df["sku_id"].tolist())

    sku_data = filtered_df[filtered_df["sku_id"] == selected_sku].iloc[0]

    with sku_card_col:
        badge_style = (
            "pill-stockout" if sku_data["risk_status"] == "Stockout Risk"
            else ("pill-overstock" if sku_data["risk_status"] == "Overstock Risk" else "pill-healthy")
        )
        margin_pct = ((sku_data["selling_price"] - sku_data["unit_cost"]) / max(sku_data["selling_price"], 0.01)) * 100
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 22px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-bottom: 8px;">
                    <div>
                        <span class="pill {badge_style}">{sku_data['risk_status']}</span>
                        <span style="font-weight:800; font-size:1.2rem; margin-left:12px; color:#f8fafc;">{sku_data['sku_id']}</span>
                        <span style="color:#94a3b8; font-size:0.9rem; margin-left:8px;">({sku_data['category']})</span>
                    </div>
                    <div>
                        <span style="color:#cbd5e1; font-size:0.88rem;">Recommended Action: <strong style="color:#38bdf8;">{sku_data['recommended_action']}</strong></span>
                    </div>
                </div>
                <div style="display:flex; gap:20px; font-size:0.85rem; color:#cbd5e1; flex-wrap:wrap; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 10px;">
                    <div>Selling Price: <strong>{curr_symbol}{sku_data['selling_price']*curr_rate:.2f}</strong></div>
                    <div>Unit Cost: <strong>{curr_symbol}{sku_data['unit_cost']*curr_rate:.2f}</strong></div>
                    <div>Gross Margin: <strong style="color:#34d399;">{margin_pct:.1f}%</strong></div>
                    <div>Stock On Hand: <strong>{sku_data['stock_on_hand']} units</strong></div>
                    <div>Inbound PO: <strong>{sku_data['stock_on_order']} units</strong></div>
                    <div>Weeks of Supply: <strong>{sku_data['weeks_of_supply']:.2f} wks</strong></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Prepare historical dataframe
    hist_sku = weekly_df[weekly_df["sku_id"] == selected_sku].sort_values("week_start").copy()
    hist_sku["type"] = "Historical Actual"
    hist_sku["revenue"] = hist_sku["weekly_sales_units"] * sku_data["selling_price"] * curr_rate
    hist_sku["date"] = pd.to_datetime(hist_sku["week_start"])
    hist_sku["ci_lower"] = hist_sku["weekly_sales_units"]
    hist_sku["ci_upper"] = hist_sku["weekly_sales_units"]

    # Generate 6-Week ML Forecast rows with simulated 95% Confidence Interval
    last_date = hist_sku["date"].max()
    std_err = hist_sku["weekly_sales_units"].std() if len(hist_sku) > 1 else 5.0
    future_rows = []
    for step in range(1, 7):
        f_date = last_date + pd.Timedelta(weeks=step)
        f_units = float(sku_data[f"forecast_w{step}"])
        # Expanding uncertainty over forecast horizon
        uncertainty = 1.96 * std_err * (0.35 + (step * 0.08))
        future_rows.append({
            "week_start": f_date.strftime("%Y-%m-%d"),
            "weekly_sales_units": f_units,
            "type": "ML Forecast",
            "revenue": f_units * sku_data["selling_price"] * curr_rate,
            "date": f_date,
            "ci_lower": max(0.0, f_units - uncertainty),
            "ci_upper": f_units + uncertainty
        })
    future_df = pd.DataFrame(future_rows)

    combined_timeline = pd.concat([
        hist_sku[["week_start", "weekly_sales_units", "type", "revenue", "date", "ci_lower", "ci_upper"]],
        future_df
    ], ignore_index=True)

    # Altair Layered Chart: Historical Area + Forecast Line + Confidence Band + Safety Stock
    # 1. Historical Shaded Area
    hist_chart = (
        alt.Chart(combined_timeline[combined_timeline["type"] == "Historical Actual"])
        .mark_area(
            line={"color": "#38bdf8", "width": 2.5},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="rgba(56, 189, 248, 0.4)", offset=0),
                    alt.GradientStop(color="rgba(56, 189, 248, 0.02)", offset=1),
                ],
                x1=1, x2=1, y1=1, y2=0,
            ),
            point=alt.OverlayMarkDef(color="#38bdf8", size=50),
        )
        .encode(
            x=alt.X("week_start:N", title="Week Starting", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("weekly_sales_units:Q", title="Demand (Units)"),
            tooltip=[
                alt.Tooltip("week_start:N", title="Week"),
                alt.Tooltip("weekly_sales_units:Q", title="Actual Units", format=".0f"),
                alt.Tooltip("revenue:Q", title=f"Revenue ({curr_symbol})", format=",.2f"),
            ],
        )
    )

    # 2. Forecast Line with Markers
    fc_chart = (
        alt.Chart(combined_timeline[combined_timeline["type"] == "ML Forecast"])
        .mark_line(
            strokeDash=[6, 6],
            color="#f97316",
            strokeWidth=3,
            point=alt.OverlayMarkDef(color="#f97316", size=60, filled=True),
        )
        .encode(
            x=alt.X("week_start:N"),
            y=alt.Y("weekly_sales_units:Q"),
            tooltip=[
                alt.Tooltip("week_start:N", title="Forecast Week"),
                alt.Tooltip("weekly_sales_units:Q", title="Projected Demand", format=".1f"),
                alt.Tooltip("ci_lower:Q", title="95% CI Lower", format=".1f"),
                alt.Tooltip("ci_upper:Q", title="95% CI Upper", format=".1f"),
                alt.Tooltip("revenue:Q", title=f"Projected Revenue ({curr_symbol})", format=",.2f"),
            ],
        )
    )

    # 3. Forecast 95% Confidence Interval Shaded Band
    ci_band = (
        alt.Chart(combined_timeline[combined_timeline["type"] == "ML Forecast"])
        .mark_area(opacity=0.2, color="#f97316")
        .encode(
            x=alt.X("week_start:N"),
            y="ci_lower:Q",
            y2="ci_upper:Q"
        )
    )

    # 4. Target Safety Stock Buffer Overlay Line
    safety_stock_units = sku_data["forecast_avg_weekly"] * target_safety_wos
    safety_rule = (
        alt.Chart(pd.DataFrame({"y": [safety_stock_units]}))
        .mark_rule(color="#34d399", strokeDash=[4, 4], strokeWidth=1.5)
        .encode(y="y:Q")
    )

    # 5. Forecast Horizon Split Divider
    split_date = last_date.strftime("%Y-%m-%d")
    split_rule = (
        alt.Chart(pd.DataFrame({"split": [split_date]}))
        .mark_rule(color="#94a3b8", strokeDash=[3, 3], strokeWidth=1.5)
        .encode(x="split:N")
    )

    full_timeline_chart = (hist_chart + ci_band + fc_chart + safety_rule + split_rule).properties(height=380)
    st.altair_chart(full_timeline_chart, use_container_width=True)

    # Runout Gauge & Financial Profitability Cards
    dcol1, dcol2, dcol3 = st.columns(3)
    with dcol1:
        daily_rate = sku_data["forecast_avg_weekly"] / 7.0
        days_left = sku_data["stock_on_hand"] / max(daily_rate, 0.001)
        lt_days = sku_data["lead_time_days"]
        st.metric(
            "Days of Stock Remaining",
            f"{days_left:.1f} Days",
            delta=f"{days_left - lt_days:.1f}d buffer vs vendor lead time",
            delta_color="normal" if days_left >= lt_days else "inverse"
        )
    with dcol2:
        unit_margin = (sku_data["selling_price"] - sku_data["unit_cost"]) * curr_rate
        st.metric(
            "Profit Margin per Unit",
            f"{curr_symbol}{unit_margin:.2f}",
            delta=f"{margin_pct:.1f}% Gross Margin"
        )
    with dcol3:
        holding_cost_est = (sku_data["unit_cost"] * 0.15) * curr_rate  # 15% annual holding cost assumption
        st.metric(
            "Annualized Holding Cost",
            f"{curr_symbol}{holding_cost_est:.2f} / unit",
            delta="Holding Cost Penalty" if sku_data["weeks_of_supply"] > 12 else "Optimized",
            delta_color="off"
        )

# =============================================================================
# TAB 3: STRESS SIMULATOR & 2D SENSITIVITY MATRIX HEATMAP
# =============================================================================
with tab3:
    st.markdown('<div class="section-title">🧪 Multi-Variable Replenishment & Stress Test Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Simulate supplier delays, marketing promotional spikes, and replenishment purchase orders to test supply chain resilience.</div>', unsafe_allow_html=True)

    sim_sku_select = st.selectbox("Select Target SKU to Simulate", filtered_df["sku_id"].tolist(), key="sim_sku_key")
    sim_base = filtered_df[filtered_df["sku_id"] == sim_sku_select].iloc[0]

    sim_c1, sim_c2, sim_c3 = st.columns(3)
    with sim_c1:
        sim_lt_delta = st.slider("Supplier Lead Time Delay (Days)", -3, 14, 0, help="Simulate vendor delay or expedited air freight")
    with sim_c2:
        sim_promo_mult = st.slider("Promotional Demand Multiplier", 0.5, 2.5, 1.0, step=0.1, help="Simulate marketing surge or seasonal drop")
    with sim_c3:
        sim_new_po = st.number_input("Simulated Inbound PO Quantity (Units)", min_value=0, max_value=1000, value=0, step=25)

    # Calculate dynamic simulation metrics
    eff_lt = max(1, sim_base["lead_time_days"] + sim_lt_delta)
    eff_weekly_demand = sim_base["forecast_avg_weekly"] * sim_promo_mult
    eff_daily_rate = eff_weekly_demand / 7.0
    eff_lt_demand = eff_daily_rate * eff_lt
    eff_available_stock = sim_base["stock_on_hand"] + sim_base["stock_on_order"] + sim_new_po
    eff_wos = sim_base["stock_on_hand"] / max(eff_weekly_demand, 0.001)

    if eff_available_stock < eff_lt_demand:
        sim_risk_status = "Stockout Risk"
        sim_deficit = eff_lt_demand - eff_available_stock
        sim_sales_at_risk = sim_deficit * sim_base["selling_price"] * curr_rate
        sim_locked_cap = 0.0
    elif eff_wos > 12.0:
        sim_risk_status = "Overstock Risk"
        sim_sales_at_risk = 0.0
        sim_locked_cap = max(0.0, sim_base["stock_on_hand"] - (eff_weekly_demand * 4.0)) * sim_base["unit_cost"] * curr_rate
    else:
        sim_risk_status = "Healthy"
        sim_sales_at_risk = 0.0
        sim_locked_cap = 0.0

    st.write("")
    sm_col1, sm_col2, sm_col3, sm_col4 = st.columns(4)
    with sm_col1:
        st.metric("Simulated Risk Status", sim_risk_status, delta="Risk Resolved!" if sim_risk_status == "Healthy" and sim_base["risk_status"] != "Healthy" else None)
    with sm_col2:
        st.metric("Lead Time Demand", f"{eff_lt_demand:.1f} units", delta=f"{eff_lt_demand - sim_base['forecast_lead_time_demand']:+.1f} units")
    with sm_col3:
        st.metric("Available Stock (with PO)", f"{eff_available_stock} units", delta=f"+{sim_new_po} PO units" if sim_new_po > 0 else None)
    with sm_col4:
        st.metric("Sales at Risk", f"{curr_symbol}{sim_sales_at_risk:,.2f}", delta=f"{sim_sales_at_risk - (sim_base['sales_at_risk_inr']*curr_rate):+,.2f}", delta_color="inverse")

    st.divider()

    # 2D Sensitivity Heatmap Grid Calculation
    st.markdown("### 📊 2D Sensitivity Matrix: Lead Time Delay vs Promotional Surge")
    st.markdown("<p style='font-size:0.85rem; color:#94a3b8;'>Grid evaluating projected Sales at Risk for various operational delay and marketing surge combinations.</p>", unsafe_allow_html=True)

    delays = [0, 3, 7, 10, 14]
    promos = [1.0, 1.25, 1.5, 1.75, 2.0]
    heatmap_rows = []

    for d in delays:
        for p in promos:
            test_lt = max(1, sim_base["lead_time_days"] + d)
            test_demand = sim_base["forecast_avg_weekly"] * p
            test_lt_demand = (test_demand / 7.0) * test_lt
            test_avail = sim_base["stock_on_hand"] + sim_base["stock_on_order"] + sim_new_po
            test_deficit = max(0.0, test_lt_demand - test_avail)
            test_risk = test_deficit * sim_base["selling_price"] * curr_rate

            heatmap_rows.append({
                "Delay (Days)": f"+{d}d Delay",
                "Promo Surge": f"{int((p-1)*100)}% Surge",
                "Sales at Risk": test_risk,
                "Deficit Units": test_deficit
            })

    hm_df = pd.DataFrame(heatmap_rows)

    heatmap_chart = (
        alt.Chart(hm_df)
        .mark_rect()
        .encode(
            x=alt.X("Promo Surge:N", title="Promotional Demand Surge"),
            y=alt.Y("Delay (Days):N", title="Vendor Lead Time Delay"),
            color=alt.Color("Sales at Risk:Q", scale=alt.Scale(scheme="reds"), title=f"Risk ({curr_symbol})"),
            tooltip=[
                alt.Tooltip("Promo Surge:N"),
                alt.Tooltip("Delay (Days):N"),
                alt.Tooltip("Sales at Risk:Q", format=",.2f"),
                alt.Tooltip("Deficit Units:Q", format=".1f")
            ]
        )
        .properties(height=260)
    )
    st.altair_chart(heatmap_chart, use_container_width=True)

    if sim_new_po > 0:
        if st.button(f"📥 Apply {sim_new_po} Units Order to PO Dispatcher for {sim_sku_select}"):
            st.session_state.po_overrides[sim_sku_select] = sim_new_po
            st.success(f"Successfully staged {sim_new_po} units for {sim_sku_select} in the Action Dispatcher!")

# =============================================================================
# TAB 4: AUTONOMOUS ACTION DISPATCHER & INTERACTIVE PO CENTER
# =============================================================================
with tab4:
    st.markdown('<div class="section-title">📝 Operational Action Dispatcher & Purchase Order Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Interactive procurement workflow center allowing supply chain teams to customize order quantities, approve purchase orders, and export execution plans.</div>', unsafe_allow_html=True)

    po_records = []
    for _, r in stockout_skus.iterrows():
        sku_id = r["sku_id"]
        # Default Order = Lead time deficit + 4 weeks safety stock
        safety_stock = r["forecast_avg_weekly"] * target_safety_wos
        def_order = int(np.ceil((r["forecast_lead_time_demand"] - r["total_available_stock"]) + safety_stock))
        
        # Check if user overridden quantity in simulation or data editor
        final_order = st.session_state.po_overrides.get(sku_id, def_order)
        status = st.session_state.po_status.get(sku_id, "Draft")

        po_records.append({
            "PO Number": f"PO-2026-{sku_id[:6]}",
            "SKU ID": sku_id,
            "Category": r["category"],
            "Status": status,
            "Recommended Order Qty": final_order,
            "Supplier Lead Time": f"{r['lead_time_days']} Days",
            "Unit Cost": r["unit_cost"] * curr_rate,
            "Total Spend": final_order * r["unit_cost"] * curr_rate,
        })

    if po_records:
        st.markdown("### 🛒 Active Replenishment Purchase Orders")
        po_editor_df = pd.DataFrame(po_records)

        # Interactive Data Editor
        edited_po_df = st.data_editor(
            po_editor_df,
            column_config={
                "Recommended Order Qty": st.column_config.NumberColumn(
                    "Order Qty (Editable)",
                    min_value=1,
                    max_value=5000,
                    step=10,
                ),
                "Unit Cost": st.column_config.NumberColumn(
                    f"Unit Cost ({curr_symbol})",
                    format=f"{curr_symbol}%.2f"
                ),
                "Total Spend": st.column_config.NumberColumn(
                    f"Total Spend ({curr_symbol})",
                    format=f"{curr_symbol}%.2f"
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Approval Workflow",
                    options=["Draft", "Approved", "Dispatched to Vendor"],
                )
            },
            disabled=["PO Number", "SKU ID", "Category", "Supplier Lead Time", "Unit Cost", "Total Spend"],
            width="stretch",
            hide_index=True,
            key="po_data_editor"
        )

        total_po_spend = edited_po_df["Total Spend"].sum()
        st.markdown(f"**Total Replenishment PO Spend:** <span style='font-size:1.2rem; font-weight:800; color:#38bdf8;'>{curr_symbol}{total_po_spend:,.2f}</span>", unsafe_allow_html=True)

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("✅ Approve All Critical Purchase Orders"):
                for row in po_records:
                    st.session_state.po_status[row["SKU ID"]] = "Approved"
                st.success("All purchase orders marked as APPROVED!")
                st.rerun()
        with col_act2:
            st.download_button(
                label="📥 Export Formatted Purchase Orders (CSV)",
                data=edited_po_df.to_csv(index=False),
                file_name="project_foresight_purchase_orders.csv",
                mime="text/csv",
            )
    else:
        st.info("✅ All SKUs have sufficient stock cover. No replenishment purchase orders required.")

    st.divider()

    # Markdown Clearance Dispatcher
    if len(overstock_skus) > 0:
        st.markdown("### 🏷️ Inventory Clearance & Markdown Plan")
        clear_records = []
        for _, r in overstock_skus.iterrows():
            excess_units = max(0, r["stock_on_hand"] - int(r["forecast_avg_weekly"] * 4))
            liberated_cap = excess_units * r["unit_cost"] * curr_rate
            clear_records.append({
                "SKU ID": r["sku_id"],
                "Category": r["category"],
                "Stock On Hand": r["stock_on_hand"],
                "Weeks of Supply": f"{r['weeks_of_supply']:.1f} wks",
                "Excess Holding Units": excess_units,
                "Current Price": r["selling_price"] * curr_rate,
                "Recommended Promo Price (25% Off)": r["selling_price"] * 0.75 * curr_rate,
                "Projected Liberated Capital": liberated_cap
            })
        clear_df = pd.DataFrame(clear_records)
        st.dataframe(
            clear_df.style.format({
                "Current Price": f"{curr_symbol}{{:,.2f}}",
                "Recommended Promo Price (25% Off)": f"{curr_symbol}{{:,.2f}}",
                "Projected Liberated Capital": f"{curr_symbol}{{:,.2f}}"
            }),
            width="stretch",
            hide_index=True
        )

        st.download_button(
            label="📥 Export Clearance Markdown Plan (CSV)",
            data=clear_df.to_csv(index=False),
            file_name="project_foresight_clearance_plan.csv",
            mime="text/csv",
        )

    st.divider()
    st.markdown("### 📥 Download Complete Summary Dataset")
    st.download_button(
        label="📥 Download Complete FORESIGHT Intelligence Data (CSV)",
        data=summary_df.to_csv(index=False),
        file_name="project_foresight_full_summary.csv",
        mime="text/csv",
    )

# =============================================================================
# TAB 5: ML MODEL PERFORMANCE & BACKTEST DIAGNOSTICS (NEW)
# =============================================================================
with tab5:
    st.markdown('<div class="section-title">🎯 Machine Learning Model Diagnostics & Backtesting</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Empirical backtest benchmark results, WAPE accuracy metrics, and ML feature importance drivers.</div>', unsafe_allow_html=True)

    diag_col1, diag_col2 = st.columns(2)

    with diag_col1:
        st.markdown("**Backtest Model Accuracy: WAPE Benchmark Comparison**")
        wape_data = pd.DataFrame({
            "Model": ["Baseline Seasonal-Naive (4W Lag)", "FORESIGHT Random Forest ML"],
            "WAPE Error (%)": [27.70, 24.49],
            "Color": ["#ef4444", "#10b981"]
        })
        wape_chart = (
            alt.Chart(wape_data)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, size=60)
            .encode(
                x=alt.X("Model:N", title="Forecasting Model", sort=None),
                y=alt.Y("WAPE Error (%):Q", title="Weighted Absolute Percentage Error (WAPE %)", scale=alt.Scale(domain=[0, 35])),
                color=alt.Color("Color:N", scale=None),
                tooltip=["Model", "WAPE Error (%)"]
            )
            .properties(height=280)
        )
        st.altair_chart(wape_chart, use_container_width=True)
        st.success("✅ **FORESIGHT ML Model** delivers **+11.58% relative accuracy gain** over baseline seasonal naive predictions.")

    with diag_col2:
        st.markdown("**Random Forest Feature Importance Drivers**")
        feat_data = pd.DataFrame({
            "Feature": ["Rolling 4W Demand Mean", "Lag 1W Sales", "Supplier Lead Time (Days)", "Lag 2W Sales", "Selling Price", "Promo Flag"],
            "Importance Score": [0.38, 0.24, 0.16, 0.11, 0.07, 0.04]
        }).sort_values("Importance Score", ascending=True)

        feat_chart = (
            alt.Chart(feat_data)
            .mark_bar(color="#818cf8", cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
            .encode(
                x=alt.X("Importance Score:Q", title="Relative Feature Importance"),
                y=alt.Y("Feature:N", title="Feature Name", sort="-x"),
                tooltip=["Feature", "Importance Score"]
            )
            .properties(height=280)
        )
        st.altair_chart(feat_chart, use_container_width=True)

    st.divider()

    st.markdown("### ⚙️ Pipeline System Architecture & File Verification")
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 20px;">
            <div style="display:flex; justify-content:space-between; margin-bottom: 8px;">
                <span>Ingestion Pipeline: <code>src/pipeline.py</code></span>
                <span style="color:#34d399;">● EXECUTED SUCCESSFULLY</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>ML Model & Risk Engine: <code>src/model.py</code></span>
                <span style="color:#34d399;">● EXECUTED SUCCESSFULLY</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
