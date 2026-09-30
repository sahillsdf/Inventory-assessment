
"""
FORESIGHT Dashboard — Streamlit app (v2, modern multi-page redesign)
Run with: streamlit run app.py
Expects in the same folder:
  - foresight.db                          (Step 8)
  - data/processed/foresight_clean.csv    (Step 1-2, used for calendar/season fields)
"""
#
# import sqlite3
# import numpy as np
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import streamlit as st
#
# DB_PATH = "foresight.db"
# CLEAN_CSV_PATH = "data/processed/foresight_clean.csv"
#
# # ---------- Design tokens ----------
# INK = "#0F172A"
# CANVAS = "#F8FAFC"
# INDIGO = "#4338CA"
# TEAL = "#0D9488"
# VIOLET = "#7C3AED"
# BLUE = "#2563EB"
# AMBER = "#D97706"
# ROSE = "#E11D48"
# SLATE = "#64748B"
# PALETTE = [INDIGO, TEAL, VIOLET, BLUE, AMBER, ROSE, SLATE]
#
# STATUS_COLORS = {
#     "Stockout Risk": ROSE, "Overstock": AMBER, "Healthy": TEAL,
#     "Reorder Immediately": ROSE, "Increase Stock": AMBER,
#     "Reduce Procurement": VIOLET, "Inventory Healthy": TEAL,
# }
#
# PAGE_ACCENTS = {
#     "Overview": INDIGO,
#     "Sales & Category": TEAL,
#     "Product Performance": VIOLET,
#     "Inventory Health": BLUE,
#     "Stock Risk": ROSE,
#     "Promotions & Seasonality": AMBER,
#     "Forecast & Recommendations": INDIGO,
# }
#
# st.set_page_config(page_title="FORESIGHT", layout="wide", page_icon="📦")
#
# st.markdown(f"""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
# html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
# .block-container {{ padding-top: 1.5rem; }}
# section[data-testid="stSidebar"] {{ background-color: {INK}; }}
# section[data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
# section[data-testid="stSidebar"] .stRadio > label {{ color: #94A3B8 !important; }}
# h1, h2, h3 {{ color: {INK}; font-weight: 600; }}
# .kpi-strip {{ display:flex; flex-wrap:wrap; gap: 36px; padding: 6px 0 24px 0;
#               border-bottom: 1px solid #E2E8F0; margin-bottom: 24px; }}
# .kpi-block {{ min-width: 130px; }}
# .kpi-value {{ font-size: 26px; font-weight:700; color:{INK};
#               font-variant-numeric: tabular-nums; border-bottom: 3px solid var(--accent);
#               padding-bottom:4px; display:inline-block; }}
# .kpi-label {{ font-size: 12.5px; color:{SLATE}; margin-top:5px; }}
# .section-header {{ border-left: 4px solid var(--accent); padding-left:12px; margin: 4px 0 16px 0; }}
# .section-header h3 {{ margin:0; }}
# .section-sub {{ color:{SLATE}; font-size: 13.5px; margin: -12px 0 18px 12px; }}
# </style>
# """, unsafe_allow_html=True)
#
#
# def kpi_strip(items, accent):
#     html = f'<div class="kpi-strip" style="--accent:{accent}">'
#     for value, label in items:
#         html += f'<div class="kpi-block"><div class="kpi-value">{value}</div><div class="kpi-label">{label}</div></div>'
#     html += "</div>"
#     st.markdown(html, unsafe_allow_html=True)
#
#
# def section_header(title, accent, subtitle=None):
#     st.markdown(f'<div class="section-header" style="--accent:{accent}"><h3>{title}</h3></div>', unsafe_allow_html=True)
#     if subtitle:
#         st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)
#
#
# def style_fig(fig, height=380):
#     fig.update_layout(
#         template="plotly_white", font_family="Inter", height=height,
#         margin=dict(t=40, l=10, r=10, b=10),
#         title_font_size=15, legend_title_text="",
#         plot_bgcolor=CANVAS, paper_bgcolor="white",
#     )
#     return fig
#
#
# # ---------- Data loading ----------
# @st.cache_data
# def load_data():
#     conn = sqlite3.connect(DB_PATH)
#     sales = pd.read_sql(
#         """SELECT s.*, p.Product_Name, p.Category, p.Subcategory, p.Cost_Price, p.Selling_Price
#            FROM Sales s JOIN Products p ON s.SKU = p.SKU""",
#         conn, parse_dates=["Date"],
#     )
#     products = pd.read_sql("SELECT * FROM Products", conn)
#     recs = pd.read_sql(
#         "SELECT r.*, p.Product_Name, p.Category FROM Recommendations r JOIN Products p ON r.SKU = p.SKU", conn
#     )
#     forecasts = pd.read_sql("SELECT * FROM Forecasts", conn, parse_dates=["Date"])
#     inventory = pd.read_sql(
#         "SELECT i.*, p.Category FROM Inventory i JOIN Products p ON i.SKU = p.SKU", conn, parse_dates=["Snapshot_Date"]
#     )
#     conn.close()
#     return sales, products, recs, forecasts, inventory
#
#
# @st.cache_data
# def load_calendar():
#     # Season/holiday/weekend fields live in the processed CSV, not the SQL schema
#     cols = ["Date", "SKU", "Units_Sold", "Revenue", "Category", "Promotion", "season", "is_holiday", "is_weekend"]
#     return pd.read_csv(CLEAN_CSV_PATH, parse_dates=["Date"])[cols]
#
#
# sales, products, recs, forecasts, inventory = load_data()
# calendar_df = load_calendar()
# recs["Days_Of_Stock"] = recs["Days_Of_Stock"].replace([np.inf, -np.inf], np.nan)
#
# # ---------- Sidebar navigation ----------
# st.sidebar.markdown("### 📦 FORESIGHT")
# st.sidebar.caption("Demand & Inventory Intelligence")
# page = st.sidebar.radio("Navigate", list(PAGE_ACCENTS.keys()), label_visibility="collapsed")
# accent = PAGE_ACCENTS[page]
#
# st.sidebar.markdown("---")
# categories = st.sidebar.multiselect("Filter by category", sorted(products["Category"].unique()),
#                                      default=sorted(products["Category"].unique()))
#
# sales_f = sales[sales["Category"].isin(categories)]
# recs_f = recs[recs["Category"].isin(categories)]
# calendar_f = calendar_df[calendar_df["Category"].isin(categories)]
# inventory_f = inventory[inventory["Category"].isin(categories)]
#
#
# # ================= PAGE: Overview =================
# if page == "Overview":
#     total_revenue = sales_f["Revenue"].sum()
#     total_units = sales_f["Units_Sold"].sum()
#     total_cost = (sales_f["Units_Sold"] * sales_f["Cost_Price"]).sum()
#     total_profit = total_revenue - total_cost
#     margin_pct = (total_profit / total_revenue * 100) if total_revenue else 0
#     asp = total_revenue / total_units if total_units else 0
#
#     section_header("Company overview", accent, "Two-year performance snapshot across the selected categories")
#     kpi_strip([
#         (f"₹{total_revenue/1e6:,.1f}M", "Total revenue"),
#         (f"₹{total_profit/1e6:,.1f}M", "Total profit"),
#         (f"{margin_pct:,.1f}%", "Gross margin"),
#         (f"{total_units/1e3:,.0f}K", "Units sold"),
#         (f"₹{asp:,.0f}", "Avg selling price"),
#     ], accent)
#
#     c1, c2 = st.columns([2, 1])
#     with c1:
#         trend = sales_f.groupby(sales_f["Date"].dt.to_period("M"))["Revenue"].sum().reset_index()
#         trend["Date"] = trend["Date"].dt.to_timestamp()
#         fig = px.area(trend, x="Date", y="Revenue", title="Monthly revenue trend")
#         fig.update_traces(line_color=INDIGO, fillcolor="rgba(67,56,202,0.12)")
#         st.plotly_chart(style_fig(fig), use_container_width=True)
#     with c2:
#         cat_rev = sales_f.groupby("Category")["Revenue"].sum().reset_index()
#         fig = px.pie(cat_rev, names="Category", values="Revenue", hole=0.55,
#                      color_discrete_sequence=PALETTE, title="Revenue by category")
#         st.plotly_chart(style_fig(fig), use_container_width=True)
#
#     top_prod = sales_f.groupby(["SKU", "Product_Name"])["Revenue"].sum().nlargest(8).reset_index()
#     fig = px.bar(top_prod, x="Revenue", y="SKU", orientation="h", title="Top 8 SKUs by revenue",
#                  color_discrete_sequence=[INDIGO], hover_data=["Product_Name"])
#     fig.update_layout(yaxis=dict(categoryorder="total ascending"))
#     st.plotly_chart(style_fig(fig, 340), use_container_width=True)
#
#
# # ================= PAGE: Sales & Category =================
# elif page == "Sales & Category":
#     yearly = sales_f.groupby(sales_f["Date"].dt.year)["Revenue"].sum()
#     yoy = ((yearly.iloc[-1] / yearly.iloc[0]) - 1) * 100 if len(yearly) > 1 else 0
#
#     section_header("Sales & category performance", accent, "Revenue trend and category/subcategory breakdown")
#     kpi_strip([
#         (f"₹{sales_f['Revenue'].sum()/1e6:,.1f}M", "Total revenue"),
#         (f"{yoy:+.1f}%", "Revenue YoY"),
#         (f"{sales_f['Units_Sold'].sum()/1e3:,.0f}K", "Units sold"),
#         (f"₹{sales_f.groupby(sales_f['Date'].dt.date)['Revenue'].sum().mean():,.0f}", "Avg daily revenue"),
#     ], accent)
#
#     sales_f = sales_f.copy()
#     sales_f["Year"] = sales_f["Date"].dt.year
#     sales_f["MonthNum"] = sales_f["Date"].dt.month
#     monthly_by_year = sales_f.groupby(["Year", "MonthNum"])["Revenue"].sum().reset_index()
#     fig = px.line(monthly_by_year, x="MonthNum", y="Revenue", color="Year", markers=True,
#                   color_discrete_sequence=[INDIGO, TEAL], title="Monthly revenue — year over year")
#     fig.update_xaxes(dtick=1, title="Month")
#     st.plotly_chart(style_fig(fig), use_container_width=True)
#
#     c1, c2 = st.columns(2)
#     with c1:
#         cat = sales_f.groupby("Category")["Revenue"].sum().sort_values(ascending=False).reset_index()
#         fig = px.bar(cat, x="Category", y="Revenue", title="Revenue by category", color_discrete_sequence=[TEAL])
#         st.plotly_chart(style_fig(fig, 330), use_container_width=True)
#     with c2:
#         subcat = sales_f.groupby("Subcategory")["Revenue"].sum().sort_values(ascending=False).head(12).reset_index()
#         fig = px.bar(subcat, x="Revenue", y="Subcategory", orientation="h", title="Top subcategories by revenue",
#                      color_discrete_sequence=[VIOLET])
#         fig.update_layout(yaxis=dict(categoryorder="total ascending"))
#         st.plotly_chart(style_fig(fig, 330), use_container_width=True)
#
#
# # ================= PAGE: Product Performance =================
# elif page == "Product Performance":
#     per_sku = sales_f.groupby(["SKU", "Product_Name", "Category"]).agg(
#         Revenue=("Revenue", "sum"), Units=("Units_Sold", "sum")
#     ).reset_index()
#     per_sku = per_sku.merge(products[["SKU", "Cost_Price"]], on="SKU", how="left")
#     per_sku["Profit"] = per_sku["Revenue"] - per_sku["Units"] * per_sku["Cost_Price"]
#     per_sku["Margin_Pct"] = (per_sku["Profit"] / per_sku["Revenue"] * 100).round(1)
#     low_threshold = per_sku["Revenue"].quantile(0.25)
#     low_performers = (per_sku["Revenue"] < low_threshold).sum()
#
#     section_header("Product performance", accent, "Revenue, profitability, and margin by SKU")
#     kpi_strip([
#         (f"{len(per_sku)}", "Total SKUs"),
#         (f"₹{per_sku['Revenue'].mean()/1e3:,.0f}K", "Avg SKU revenue"),
#         (f"₹{per_sku['Revenue'].max()/1e6:,.1f}M", "Top SKU revenue"),
#         (f"{low_performers}", "Low performers (bottom 25%)"),
#     ], accent)
#
#     fig = px.scatter(per_sku, x="Revenue", y="Margin_Pct", size="Units", color="Category",
#                       hover_data=["SKU", "Product_Name"], color_discrete_sequence=PALETTE,
#                       title="Revenue vs. gross margin (bubble size = units sold)")
#     st.plotly_chart(style_fig(fig, 400), use_container_width=True)
#
#     st.dataframe(
#         per_sku.sort_values("Revenue", ascending=False).head(15)
#         [["SKU", "Product_Name", "Category", "Revenue", "Units", "Profit", "Margin_Pct"]]
#         .style.format({"Revenue": "₹{:,.0f}", "Profit": "₹{:,.0f}", "Margin_Pct": "{:.1f}%"}),
#         use_container_width=True, hide_index=True,
#     )
#
#
# # ================= PAGE: Inventory Health =================
# elif page == "Inventory Health":
#     latest_inv = inventory_f.sort_values("Snapshot_Date").groupby("SKU").tail(1)
#     avg_total_inv = inventory_f.groupby("Snapshot_Date")["Current_Stock"].sum().mean()
#     n_years = (sales_f["Date"].max() - sales_f["Date"].min()).days / 365.25
#     turnover = (sales_f["Units_Sold"].sum() / n_years) / avg_total_inv if avg_total_inv else 0
#
#     section_header("Inventory health", accent, "Stock position, value, and coverage across the network")
#     kpi_strip([
#         (f"{latest_inv['Current_Stock'].sum():,.0f}", "On-hand units"),
#         (f"{latest_inv['On_Order'].sum():,.0f}", "On-order units"),
#         (f"₹{latest_inv['Inventory_Value'].sum()/1e6:,.2f}M", "Inventory value"),
#         (f"{turnover:,.1f}x", "Turnover (annualized, units basis)"),
#         (f"{recs_f['Days_Of_Stock'].median():,.1f}d", "Median days of cover"),
#     ], accent)
#
#     c1, c2 = st.columns(2)
#     with c1:
#         inv_by_cat = latest_inv.groupby("Category")["Inventory_Value"].sum().reset_index()
#         fig = px.treemap(inv_by_cat, path=["Category"], values="Inventory_Value",
#                           color="Inventory_Value", color_continuous_scale=[CANVAS, BLUE],
#                           title="Inventory value by category")
#         st.plotly_chart(style_fig(fig, 360), use_container_width=True)
#     with c2:
#         doc = recs_f.groupby("Category")["Days_Of_Stock"].median().sort_values().reset_index()
#         fig = px.bar(doc, x="Days_Of_Stock", y="Category", orientation="h",
#                      title="Median days of cover by category", color_discrete_sequence=[BLUE])
#         st.plotly_chart(style_fig(fig, 360), use_container_width=True)
#
#     fig = px.scatter(recs_f, x="Reorder_Point_Calc", y="Current_Stock", color="Risk_Status",
#                       hover_data=["SKU", "Product_Name"], color_discrete_map=STATUS_COLORS,
#                       title="On-hand stock vs. reorder point, by SKU")
#     fig.add_shape(type="line", x0=0, y0=0, x1=recs_f["Reorder_Point_Calc"].max(),
#                   y1=recs_f["Reorder_Point_Calc"].max(), line=dict(color=SLATE, dash="dot"))
#     st.plotly_chart(style_fig(fig, 380), use_container_width=True)
#
#
# # ================= PAGE: Stock Risk =================
# elif page == "Stock Risk":
#     counts = recs_f["Risk_Status"].value_counts()
#
#     section_header("Stock risk", accent, "SKUs classified by demand-forecast-driven reorder logic")
#     kpi_strip([
#         (f"{int(counts.get('Stockout Risk', 0))}", "Stockout risk"),
#         (f"{int(counts.get('Overstock', 0))}", "Overstock"),
#         (f"{int(counts.get('Healthy', 0))}", "Healthy"),
#         (f"{recs_f.loc[recs_f['Risk_Status']=='Stockout Risk','Days_Of_Stock'].median():,.1f}d"
#          if counts.get("Stockout Risk", 0) else "—", "Median days left (at-risk)"),
#     ], accent)
#
#     c1, c2 = st.columns([1, 1.4])
#     with c1:
#         fig = px.pie(counts.reset_index(), names="Risk_Status", values="count", hole=0.55,
#                      color="Risk_Status", color_discrete_map=STATUS_COLORS, title="Risk distribution")
#         st.plotly_chart(style_fig(fig, 340), use_container_width=True)
#     with c2:
#         rate = recs_f.groupby("Category")["Risk_Status"].apply(
#             lambda s: (s == "Stockout Risk").mean() * 100
#         ).sort_values(ascending=False).reset_index(name="Stockout_Rate")
#         fig = px.bar(rate, x="Stockout_Rate", y="Category", orientation="h", color_discrete_sequence=[ROSE],
#                      title="Stockout rate by category (%)")
#         st.plotly_chart(style_fig(fig, 340), use_container_width=True)
#
#     section_header("Risk matrix", accent)
#     table = recs_f[["SKU", "Product_Name", "Current_Stock", "Reorder_Point_Calc", "Days_Of_Stock", "Risk_Status"]] \
#         .sort_values("Days_Of_Stock", na_position="last")
#
#     def _row_color(row):
#         return [f"background-color: {STATUS_COLORS.get(row['Risk_Status'], '')}22"] * len(row)
#
#     st.dataframe(table.style.apply(_row_color, axis=1), use_container_width=True, hide_index=True)
#
#
# # ================= PAGE: Promotions & Seasonality =================
# elif page == "Promotions & Seasonality":
#     promo = calendar_f[calendar_f["Promotion"] == 1]
#     non_promo = calendar_f[calendar_f["Promotion"] == 0]
#     uplift = ((promo["Units_Sold"].mean() / non_promo["Units_Sold"].mean()) - 1) * 100 if len(non_promo) else 0
#     asp_promo = promo["Revenue"].sum() / promo["Units_Sold"].sum() if promo["Units_Sold"].sum() else 0
#
#     section_header("Promotions & seasonality", accent, "How promotions and time-of-year affect demand")
#     kpi_strip([
#         (f"₹{promo['Revenue'].sum()/1e6:,.1f}M", "Promo revenue"),
#         (f"{promo['Units_Sold'].sum()/1e3:,.0f}K", "Promo units"),
#         (f"{uplift:+.1f}%", "Promo uplift vs. baseline"),
#         (f"₹{asp_promo:,.0f}", "Promo avg. selling price"),
#     ], accent)
#
#     c1, c2 = st.columns(2)
#     with c1:
#         ptrend = promo.groupby(promo["Date"].dt.to_period("M"))["Revenue"].sum().reset_index()
#         ptrend["Date"] = ptrend["Date"].dt.to_timestamp()
#         fig = px.line(ptrend, x="Date", y="Revenue", markers=True, title="Promotion revenue trend",
#                       color_discrete_sequence=[AMBER])
#         st.plotly_chart(style_fig(fig, 340), use_container_width=True)
#     with c2:
#         season_order = ["Winter", "Spring", "Summer", "Monsoon", "Autumn"]
#         season = calendar_f.groupby("season")["Units_Sold"].sum().reindex(
#             [s for s in season_order if s in calendar_f["season"].unique()]
#         ).reset_index()
#         fig = px.bar(season, x="season", y="Units_Sold", title="Demand by season", color_discrete_sequence=[TEAL])
#         st.plotly_chart(style_fig(fig, 340), use_container_width=True)
#
#     holiday = calendar_f.groupby("is_holiday")["Units_Sold"].mean().reset_index()
#     holiday["is_holiday"] = holiday["is_holiday"].map({0: "Non-holiday", 1: "Holiday"})
#     fig = px.bar(holiday, x="is_holiday", y="Units_Sold", title="Avg daily demand: holiday vs. non-holiday",
#                  color_discrete_sequence=[VIOLET])
#     st.plotly_chart(style_fig(fig, 320), use_container_width=True)
#
#
# # ================= PAGE: Forecast & Recommendations =================
# elif page == "Forecast & Recommendations":
#     dist = recs_f["Recommendation"].value_counts()
#
#     section_header("Forecast & recommendations", accent, "Model-driven demand forecasts and reorder actions")
#     kpi_strip([
#         (f"{int(dist.get('Reorder Immediately', 0))}", "Reorder immediately"),
#         (f"{int(dist.get('Increase Stock', 0))}", "Increase stock"),
#         (f"{int(dist.get('Reduce Procurement', 0))}", "Reduce procurement"),
#         (f"{int(dist.get('Inventory Healthy', 0))}", "Inventory healthy"),
#     ], accent)
#
#     c1, c2 = st.columns([1.4, 1])
#     with c1:
#         fc_skus = sorted(forecasts["SKU"].unique())
#         chosen = st.selectbox("Select a SKU to inspect its forecast", fc_skus)
#         sku_fc = forecasts[forecasts["SKU"] == chosen].sort_values("Date")
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=sku_fc["Date"], y=sku_fc["Actual_Demand"], name="Actual", line=dict(color=INK)))
#         fig.add_trace(go.Scatter(x=sku_fc["Date"], y=sku_fc["Forecast_Demand"], name="Forecast", line=dict(color=INDIGO, dash="dash")))
#         fig.update_layout(title=f"{chosen} — actual vs. forecast demand")
#         st.plotly_chart(style_fig(fig, 360), use_container_width=True)
#         mae = (sku_fc["Actual_Demand"] - sku_fc["Forecast_Demand"]).abs().mean()
#         st.caption(f"Mean absolute error for {chosen}: **{mae:.2f} units/day**")
#     with c2:
#         fig = px.pie(dist.reset_index(), names="Recommendation", values="count", hole=0.55,
#                      color="Recommendation", color_discrete_map=STATUS_COLORS, title="Recommendation mix")
#         st.plotly_chart(style_fig(fig, 360), use_container_width=True)
#
#     section_header("Executive action table", accent)
#     rec_filter = st.multiselect("Filter by recommendation", sorted(recs_f["Recommendation"].unique()),
#                                  default=sorted(recs_f["Recommendation"].unique()))
#     table = recs_f[recs_f["Recommendation"].isin(rec_filter)][
#         ["SKU", "Product_Name", "Category", "Current_Stock", "On_Order", "Recommendation", "Recommended_Qty", "Days_Of_Stock"]
#     ].sort_values("Days_Of_Stock", na_position="last")
#     st.dataframe(table, use_container_width=True, hide_index=True)
#
# st.sidebar.markdown("---")
# st.sidebar.caption("FORESIGHT · Demand & Inventory Intelligence")



import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# FORESIGHT — Power BI reference-matched Streamlit dashboard
# 12 pages / sections matching "Dashboards PDF.pdf"
# ============================================================

DB_PATH = "foresight.db"
CLEAN_CSV_PATH = "data/processed/foresight_clean.csv"

# ---------- Theme / design tokens ----------
BG = "#F7F7F5"
WHITE = "#FFFFFF"
INK = "#202020"
MUTED = "#6B6B6B"
BORDER = "#C9C9C9"

#PAGE_COLORS = {
 #   "Company Overview": "#536B35",
  #  "Sales Performance": "#E6C82F",#16A34A
 #   "Product Performance": "#E48CC5",
  #  "Category Performance": "#49A3E8",
  #  "Inventory Health": "#F0A486",
   # "Stock Risk": "#E56D77",
    #"Overstock": "#49A3E8",
   # "Promotion Analysis": "#536B35",
  #  "Seasonality": "#E6C82F",
   # "Forecast": "#E48CC5",
   # "Customer & Business Insights": "#F0A486",
   # "Recommendation": "#A85B5B",
#}

PAGE_COLORS = {
    "Company Overview": "#2563EB",                 # Blue
    "Sales Performance": "#16A34A",                # Green
    "Product Performance": "#7C3AED",             # Purple
    "Category Performance": "#0891B2",             # Cyan
    "Inventory Health": "#0F766E",                 # Teal
    "Stock Risk": "#DC2626",                      # Red
    "Overstock": "#EA580C",                       # Orange
    "Promotion Analysis": "#059669",              # Emerald
    "Seasonality": "#CA8A04",                     # Gold
    "Forecast": "#9333EA",                        # Violet
    "Customer & Business Insights": "#0284C7",    # Sky Blue
    "Recommendation": "#BE123C",                  # Rose
}

CATEGORY_ORDER = ["Kitchen", "Textiles", "Decor", "Lighting", "Furniture", "Storage"]
MONTHS = list(range(1, 13))

st.set_page_config(
    page_title="FORESIGHT",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- CSS ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: Inter, Arial, sans-serif;
}}
.stApp {{
    background: {BG};
}}
.block-container {{
    max-width: 1600px;
    padding-top: 1.1rem;
    padding-bottom: 1.5rem;
}}
section[data-testid="stSidebar"] {{
    background: #1E241D;
}}
section[data-testid="stSidebar"] * {{
    color: #F1F4EC !important;
}}
section[data-testid="stSidebar"] .stRadio label {{
    font-size: 13px;
}}
h1, h2, h3, h4 {{
    color: {INK};
}}
div[data-testid="stMetric"] {{
    background: transparent;
}}
div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: {BORDER};
}}
.dashboard-title {{
    height: 76px;
    border: 1px solid #BEBEBE;
    border-radius: 14px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:800;
    font-size:28px;
    text-transform:uppercase;
    text-decoration:underline;
    letter-spacing:.3px;
    margin-bottom:10px;
    box-shadow: 0 2px 3px rgba(0,0,0,.08);
}}
.kpi-card {{
    min-height: 88px;
    border: 1px solid #AFAFAF;
    border-radius: 12px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    padding:8px 7px;
    box-shadow: 0 2px 4px rgba(0,0,0,.10);
    background: #FFF;
}}
.kpi-value {{
    font-size: 24px;
    line-height: 1.05;
    font-weight:800;
    color:{INK};
}}
.kpi-label {{
    font-size:11px;
    line-height:1.15;
    color:{MUTED};
    margin-top:5px;
}}
.panel {{
    background:#FFF;
    border:1px solid #C9C9C9;
    border-radius:11px;
    padding:8px 10px 4px 10px;
    box-shadow:0 1px 2px rgba(0,0,0,.06);
}}
.filter-caption {{
    font-size:10px;
    color:#555;
    margin-bottom:1px;
}}
.small-note {{
    font-size:11px;
    color:#777;
}}
[data-testid="stDataFrame"] {{
    border:1px solid #C9C9C9;
    border-radius:10px;
}}
.stButton button {{
    border-radius:8px;
}}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    sales = pd.read_sql(
        """
        SELECT s.*, p.Product_Name, p.Category, p.Subcategory,
               p.Cost_Price, p.Selling_Price
        FROM Sales s
        JOIN Products p ON s.SKU = p.SKU
        """,
        conn,
        parse_dates=["Date"],
    )

    products = pd.read_sql("SELECT * FROM Products", conn)

    recs = pd.read_sql(
        """
        SELECT r.*, p.Product_Name, p.Category, p.Subcategory,
               p.Cost_Price, p.Selling_Price
        FROM Recommendations r
        JOIN Products p ON r.SKU = p.SKU
        """,
        conn,
    )

    forecasts = pd.read_sql(
        "SELECT * FROM Forecasts",
        conn,
        parse_dates=["Date"],
    )

    inventory = pd.read_sql(
        """
        SELECT i.*, p.Product_Name, p.Category, p.Subcategory
        FROM Inventory i
        JOIN Products p ON i.SKU = p.SKU
        """,
        conn,
        parse_dates=["Snapshot_Date"],
    )

    conn.close()
    return sales, products, recs, forecasts, inventory


@st.cache_data
def load_calendar():
    p = Path(CLEAN_CSV_PATH)
    if not p.exists():
        return pd.DataFrame()
    cols = [
        "Date", "SKU", "Units_Sold", "Revenue", "Category",
        "Promotion", "season", "is_holiday", "is_weekend"
    ]
    df = pd.read_csv(p, parse_dates=["Date"])
    return df[[c for c in cols if c in df.columns]]


try:
    sales, products, recs, forecasts, inventory = load_data()
except Exception as e:
    st.error(
        "Could not load the FORESIGHT database. Put foresight.db in the app "
        "directory and ensure the Sales, Products, Recommendations, Forecasts "
        "and Inventory tables exist."
    )
    st.exception(e)
    st.stop()

calendar_df = load_calendar()

for df in (sales, products, recs, forecasts, inventory, calendar_df):
    if isinstance(df, pd.DataFrame):
        for c in df.columns:
            if c in ["Revenue", "Units_Sold", "Cost_Price", "Selling_Price",
                     "Current_Stock", "On_Order", "Inventory_Value",
                     "Forecast_Demand", "Actual_Demand", "Days_Of_Stock",
                     "Reorder_Point_Calc", "Recommended_Qty",
                     "Excess_Inventory_Units", "Excess_Inventory_Value"]:
                df[c] = pd.to_numeric(df[c], errors="coerce")


# ============================================================
# HELPERS
# ============================================================

def safe_col(df, candidates, default=np.nan):
    for c in candidates:
        if c in df.columns:
            return df[c]
    return pd.Series(default, index=df.index)


def val(df, column, default=0):
    if column not in df.columns or len(df) == 0:
        return default
    x = pd.to_numeric(df[column], errors="coerce")
    return float(x.sum()) if len(x) else default


def mean_val(df, column, default=0):
    if column not in df.columns or len(df) == 0:
        return default
    x = pd.to_numeric(df[column], errors="coerce").dropna()
    return float(x.mean()) if len(x) else default


def latest_inventory(inv):
    if inv.empty or "Snapshot_Date" not in inv.columns:
        return inv.copy()
    return inv.sort_values("Snapshot_Date").groupby("SKU", as_index=False).tail(1)


def fmt_money(x, decimals=2):
    x = float(x or 0)
    a = abs(x)
    if a >= 1e9:
        return f"₹{x/1e9:.{decimals}f}B"
    if a >= 1e6:
        return f"₹{x/1e6:.{decimals}f}M"
    if a >= 1e3:
        return f"₹{x/1e3:.{decimals}f}K"
    return f"₹{x:,.0f}"


def fmt_num(x):
    x = float(x or 0)
    a = abs(x)
    if a >= 1e9:
        return f"{x/1e9:.2f}B"
    if a >= 1e6:
        return f"{x/1e6:.2f}M"
    if a >= 1e3:
        return f"{x/1e3:.2f}K"
    return f"{x:,.0f}"


def fmt_pct(x, decimals=2):
    return f"{float(x or 0):.{decimals}f}%"


def card(value, label, accent):
    st.markdown(
        f"""
        <div class="kpi-card" style="background:{accent}22;">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def title_bar(title, accent):
    st.markdown(
        f'<div class="dashboard-title" style="background:{accent};">{title}</div>',
        unsafe_allow_html=True,
    )


def panel_title(title):
    st.markdown(
        f'<div style="font-size:12px;font-weight:700;text-align:center;margin:2px 0 4px;">{title}</div>',
        unsafe_allow_html=True,
    )


def chart(fig, height=300):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(t=35, l=8, r=8, b=8),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", size=10, color=INK),
        legend=dict(font=dict(size=9)),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EEEEEE")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def apply_filters(df, date_col=None):
    out = df.copy()
    if date_col and date_col in out.columns and selected_date is not None:
        out = out[
            (out[date_col].dt.date >= selected_date[0]) &
            (out[date_col].dt.date <= selected_date[1])
        ]
    if "Category" in out.columns and selected_categories:
        out = out[out["Category"].isin(selected_categories)]
    if "Subcategory" in out.columns and selected_subcategories:
        out = out[out["Subcategory"].isin(selected_subcategories)]
    return out


def empty_chart(message="No data available"):
    fig = go.Figure()
    fig.add_annotation(text=message, x=.5, y=.5, xref="paper", yref="paper",
                       showarrow=False, font=dict(size=14, color=MUTED))
    chart(fig, 260)


def monthly_series(df, value_col, date_col="Date"):
    if df.empty or date_col not in df.columns or value_col not in df.columns:
        return pd.DataFrame(columns=["Date", value_col])
    x = df.dropna(subset=[date_col]).copy()
    x["Month"] = x[date_col].dt.to_period("M").dt.to_timestamp()
    return x.groupby("Month", as_index=False)[value_col].sum().rename(columns={"Month": "Date"})


def category_sum(df, column):
    if df.empty or "Category" not in df.columns or column not in df.columns:
        return pd.DataFrame(columns=["Category", column])
    return df.groupby("Category", as_index=False)[column].sum().sort_values(column, ascending=False)


def kpi_row(items, accent, widths=None):
    # Keep KPI cards at a usable width. Never put a multi-card KPI row
    # inside a narrow chart column; call this before the chart layout.
    cols = st.columns(widths or [1] * len(items), gap="small")
    for c, (v, label) in zip(cols, items):
        with c:
            card(v, label, accent)


def filter_row(show_date=True, show_category=True, show_subcategory=True,
               show_product=False, show_sku=False, show_year=False):
    global selected_date, selected_categories, selected_subcategories

    cols = []
    if show_date:
        cols.append("date")
    if show_category:
        cols.append("category")
    if show_subcategory:
        cols.append("subcategory")
    if show_product:
        cols.append("product")
    if show_sku:
        cols.append("sku")
    if show_year:
        cols.append("year")

    cc = st.columns(len(cols))
    for c, typ in zip(cc, cols):
        with c:
            if typ == "date":
                d = date_minmax()
                selected_date = st.date_input(
                    "Date",
                    value=d,
                    min_value=d[0],
                    max_value=d[1],
                    key=f"date_{st.session_state.get('_page_key','x')}",
                )
                if isinstance(selected_date, tuple) and len(selected_date) == 2:
                    pass
                else:
                    selected_date = d
            elif typ == "category":
                selected_categories = st.multiselect(
                    "Category",
                    sorted(products["Category"].dropna().unique()) if "Category" in products else [],
                    default=sorted(products["Category"].dropna().unique()) if "Category" in products else [],
                    key=f"cat_{st.session_state.get('_page_key','x')}",
                )
            elif typ == "subcategory":
                options = sorted(products["Subcategory"].dropna().unique()) if "Subcategory" in products else []
                selected_subcategories = st.multiselect(
                    "Subcategory", options, default=options,
                    key=f"sub_{st.session_state.get('_page_key','x')}",
                )
            elif typ == "product":
                opts = sorted(products["Product_Name"].dropna().unique()) if "Product_Name" in products else []
                st.multiselect("Products", opts, default=opts, key=f"prod_{st.session_state.get('_page_key','x')}")
            elif typ == "sku":
                opts = sorted(products["SKU"].dropna().unique()) if "SKU" in products else []
                st.multiselect("SKU", opts, default=opts, key=f"sku_{st.session_state.get('_page_key','x')}")
            elif typ == "year":
                opts = sorted(sales["Date"].dt.year.dropna().unique()) if "Date" in sales else []
                st.multiselect("Year", opts, default=opts, key=f"year_{st.session_state.get('_page_key','x')}")


def date_minmax():
    if "Date" in sales.columns and sales["Date"].notna().any():
        return (sales["Date"].min().date(), sales["Date"].max().date())
    from datetime import date
    return (date(2024, 1, 1), date(2025, 12, 31))


# ============================================================
# SIDEBAR
# ============================================================

PAGES = [
    "Company Overview",
    "Sales Performance",
    "Product Performance",
    "Category Performance",
    "Inventory Health",
    "Stock Risk",
    "Overstock",
    "Promotion Analysis",
    "Seasonality",
    "Forecast",
    "Customer & Business Insights",
    "Recommendation",
]

st.sidebar.markdown("## 📦 Inventory Dashboard")
st.sidebar.caption("Demand & Inventory Intelligence")
page = st.sidebar.radio("Dashboard pages", PAGES)

# page-local state
st.session_state["_page_key"] = page.replace(" ", "_")
selected_date = date_minmax()
selected_categories = sorted(products["Category"].dropna().unique()) if "Category" in products else []
selected_subcategories = sorted(products["Subcategory"].dropna().unique()) if "Subcategory" in products else []

# ============================================================
# 1 — COMPANY OVERVIEW
# ============================================================

if page == "Company Overview":
    accent = PAGE_COLORS[page]
    title_bar("COMPANY OVERVIEW", accent)

    sf = sales.copy()
    revenue = val(sf, "Revenue")
    units = val(sf, "Units_Sold")
    profit = revenue - val(sf.assign(Cost=sf["Units_Sold"] * sf["Cost_Price"]), "Cost")
    asp = revenue / units if units else 0
    inv_latest = latest_inventory(inventory)
    inv_value = val(inv_latest, "Inventory_Value")
    turnover = units / inv_value if inv_value else 0

    kpi_row([
        (fmt_money(revenue), "Total Revenue"),
        (fmt_money(profit), "Total Profit"),
        (f"{turnover:.2f}", "Inventory Turnover"),
        (fmt_money(inv_value), "Inventory Value"),
        (f"{asp:,.2f}", "Average Selling Price"),
        (fmt_num(units), "Total Units Sold"),
    ], accent)

    main = st.container()
    with main:
        c1, c2 = st.columns([1.25, 1.15])
        with c1:
            m = monthly_series(sf, "Revenue")
            if not m.empty:
                fig = px.area(m, x="Date", y="Revenue", title="Revenue Trends")
                fig.update_traces(line_color=accent, fillcolor="#B8C7A2")
                chart(fig, 310)
            else:
                empty_chart()
        with c2:
            cat = category_sum(sf, "Revenue")
            if not cat.empty:
                fig = px.pie(cat, names="Category", values="Revenue", hole=.55,
                             title="Total Revenue by category")
                chart(fig, 310)
            else:
                empty_chart()

        c3, c4 = st.columns([1.25, 1.15])
        with c3:
            top = sf.groupby("Product_Name", as_index=False)["Revenue"].sum().nlargest(10, "Revenue")
            fig = px.bar(top.sort_values("Revenue"), x="Revenue", y="Product_Name",
                         orientation="h", title="Top 10 Products by Revenue")
            fig.update_traces(marker_color=accent)
            chart(fig, 310)
        with c4:
            sm = monthly_series(sf, "Revenue")
            fig = px.bar(sm, x="Date", y="Revenue", title="Sales by Month")
            fig.update_traces(marker_color=accent)
            chart(fig, 310)

    st.markdown("#### Filters")
    filter_row(show_date=False, show_category=True, show_subcategory=True)

# ============================================================
# 2 — SALES PERFORMANCE
# ============================================================

elif page == "Sales Performance":
    accent = PAGE_COLORS[page]
    title_bar("SALES PERFORMANCE", accent)

    revenue = val(sales, "Revenue")
    units = val(sales, "Units_Sold")
    years = sales.groupby(sales["Date"].dt.year)["Revenue"].sum() if "Date" in sales else pd.Series()
    yoy = ((years.iloc[-1] / years.iloc[0]) - 1) * 100 if len(years) >= 2 and years.iloc[0] else 0
    profit = revenue - val(sales.assign(Cost=sales["Units_Sold"] * sales["Cost_Price"]), "Cost")
    margin = profit / revenue * 100 if revenue else 0
    asp = revenue / units if units else 0

    kpi_row([
        (fmt_money(revenue), "Total Revenue"),
        (f"{asp:,.2f}", "Average Selling Price"),
        (fmt_money(profit), "Gross Profit"),
        (f"{margin:.2f}%", "Gross Margin %"),
        (fmt_num(units), "Total Units Sold"),
        (f"{yoy:.2f}", "Revenue YoY %"),
    ], accent)

    right = st.container()
    with right:
        m = sales.copy()
        m["Year"] = m["Date"].dt.year
        m["MonthNum"] = m["Date"].dt.month
        monthly = m.groupby(["Year", "MonthNum"], as_index=False)["Revenue"].sum()
        monthly["Month"] = monthly["MonthNum"].map({
            1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
            7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"
        })
        fig = px.line(monthly, x="MonthNum", y="Revenue", color="Year", markers=True,
                      title="Monthly Revenue Trend")
        chart(fig, 300)

        c1, c2 = st.columns([1, 1])
        with c1:
            cat = category_sum(sales, "Revenue")
            fig = px.bar(cat, x="Category", y="Revenue", title="Revenue by Category")
            fig.update_traces(marker_color=accent)
            chart(fig, 300)
        with c2:
            sub = sales.groupby("Subcategory", as_index=False)["Revenue"].sum().nlargest(20, "Revenue")
            fig = px.bar(sub.sort_values("Revenue"), x="Revenue", y="Subcategory",
                         orientation="h", title="Revenue by Subcategory")
            fig.update_traces(marker_color=accent)
            chart(fig, 420)

    st.markdown("#### Filters")
    filter_row(show_date=True, show_category=True, show_subcategory=True)

# ============================================================
# 3 — PRODUCT PERFORMANCE
# ============================================================

elif page == "Product Performance":
    accent = PAGE_COLORS[page]
    title_bar("PRODUCT PERFORMANCE", accent)

    per = sales.groupby(["SKU", "Product_Name", "Category"], as_index=False).agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Units_Sold=("Units_Sold", "sum"),
    )
    per = per.merge(products[["SKU", "Cost_Price"]], on="SKU", how="left")
    per["Total_Profit"] = per["Total_Revenue"] - per["Total_Units_Sold"] * per["Cost_Price"]
    per["Gross_Margin_Pct"] = np.where(
        per["Total_Revenue"] != 0,
        per["Total_Profit"] / per["Total_Revenue"] * 100, 0
    )
    low = int((per["Total_Revenue"] < per["Total_Revenue"].quantile(.25)).sum()) if len(per) else 0

    kpi_row([
        (f"{len(per):,}", "Total SKUs"),
        (fmt_money(per["Total_Revenue"].mean() if len(per) else 0), "Average SKU Revenue"),
        (fmt_money(per["Total_Revenue"].max() if len(per) else 0), "Top SKU Revenue"),
        (f"{low:,}", "Low Performing SKUs"),
        (f"{(per['Gross_Margin_Pct'].mean() if len(per) else 0):.2f}%", "Gross Margin %"),
    ], accent)

    main, right = st.columns([2.8, 1.25])
    with main:
        fig = px.scatter(
            per, x="Total_Revenue", y="Gross_Margin_Pct",
            size="Total_Units_Sold", color="Category",
            hover_data=["SKU", "Product_Name"],
            title="Product Revenue vs Gross Margin % (Top 20)",
        )
        chart(fig, 390)
        table = per.sort_values("Total_Revenue", ascending=False).head(20)
        table = table.rename(columns={
            "SKU":"Sku_id", "Total_Revenue":"Total Revenue",
            "Total_Units_Sold":"Total Units Sold",
            "Total_Profit":"Total Profit", "Gross_Margin_Pct":"Gross Margin %"
        })
        st.dataframe(
            table[["Sku_id","Product_Name","Total Revenue","Total Units Sold","Total Profit","Gross Margin %"]],
            use_container_width=True, hide_index=True
        )
    with right:
        top = per.nlargest(20, "Total_Revenue").sort_values("Total_Revenue")
        fig = px.bar(top, x="Total_Revenue", y="Product_Name", orientation="h",
                     title="Top 20 Products")
        fig.update_traces(marker_color=accent)
        chart(fig, 620)

    st.markdown("#### Filters")
    filter_row(show_date=True, show_category=True, show_subcategory=True)

# ============================================================
# 4 — CATEGORY PERFORMANCE
# ============================================================

elif page == "Category Performance":
    accent = PAGE_COLORS[page]
    title_bar("CATEGORY PERFORMANCE", accent)

    revenue = val(sales, "Revenue")
    units = val(sales, "Units_Sold")
    profit = revenue - val(sales.assign(Cost=sales["Units_Sold"] * sales["Cost_Price"]), "Cost")
    margin = profit / revenue * 100 if revenue else 0
    yearly = sales.groupby(sales["Date"].dt.year)["Revenue"].sum()
    growth = ((yearly.iloc[-1]/yearly.iloc[0])-1)*100 if len(yearly)>=2 and yearly.iloc[0] else 0
    contribution = 1.0

    kpi_row([
        (fmt_money(revenue), "Revenue"),
        (fmt_num(units), "Units Sold"),
        (fmt_money(profit), "Profit"),
        (f"{margin:.2f}%", "Margin %"),
        (f"{growth:.2f}%", "Revenue Growth %"),
        (f"{contribution:.2f}", "Category Contribution %"),
    ], accent)

    main = st.container()
    with main:
        c1, c2 = st.columns([1.15, 1])
        with c1:
            sub = sales.groupby("Subcategory", as_index=False)["Revenue"].sum().nlargest(5, "Revenue")
            fig = px.bar(sub.sort_values("Revenue"), x="Revenue", y="Subcategory",
                         orientation="h", title="Top 5 Subcategory")
            fig.update_traces(marker_color=accent)
            chart(fig, 260)
        with c2:
            cy = sales.copy()
            cy["Year"] = cy["Date"].dt.year
            cat_year = cy.groupby(["Category","Year"], as_index=False)["Revenue"].sum()
            piv = cat_year.pivot(index="Category", columns="Year", values="Revenue").fillna(0)
            growths = ((piv.iloc[:, -1]/piv.iloc[:, 0])-1)*100 if piv.shape[1]>=2 else pd.Series(0,index=piv.index)
            gd = growths.sort_values(ascending=False).reset_index(name="Growth")
            fig = px.bar(gd, x="Category", y="Growth", title="Category Growth")
            fig.update_traces(marker_color=accent)
            chart(fig, 260)

        cat = category_sum(sales, "Revenue")
        fig = px.bar(cat, x="Revenue", y="Category", orientation="h", title="Revenue by Category")
        fig.update_traces(marker_color=accent)
        chart(fig, 270)

        m = sales.copy()
        m["Month"] = m["Date"].dt.to_period("M").dt.to_timestamp()
        trend = m.groupby(["Month","Category"], as_index=False)["Revenue"].sum()
        fig = px.line(trend, x="Month", y="Revenue", color="Category", title="Category Trend")
        chart(fig, 300)

    st.markdown("#### Filters")
    filter_row(show_date=True, show_category=True, show_subcategory=True, show_sku=True)

# ============================================================
# 5 — INVENTORY HEALTH
# ============================================================

elif page == "Inventory Health":
    accent = PAGE_COLORS[page]
    title_bar("INVENTORY HEALTH", accent)

    li = latest_inventory(inventory)
    on_hand = val(li, "Current_Stock")
    on_order = val(li, "On_Order")
    inv_value = val(li, "Inventory_Value")
    potential = val(li, "Potential_Inventory_Value")
    turnover = val(sales, "Units_Sold") / inv_value if inv_value else 0
    days_cover = mean_val(recs, "Days_Of_Stock")
    avg_inv = mean_val(inventory, "Inventory_Value")

    kpi_row([
        (fmt_num(on_hand), "On Hand Units"),
        (fmt_money(avg_inv), "Average Inventory Value"),
        (fmt_money(inv_value), "Inventory Value"),
        (fmt_money(potential), "Potential Inventory Value"),
        (fmt_num(on_order), "On Order Units"),
        (f"{turnover:.2f}", "Inventory Turnover"),
        (f"{days_cover:.2f}", "Days Of Cover"),
    ], accent)

    main = st.container()
    with main:
        c1, c2 = st.columns([1, 1])
        with c1:
            inv_cat = category_sum(li, "Inventory_Value")
            fig = px.bar(inv_cat, x="Inventory_Value", y="Category", orientation="h",
                         title="Inventory by Category")
            fig.update_traces(marker_color=accent)
            chart(fig, 260)
        with c2:
            inv_cat = category_sum(li, "Inventory_Value")
            fig = px.treemap(inv_cat, path=["Category"], values="Inventory_Value",
                             title="Inventory Value by Category")
            chart(fig, 260)

        if not recs.empty:
            rec = recs.copy()
            doc = rec.groupby("Category", as_index=False)["Days_Of_Stock"].mean().sort_values("Days_Of_Stock")
            fig = px.bar(doc, x="Days_Of_Stock", y="Category", orientation="h",
                         title="Days of Cover by Category")
            fig.update_traces(marker_color=accent)
            chart(fig, 240)

            x = safe_col(rec, ["Reorder_Point_Calc","Reorder_Point"], 0)
            y = safe_col(rec, ["Current_Stock","On_Hand_Units"], 0)
            scatter = pd.DataFrame({"Reorder Point":x, "On Hand Units":y,
                                    "Category":safe_col(rec,["Category"],"")})
            fig = px.scatter(scatter, x="Reorder Point", y="On Hand Units",
                             color="Category", title="On-Hand Inventory vs Reorder Point — TOP 30")
            chart(fig, 300)

    st.markdown("#### Filters")
    filter_row(show_date=True, show_category=True, show_subcategory=True, show_sku=True)

# ============================================================
# 6 — STOCK RISK
# ============================================================

elif page == "Stock Risk":
    accent = PAGE_COLORS[page]
    title_bar("STOCK RISK", accent)

    risk = recs.copy()
    if "Risk_Status" not in risk.columns:
        risk["Risk_Status"] = "Healthy"
    counts = risk["Risk_Status"].fillna("Healthy").value_counts()
    stockout = int(counts.get("Stockout", counts.get("Stockout Risk", 0)))
    critical = int(counts.get("Critical", 0))
    high = int(counts.get("High", counts.get("High Risk", 0)))
    healthy = int(counts.get("Healthy", 0))
    daily = mean_val(risk, "Average_Daily_Demand")
    lead = mean_val(risk, "Lead_Time_Demand")

    # KPI cards span the full content width — matching the reference layout.
    kpi_row([
        (fmt_num(stockout), "Stockout SKUs"),
        (fmt_num(critical), "Critical SKUs"),
        (fmt_num(daily), "Daily Demand at Stockout Risk"),
        (fmt_num(lead), "Lead Time Demand"),
        (fmt_num(high), "High Risk SKUs"),
        (fmt_num(healthy), "Healthy SKUs"),
    ], accent)

    c1, c2 = st.columns([1, 1.3])
    with c1:
        rd = counts.reset_index()
        rd.columns = ["Risk Status", "Count"]
        fig = px.pie(rd, names="Risk Status", values="Count", hole=.55,
                     title="Risk Distribution")
        chart(fig, 270)
    with c2:
        rr = risk.copy()
        rr["Is_Stockout"] = rr["Risk_Status"].astype(str).str.lower().str.contains("stockout").astype(int)
        rate = rr.groupby("Category", as_index=False)["Is_Stockout"].mean()
        rate["Stockout Rate"] = rate["Is_Stockout"] * 100
        fig = px.bar(rate.sort_values("Stockout Rate"), x="Stockout Rate", y="Category",
                     orientation="h", title="Stockout Rate by Category %")
        fig.update_traces(marker_color=accent)
        chart(fig, 270)

    cols = [c for c in [
        "SKU","Current_Stock","Average_Daily_Demand","Days_Of_Stock",
        "Reorder_Point_Calc","Risk_Status"
    ] if c in risk.columns]
    table = risk[cols].copy().sort_values("Days_Of_Stock", na_position="last")
    st.markdown("**Risk Matrix**")
    st.dataframe(table, use_container_width=True, hide_index=True)

    st.markdown("#### Filters")
    filter_row(show_date=True, show_category=True, show_sku=True)

# ============================================================
# 7 — OVERSTOCK
# ============================================================
#========================================================
# elif page == "Overstock":
#     accent = PAGE_COLORS[page]
#     title_bar("OVERSTOCK", accent)

#     r = recs.copy()
#     excess_units = val(r, "Excess_Inventory_Units")
#     excess_value = val(r, "Excess_Inventory_Value")
#     if "Risk_Status" in r.columns:
#         overstock_skus = int((r["Risk_Status"].astype(str).str.lower() == "overstock").sum())
#         dead = int((r["Risk_Status"].astype(str).str.lower().str.contains("dead")).sum())
#     else:
#         overstock_skus = int((safe_col(r,["Excess_Inventory_Units"],0) > 0).sum())
#         dead = 0

#     kpi_row([
#         (fmt_num(overstock_skus), "Overstock SKUs"),
#         (fmt_money(excess_value), "Excess Inventory Value"),
#         (fmt_num(excess_units), "Excess Inventory Units"),
#         (fmt_num(dead), "Dead Stock SKUs"),
#     ], accent)

#     main = st.container()
#     with main:
#         c1, c2 = st.columns(2)
#         with c1:
#             x = r.copy()
#             x["Overstock"] = pd.to_numeric(safe_col(x,["Excess_Inventory_Units"],0), errors="coerce").fillna(0)
#             oc = x.groupby("Category", as_index=False)["Overstock"].sum().sort_values("Overstock", ascending=False)
#             fig = px.bar(oc, x="Category", y="Overstock", title="Overstock SKUs by category")
#             fig.update_traces(marker_color=accent)
#             chart(fig, 260)
#         with c2:
#             x = r.copy()
#             x["Excess Value"] = pd.to_numeric(safe_col(x,["Excess_Inventory_Value"],0), errors="coerce").fillna(0)
#             oc = x.groupby("Category", as_index=False)["Excess Value"].sum().sort_values("Excess Value", ascending=False)
#             fig = px.bar(oc, x="Category", y="Excess Value", title="Excess Inventory Value by category")
#             fig.update_traces(marker_color=accent)
#             chart(fig, 260)

#         cols = [c for c in [
#             "SKU","Category","Product_Name","Current_Stock","Average_Daily_Demand",
#             "Cost_Price","Excess_Inventory_Units","Excess_Inventory_Value"
#         ] if c in r.columns]
#         st.markdown("**Overstock SKU Details**")
#         st.dataframe(r[cols].sort_values("Excess_Inventory_Value", ascending=False),
#                      use_container_width=True, hide_index=True)

#         if "Current_Stock" in r.columns:
#             sc = r.copy()
#             sc["Demand"] = pd.to_numeric(safe_col(sc,["Average_Daily_Demand"],0), errors="coerce")
#             fig = px.scatter(sc, x="Demand", y="Current_Stock", color="Category",
#                              hover_data=[c for c in ["SKU","Product_Name"] if c in sc.columns],
#                              title="Inventory vs Demand by SKU")
#             chart(fig, 300)

#     st.markdown("#### Filters")
#     filter_row(show_date=True, show_category=True, show_product=True, show_sku=True)

#
# 7 — OVERSTOCK
# ============================================================

elif page == "Overstock":
    accent = PAGE_COLORS[page]
    title_bar("OVERSTOCK", accent)

    r = recs.copy()

    # ------------------------------------------------------------
    # Ensure Excess Inventory Units exists
    # ------------------------------------------------------------
    if "Excess_Inventory_Units" not in r.columns:
        current_stock = pd.to_numeric(
            safe_col(r, ["Current_Stock", "On_Hand_Units"], 0),
            errors="coerce"
        ).fillna(0)

        forecast_demand = pd.to_numeric(
            safe_col(r, ["Forecast_Demand"], 0),
            errors="coerce"
        ).fillna(0)

        r["Excess_Inventory_Units"] = (
            current_stock - forecast_demand
        ).clip(lower=0)

    # ------------------------------------------------------------
    # Ensure Excess Inventory Value exists
    # ------------------------------------------------------------
    if "Excess_Inventory_Value" not in r.columns:
        excess_units_calc = pd.to_numeric(
            r["Excess_Inventory_Units"],
            errors="coerce"
        ).fillna(0)

        cost_price_calc = pd.to_numeric(
            safe_col(r, ["Cost_Price"], 0),
            errors="coerce"
        ).fillna(0)

        r["Excess_Inventory_Value"] = (
            excess_units_calc * cost_price_calc
        )

    # ------------------------------------------------------------
    # Clean numeric columns
    # ------------------------------------------------------------
    r["Excess_Inventory_Units"] = pd.to_numeric(
        r["Excess_Inventory_Units"],
        errors="coerce"
    ).fillna(0)

    r["Excess_Inventory_Value"] = pd.to_numeric(
        r["Excess_Inventory_Value"],
        errors="coerce"
    ).fillna(0)

    # ------------------------------------------------------------
    # KPI calculations
    # ------------------------------------------------------------
    excess_units = r["Excess_Inventory_Units"].sum()
    excess_value = r["Excess_Inventory_Value"].sum()

    if "Risk_Status" in r.columns:
        risk_status = r["Risk_Status"].astype(str).str.lower()

        overstock_skus = int(
            (risk_status == "overstock").sum()
        )

        dead = int(
            risk_status.str.contains("dead").sum()
        )
    else:
        overstock_skus = int(
            (r["Excess_Inventory_Units"] > 0).sum()
        )
        dead = 0

    # ------------------------------------------------------------
    # KPI CARDS
    # ------------------------------------------------------------
    kpi_row([
        (fmt_num(overstock_skus), "Overstock SKUs"),
        (fmt_money(excess_value), "Excess Inventory Value"),
        (fmt_num(excess_units), "Excess Inventory Units"),
        (fmt_num(dead), "Dead Stock SKUs"),
    ], accent)

    # ------------------------------------------------------------
    # MAIN CONTENT
    # ------------------------------------------------------------
    main = st.container()

    with main:

        c1, c2 = st.columns(2)

        # --------------------------------------------------------
        # Overstock by Category
        # --------------------------------------------------------
        with c1:

            x = r.copy()

            x["Overstock"] = pd.to_numeric(
                x["Excess_Inventory_Units"],
                errors="coerce"
            ).fillna(0)

            if "Category" in x.columns:

                oc = (
                    x.groupby("Category", as_index=False)["Overstock"]
                    .sum()
                    .sort_values("Overstock", ascending=False)
                )

                fig = px.bar(
                    oc,
                    x="Category",
                    y="Overstock",
                    title="Overstock SKUs by Category"
                )

                fig.update_traces(marker_color=accent)

                chart(fig, 260)

        # --------------------------------------------------------
        # Excess Inventory Value by Category
        # --------------------------------------------------------
        with c2:

            x = r.copy()

            x["Excess Value"] = pd.to_numeric(
                x["Excess_Inventory_Value"],
                errors="coerce"
            ).fillna(0)

            if "Category" in x.columns:

                oc = (
                    x.groupby("Category", as_index=False)["Excess Value"]
                    .sum()
                    .sort_values(
                        "Excess Value",
                        ascending=False
                    )
                )

                fig = px.bar(
                    oc,
                    x="Category",
                    y="Excess Value",
                    title="Excess Inventory Value by Category"
                )

                fig.update_traces(marker_color=accent)

                chart(fig, 260)

        # --------------------------------------------------------
        # Overstock SKU Details
        # --------------------------------------------------------
        cols = [
            c for c in [
                "SKU",
                "Category",
                "Product_Name",
                "Current_Stock",
                "Average_Daily_Demand",
                "Cost_Price",
                "Excess_Inventory_Units",
                "Excess_Inventory_Value"
            ]
            if c in r.columns
        ]

        st.markdown("**Overstock SKU Details**")

        # IMPORTANT:
        # Sort the original dataframe BEFORE selecting columns.
        table = (
            r.sort_values(
                "Excess_Inventory_Value",
                ascending=False
            )[cols]
        )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------------
        # Inventory vs Demand
        # --------------------------------------------------------
        if "Current_Stock" in r.columns:

            sc = r.copy()

            sc["Demand"] = pd.to_numeric(
                safe_col(
                    sc,
                    ["Average_Daily_Demand"],
                    0
                ),
                errors="coerce"
            ).fillna(0)

            hover_cols = [
                c for c in [
                    "SKU",
                    "Product_Name"
                ]
                if c in sc.columns
            ]

            if "Category" in sc.columns:

                fig = px.scatter(
                    sc,
                    x="Demand",
                    y="Current_Stock",
                    color="Category",
                    hover_data=hover_cols,
                    title="Inventory vs Demand by SKU"
                )

            else:

                fig = px.scatter(
                    sc,
                    x="Demand",
                    y="Current_Stock",
                    hover_data=hover_cols,
                    title="Inventory vs Demand by SKU"
                )

            chart(fig, 300)

    # ------------------------------------------------------------
    # FILTERS
    # ------------------------------------------------------------
    st.markdown("#### Filters")

    filter_row(
        show_date=True,
        show_category=True,
        show_product=True,
        show_sku=True
    )
# ============================================================
# 8 — PROMOTION ANALYSIS
# ============================================================

elif page == "Promotion Analysis":
    accent = PAGE_COLORS[page]
    title_bar("PROMOTION ANALYSIS", accent)

    cal = calendar_df.copy()
    if cal.empty:
        st.warning("Promotion calendar data is not available in the processed CSV.")
    else:
        promo = cal[cal.get("Promotion", 0) == 1]
        non = cal[cal.get("Promotion", 0) == 0]
        promo_revenue = val(promo, "Revenue")
        promo_units = val(promo, "Units_Sold")
        uplift = ((promo_units / len(promo)) / (val(non,"Units_Sold") / len(non)) - 1) * 100 if len(promo) and len(non) else 0
        asp = promo_revenue / promo_units if promo_units else 0

        kpi_row([
            (fmt_money(promo_revenue), "Promo Revenue"),
            (fmt_num(promo_units), "Promo Units"),
            (f"{uplift:.2f}%", "Promo Uplift %"),
            (f"{len(promo):,}", "Promo Days"),
            (f"{asp:.2f}", "Promo ASP"),
        ], accent)

        main = st.container()
        with main:
            c1, c2 = st.columns([1.5, 1])
            with c1:
                pt = monthly_series(promo, "Revenue")
                fig = px.line(pt, x="Date", y="Revenue", markers=True, title="Promotion Trend")
                fig.update_traces(line_color=accent)
                chart(fig, 280)
            with c2:
                pu = promo.groupby("Category", as_index=False)["Units_Sold"].sum()
                nu = non.groupby("Category", as_index=False)["Units_Sold"].sum()
                q = pu.merge(nu, on="Category", how="outer", suffixes=("_Promo","_NonPromo")).fillna(0)
                q["Uplift %"] = np.where(q["Units_Sold_NonPromo"]>0,
                    (q["Units_Sold_Promo"]/q["Units_Sold_NonPromo"]-1)*100,0)
                fig = px.bar(q.sort_values("Uplift %"), x="Uplift %", y="Category",
                             orientation="h", title="Promo Uplift by Category")
                fig.update_traces(marker_color=accent)
                chart(fig, 280)

            c3, c4 = st.columns(2)
            with c3:
                # Promotion events if an event field exists; otherwise monthly promo revenue.
                event_col = next((c for c in ["Promotion_Event","Promotion_Name","Event","promotion_event"] if c in cal.columns), None)
                if event_col:
                    ev = promo.groupby(event_col, as_index=False)["Revenue"].sum().nlargest(8, "Revenue")
                    fig = px.bar(ev.sort_values("Revenue"), x="Revenue", y=event_col, orientation="h",
                                 title="Promotion Event Performance")
                else:
                    ev = monthly_series(promo, "Revenue").nlargest(8, "Revenue")
                    fig = px.bar(ev.sort_values("Revenue"), x="Revenue", y="Date", orientation="h",
                                 title="Promotion Event Performance")
                fig.update_traces(marker_color=accent)
                chart(fig, 280)
            with c4:
                p = promo.groupby(promo["Date"].dt.to_period("M"))["Units_Sold"].sum()
                n = non.groupby(non["Date"].dt.to_period("M"))["Units_Sold"].sum()
                z = pd.concat([p.rename("Promo Units"), n.rename("Non Promo Units")], axis=1).fillna(0).reset_index()
                z["Month"] = z["Date"].astype(str)
                fig = px.bar(z, x="Month", y=["Promo Units","Non Promo Units"],
                             title="Promo vs Non Promo Units Sold", barmode="group")
                chart(fig, 280)

        st.markdown("#### Filters")
        filter_row(show_date=True, show_category=True, show_product=True, show_sku=True) 

# ============================================================
# 9 — SEASONALITY
# ============================================================

elif page == "Seasonality":
    accent = PAGE_COLORS[page]
    title_bar("SEASONALITY", accent)

    cal = calendar_df.copy()
    if cal.empty or "season" not in cal.columns:
        st.warning("Seasonality fields are not available.")
    else:
        demand = val(cal, "Units_Sold")
        daily = demand / cal["Date"].nunique() if "Date" in cal and cal["Date"].nunique() else 0
        peak = cal.groupby("Date")["Units_Sold"].sum().max() if len(cal) else 0
        yoy = 0
        if "Date" in cal:
            y = cal.groupby(cal["Date"].dt.year)["Units_Sold"].sum()
            if len(y)>=2 and y.iloc[0]:
                yoy = (y.iloc[-1]/y.iloc[0]-1)*100

        kpi_row([
            (fmt_num(demand), "Total Demand"),
            (f"{daily:.2f}", "Average Daily Demand"),
            (fmt_num(peak), "Peak Demand"),
            (f"{yoy:.2f}%", "Demand YoY %"),
            (fmt_money(val(cal,"Revenue")), "Seasonal Revenue"),
        ], accent)

        main = st.container()
        with main:
            m = monthly_series(cal, "Units_Sold")
            fig = px.area(m, x="Date", y="Units_Sold", title="Monthly Demand Trend")
            fig.update_traces(line_color=accent, fillcolor="#F0E4A0")
            chart(fig, 280)

            c1, c2 = st.columns(2)
            with c1:
                season = cal.groupby("season", as_index=False)["Units_Sold"].sum().sort_values("Units_Sold", ascending=False)
                fig = px.bar(season, x="Units_Sold", y="season", orientation="h",
                             title="Demand by season")
                fig.update_traces(marker_color=accent)
                chart(fig, 260)
            with c2:
                holiday = cal.groupby("is_holiday", as_index=False)["Units_Sold"].sum()
                holiday["Type"] = holiday["is_holiday"].map({0:"Non-Holiday",1:"Holiday"}).fillna("Unknown")
                fig = px.bar(holiday, x="Type", y="Units_Sold", title="Holiday vs Non-Holiday Demand")
                fig.update_traces(marker_color=accent)
                chart(fig, 260)

            sc = cal.groupby(["season","Category"], as_index=False)["Units_Sold"].sum()
            piv = sc.pivot(index="season", columns="Category", values="Units_Sold").fillna(0)
            st.markdown("**Seasonal Demand by Category**")
            st.dataframe(piv.reset_index(), use_container_width=True, hide_index=True)

        st.markdown("#### Filters")
        filter_row(show_date=True, show_category=True, show_product=True)
        st.markdown("Select seasons in the sidebar-style controls above if you extend this page with season filters.")

# ============================================================
# 10 — FORECAST
# ============================================================

elif page == "Forecast":
    accent = PAGE_COLORS[page]
    title_bar("FORECAST", accent)

    fc = forecasts.copy()
    if fc.empty:
        st.warning("Forecast data is not available.")
    else:
        forecast_total = val(fc, "Forecast_Demand")
        accuracy = 0
        error_pct = 0
        if "Actual_Demand" in fc.columns:
            actual = pd.to_numeric(fc["Actual_Demand"], errors="coerce")
            pred = pd.to_numeric(fc["Forecast_Demand"], errors="coerce")
            denom = actual.abs().sum()
            error_pct = ((actual-pred).abs().sum()/denom*100) if denom else 0
            accuracy = max(0, 100-error_pct)

        growth = 0
        if "Date" in fc.columns:
            ys = fc.groupby(fc["Date"].dt.year)["Forecast_Demand"].sum()
            if len(ys)>=2 and ys.iloc[0]:
                growth = (ys.iloc[-1]/ys.iloc[0]-1)*100

        excess_skus = int((pd.to_numeric(safe_col(recs,["Excess_Inventory_Units"],0), errors="coerce") > 0).sum())

        kpi_row([
            (fmt_num(forecast_total), "Forecast Demand"),
            (f"{accuracy:.2f}%", "Forecast Accuracy %"),
            (f"{error_pct:.2f}%", "Forecast Error %"),
            (f"{growth:.2f}%", "Forecast Demand Growth %"),
            (fmt_num(excess_skus), "Forecasted Excess SKUs"),
        ], accent)

        main, right = st.columns([2.8, 1.2])
        with main:
            trend = fc.groupby("Date", as_index=False)["Forecast_Demand"].sum()
            fig = px.line(trend, x="Date", y="Forecast_Demand", title="Forecast Demand")
            fig.update_traces(line_color=accent)
            chart(fig, 290)

            inv = latest_inventory(inventory)
            fd = fc.groupby("SKU", as_index=False)["Forecast_Demand"].sum()
            inv2 = inv.groupby("SKU", as_index=False)["Current_Stock"].sum()
            q = fd.merge(inv2, on="SKU", how="left").fillna(0)
            q = q.merge(products[["SKU","Category"]], on="SKU", how="left")
            fig = px.scatter(q, x="Forecast_Demand", y="Current_Stock", color="Category",
                             title="Forecast Demand vs Current Inventory")
            chart(fig, 300)
        with right:
            cat = fc.merge(products[["SKU","Category"]], on="SKU", how="left")
            cat = cat.groupby("Category", as_index=False)["Forecast_Demand"].sum().nlargest(6, "Forecast_Demand")
            fig = px.bar(cat.sort_values("Forecast_Demand"), x="Forecast_Demand", y="Category",
                         orientation="h", title="Forecast Demand by Category")
            fig.update_traces(marker_color=accent)
            chart(fig, 500)

        st.markdown("#### Filters")
        filter_row(show_date=True, show_category=True, show_subcategory=True)

# ============================================================
# 11 — CUSTOMER & BUSINESS INSIGHTS
# ============================================================

elif page == "Customer & Business Insights":
    accent = PAGE_COLORS[page]
    title_bar("CUSTOMER & BUSINESS INSIGHTS", accent)

    cal = calendar_df.copy()
    demand = val(cal, "Units_Sold")
    days = cal["Date"].nunique() if "Date" in cal else 1
    avg_daily = demand/days if days else 0

    ma7 = 0
    ma30 = 0
    if "Date" in cal:
        daily = cal.groupby("Date", as_index=False)["Units_Sold"].sum().sort_values("Date")
        ma7 = daily["Units_Sold"].rolling(7).mean().iloc[-1] if len(daily)>=7 else daily["Units_Sold"].mean()
        ma30 = daily["Units_Sold"].rolling(30).mean().iloc[-1] if len(daily)>=30 else daily["Units_Sold"].mean()

    promo_uplift = 0
    if not cal.empty and "Promotion" in cal.columns:
        p = cal[cal["Promotion"]==1]["Units_Sold"].mean()
        n = cal[cal["Promotion"]==0]["Units_Sold"].mean()
        promo_uplift = (p/n-1)*100 if n else 0

    yoy = 0
    if "Date" in cal:
        y = cal.groupby(cal["Date"].dt.year)["Units_Sold"].sum()
        if len(y)>=2 and y.iloc[0]:
            yoy=(y.iloc[-1]/y.iloc[0]-1)*100

    kpi_row([
        (fmt_num(avg_daily), "Average Daily Demand"),
        (fmt_num(ma7), "7 Day Moving Average"),
        (fmt_num(ma30), "30 Day Moving Average"),
        (f"{promo_uplift:.2f}%", "Promo Uplift %"),
        (fmt_num(val(cal,"Units_Sold")), "Seasonal Demand"),
        (f"{yoy:.2f}%", "Demand Growth % (YOY)"),
    ], accent)

    main = st.container()
    with main:
        c1, c2 = st.columns(2)
        with c1:
            dc = cal.groupby("Category", as_index=False)["Units_Sold"].sum().sort_values("Units_Sold", ascending=False)
            fig = px.bar(dc, x="Units_Sold", y="Category", orientation="h",
                         title="Demand by Category")
            fig.update_traces(marker_color=accent)
            chart(fig, 280)
        with c2:
            inv = latest_inventory(inventory)
            ic = inv.groupby("Category", as_index=False)["Current_Stock"].mean().rename(columns={"Current_Stock":"Average On Hand Units"})
            d = cal.groupby("Category", as_index=False)["Units_Sold"].sum().rename(columns={"Units_Sold":"Total Demand"})
            q = d.merge(ic, on="Category", how="left").fillna(0)
            fig = px.bar(q, x="Category", y=["Total Demand","Average On Hand Units"],
                         barmode="group", title="Demand vs Inventory by Category")
            chart(fig, 280)

        m = monthly_series(cal, "Units_Sold")
        fig = px.area(m, x="Date", y="Units_Sold", title="Demand Trend")
        fig.update_traces(line_color=accent, fillcolor="#EEC9B9")
        chart(fig, 290)

        if not cal.empty:
            high_threshold = cal.groupby("Category")["Units_Sold"].sum().median()
            dist = pd.DataFrame({
                "Segment":["High Demand","Low Demand"],
                "Share":[
                    (cal.groupby("Category")["Units_Sold"].sum() >= high_threshold).sum(),
                    (cal.groupby("Category")["Units_Sold"].sum() < high_threshold).sum()
                ]
            })
            fig = px.pie(dist, names="Segment", values="Share", hole=.55,
                         title="Demand Segment Distribution")
            chart(fig, 260)

    st.markdown("#### Filters")
    filter_row(show_date=True, show_category=True, show_product=True)

# ============================================================
# 12 — RECOMMENDATION
# ============================================================

elif page == "Recommendation":
    accent = PAGE_COLORS[page]
    title_bar("RECOMMENDATION", accent)

    r = recs.copy()
    if "Recommendation" not in r.columns:
        r["Recommendation"] = np.where(
            pd.to_numeric(safe_col(r,["Excess_Inventory_Units"],0), errors="coerce") > 0,
            "OVERSTOCK", "REORDER"
        )

    reorder = int(r["Recommendation"].astype(str).str.upper().str.contains("REORDER").sum())
    overstock = int(r["Recommendation"].astype(str).str.upper().str.contains("OVERSTOCK").sum())
    healthy = int(r["Recommendation"].astype(str).str.upper().str.contains("HEALTHY").sum())
    risk_value = val(r, "Excess_Inventory_Value")

    kpi_row([
        (fmt_num(reorder), "Reorder SKUs"),
        (fmt_num(overstock), "Overstock SKUs"),
        (fmt_num(healthy), "Healthy SKUs"),
        (fmt_money(risk_value), "Inventory Value at Risk"),
    ], accent)

    main = st.container()
    with main:
        cols = [c for c in [
            "SKU","Current_Stock","Forecast_Demand",
            "Excess_Inventory_Units","Excess_Inventory_Value","Recommendation"
        ] if c in r.columns]
        table = r[cols].copy()
        st.markdown("**Executive Action Matrix**")
        st.dataframe(table, use_container_width=True, hide_index=True, height=300)

        q = r.copy()
        q["Daily Demand"] = pd.to_numeric(safe_col(q,["Average_Daily_Demand","Daily_Demand"],0), errors="coerce")
        q["On Hand Units"] = pd.to_numeric(safe_col(q,["Current_Stock","On_Hand_Units"],0), errors="coerce")
        q["Recommendation Category"] = q["Recommendation"].astype(str)
        fig = px.scatter(q, x="Daily Demand", y="On Hand Units",
                         color="Recommendation Category", title="Inventory Risk vs Demand")
        chart(fig, 300)
    c1, c2 = st.columns([1.2, 1])
    with c1:
        q = r.copy()
        q["Count"] = 1
        q["Recommendation Category"] = q["Recommendation"].astype(str)
        cat = q.groupby(["Category","Recommendation Category"], as_index=False)["Count"].sum()
        fig = px.bar(cat, x="Count", y="Category", color="Recommendation Category",
                     orientation="h", barmode="stack",
                     title="Category-Level Recommendation")
        chart(fig, 330)
    with c2:
        mix = r["Recommendation"].astype(str).str.upper().map(
            lambda x: "REORDER" if "REORDER" in x else ("OVERSTOCK" if "OVERSTOCK" in x else "HEALTHY")
        ).value_counts().reset_index()
        mix.columns = ["Recommendation", "Count"]
        fig = px.pie(mix, names="Recommendation", values="Count", hole=.55,
                     title="Recommendation Action")
        chart(fig, 330)

    st.markdown("#### Filters")
    filter_row(show_date=True, show_category=True, show_product=True, show_sku=True)

st.sidebar.markdown("---")
# st.sidebar.caption("FORESIGHT · Power BI reference-matched dashboard")
