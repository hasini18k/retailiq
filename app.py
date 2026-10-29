import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="RETAILIQ | Retail Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- RETAILIQ DESIGN SYSTEM ----------
BG = "#FAF7F5"
INK = "#202638"
MUTED = "#6E7482"
RED = "#A7193F"
RED_DARK = "#7D1230"
ROSE = "#FBE8ED"
BORDER = "#E9E2E4"
WHITE = "#FFFFFF"
GREEN = "#2E7D55"
GOLD = "#C98B24"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {{
        --retailiq-bg: {BG};
        --retailiq-ink: {INK};
        --retailiq-red: {RED};
    }}
    .stApp {{
        background: var(--retailiq-bg);
        color: var(--retailiq-ink);
        font-family: 'DM Sans', sans-serif;
    }}
    [data-testid="stHeader"] {{ background: rgba(250,247,245,.92); }}
    .block-container {{
        max-width: 1440px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }}
    h1, h2, h3, h4 {{
        font-family: 'Manrope', sans-serif !important;
        color: {INK} !important;
        letter-spacing: -0.035em;
    }}
    h1 {{ font-size: 2.6rem !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.65rem !important; font-weight: 800 !important; }}
    h3 {{ font-size: 1.1rem !important; font-weight: 700 !important; }}
    p, label, .stMarkdown {{ color: {INK}; }}
    .retailiq-topbar {{
        display:flex; justify-content:space-between; align-items:center;
        padding: 0.25rem 0 1.15rem 0; border-bottom: 1px solid {BORDER};
        margin-bottom: 1.2rem;
    }}
    .brand-lockup {{ display:flex; gap:.7rem; align-items:center; }}
    .brand-icon {{
        width:44px; height:44px; display:flex; align-items:center; justify-content:center;
        background:{RED}; color:white; border-radius:14px; font-size:1.4rem;
        box-shadow: 0 8px 18px rgba(167,25,63,.18);
    }}
    .brand-name {{ font-family:'Manrope',sans-serif; font-size:1.15rem; font-weight:800; color:{INK}; }}
    .brand-tagline {{ font-size:.75rem; color:{MUTED}; margin-top:-2px; }}
    .top-pill {{
        display:inline-block; background:#F4E4E8; color:{RED_DARK}; padding:.45rem .8rem;
        border-radius:999px; font-size:.78rem; font-weight:700; letter-spacing:.02em;
    }}
    .hero {{
        position:relative; overflow:hidden; border-radius:24px; padding:2rem 2.1rem;
        background:linear-gradient(115deg, #FFF 0%, #FFF8F7 55%, #F8E5E9 100%);
        border:1px solid {BORDER}; margin-bottom:1.6rem;
    }}
    .hero-kicker {{ color:{RED}; font-size:.75rem; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }}
    .hero-title {{ font-family:'Manrope',sans-serif; font-weight:800; font-size:2.7rem; line-height:1.08; color:{INK}; margin:.45rem 0 .65rem; }}
    .hero-title span {{ color:{RED}; }}
    .hero-copy {{ color:{MUTED}; max-width:650px; font-size:1rem; line-height:1.65; }}
    .hero-chips {{ display:flex; gap:.55rem; flex-wrap:wrap; margin-top:1.15rem; }}
    .hero-chip {{ background:white; border:1px solid {BORDER}; padding:.48rem .7rem; border-radius:10px; font-size:.78rem; color:{INK}; font-weight:600; }}
    .section-head {{ display:flex; align-items:center; gap:.7rem; margin:1.6rem 0 .8rem; }}
    .section-number {{
        display:inline-flex; align-items:center; justify-content:center; min-width:32px; height:32px;
        border-radius:11px; color:white; background:{RED}; font-weight:800; font-size:.85rem;
    }}
    .section-title {{ font-family:'Manrope',sans-serif; font-size:1.35rem; font-weight:800; color:{INK}; }}
    .section-subtitle {{ color:{MUTED}; font-size:.86rem; margin:.15rem 0 .8rem 2.7rem; }}
    [data-testid="stMetric"] {{
        background:{WHITE}; border:1px solid {BORDER}; padding:1.1rem 1.15rem;
        border-radius:18px; box-shadow:0 4px 15px rgba(32,38,56,.035);
    }}
    [data-testid="stMetricLabel"] p {{ color:{MUTED} !important; font-weight:600; font-size:.84rem; }}
    [data-testid="stMetricValue"] {{ color:{INK} !important; font-family:'Manrope',sans-serif; font-weight:800; }}
    [data-testid="stMetricDelta"] {{ font-size:.78rem; }}
    div[data-testid="stFileUploader"] {{
        background:{WHITE}; border:1px dashed #D6B5BE; border-radius:16px; padding:.8rem;
    }}
    div[data-testid="stFileUploader"] section {{ background:#FFF9FA; border-radius:12px; }}
    .stButton > button, .stDownloadButton > button {{
        background:{RED}; color:white; border:1px solid {RED}; border-radius:11px;
        font-weight:700; padding:.55rem 1rem; transition:all .15s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background:{RED_DARK}; color:white; border-color:{RED_DARK};
    }}
    div[data-baseweb="select"] > div {{
        border-radius:11px !important; border-color:{BORDER} !important; background:white;
    }}
    .insight-card {{
        background:white; border:1px solid {BORDER}; border-radius:16px; padding:1rem 1.1rem;
        height:100%; box-shadow:0 4px 15px rgba(32,38,56,.035);
    }}
    .insight-label {{ color:{RED}; text-transform:uppercase; font-size:.7rem; font-weight:800; letter-spacing:.1em; }}
    .insight-title {{ color:{INK}; font-family:'Manrope',sans-serif; font-size:1rem; font-weight:800; margin:.35rem 0; }}
    .insight-copy {{ color:{MUTED}; font-size:.85rem; line-height:1.55; }}
    .footer {{
        margin-top:2.5rem; padding-top:1.1rem; border-top:1px solid {BORDER};
        display:flex; justify-content:space-between; color:{MUTED}; font-size:.78rem;
    }}
    .stAlert {{ border-radius:12px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="retailiq-topbar">
      <div class="brand-lockup">
        <div class="brand-icon">🛒</div>
        <div>
          <div class="brand-name">RETAILIQ</div>
          <div class="brand-tagline">Retail intelligence for better decisions</div>
        </div>
      </div>
      <div class="top-pill">DATA&nbsp; · &nbsp;INSIGHTS&nbsp; · &nbsp;GROWTH</div>
    </div>
    <div class="hero">
      <div class="hero-kicker">Retail performance workspace</div>
      <div class="hero-title">Turn retail data into<br><span>smarter decisions.</span></div>
      <div class="hero-copy">
        Explore sales, profitability and regional performance in one clear workspace.
        Upload your dataset to uncover trends and practical opportunities for growth.
      </div>
      <div class="hero-chips">
        <div class="hero-chip">↗ Performance analytics</div>
        <div class="hero-chip">◎ Category & region insights</div>
        <div class="hero-chip">✦ Actionable recommendations</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

def section_heading(number, title, subtitle=None):
    st.markdown(
        f'<div class="section-head"><span class="section-number">{number}</span>'
        f'<span class="section-title">{title}</span></div>',
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)

section_heading("1", "Upload your dataset", "Start with a CSV or Excel file. RETAILIQ will validate the key fields before analysing.")
uploaded_file = st.file_uploader(
    "Choose a retail dataset",
    type=["csv", "xlsx"],
    help="Required columns: Sales and Profit. Category, Region and Order Date enable extra insights.",
)

if uploaded_file is None:
    st.markdown(
        """
        <div class="insight-card">
          <div class="insight-label">Getting started</div>
          <div class="insight-title">Your next business insight starts here.</div>
          <div class="insight-copy">Upload a dataset to see performance indicators, category comparisons,
          regional profitability, monthly trends and recommendations.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="footer"><span>RETAILIQ · Retail intelligence for better decisions</span><span>Built with Python & Streamlit</span></div>', unsafe_allow_html=True)
    st.stop()

try:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
except Exception as error:
    st.error(f"Unable to read this file: {error}")
    st.stop()

# Normalize column names consistently, including punctuation and spaces.
df.columns = (
    df.columns.astype(str).str.strip().str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

required_columns = ["sales", "profit"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error("This dataset is missing required columns: " + ", ".join(missing_columns))
    st.info("Please include Sales and Profit columns. Optional columns: Category, Region and Order Date.")
    st.write("Columns detected:", df.columns.tolist())
    st.stop()

for column in ["sales", "profit"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")
df = df.dropna(subset=["sales", "profit"]).copy()

if df.empty:
    st.error("No valid sales and profit records were found in this file.")
    st.stop()

st.success(f"Dataset ready · {len(df):,} valid records · {len(df.columns)} columns detected")
with st.expander("Preview uploaded data", expanded=False):
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)

section_heading("2", "Explore your business", "Use the filters to focus on the segments you want to understand.")
filtered_df = df.copy()
filter_columns = [col for col in ["category", "region"] if col in filtered_df.columns]
if filter_columns:
    filter_cols = st.columns(len(filter_columns))
    for index, column in enumerate(filter_columns):
        with filter_cols[index]:
            options = sorted(filtered_df[column].dropna().astype(str).unique().tolist())
            selected = st.multiselect(
                f"{column.replace('_', ' ').title()}",
                options=options,
                default=options,
                key=f"filter_{column}",
                placeholder=f"Select {column}",
            )
            filtered_df = filtered_df[filtered_df[column].astype(str).isin(selected)]

if filtered_df.empty:
    st.warning("No records match your current filters. Select at least one category or region.")
    st.stop()

total_sales = float(filtered_df["sales"].sum())
total_profit = float(filtered_df["profit"].sum())
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
previous_sales = float(df["sales"].sum())
sales_delta = ((total_sales - previous_sales) / abs(previous_sales) * 100) if previous_sales else 0
previous_profit = float(df["profit"].sum())
profit_delta = ((total_profit - previous_profit) / abs(previous_profit) * 100) if previous_profit else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total sales", f"{total_sales:,.0f}", help="Sum of sales for the selected records.")
k2.metric("Total profit", f"{total_profit:,.0f}", help="Sum of profit for the selected records.")
k3.metric("Profit margin", f"{profit_margin:.2f}%", help="Total profit divided by total sales.")
k4.metric("Records analysed", f"{len(filtered_df):,}", help="Number of valid records after filtering.")

section_heading("3", "Performance dashboard", "Compare categories, regions and monthly movement at a glance.")
chart_cols = st.columns(2)

def style_axis(ax):
    ax.set_facecolor(WHITE)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BORDER)
    ax.spines["bottom"].set_color(BORDER)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", linestyle="--", linewidth=.7, alpha=.55, color=BORDER)
    ax.set_axisbelow(True)
    ax.title.set_color(INK)
    ax.title.set_fontweight("bold")
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)

if "category" in filtered_df.columns:
    with chart_cols[0]:
        category_sales = filtered_df.groupby("category")["sales"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor(WHITE)
        category_sales.plot(kind="bar", ax=ax, color=[RED if i == 0 else "#D86B83" for i in range(len(category_sales))], width=.68)
        ax.set_title("Sales by category", loc="left", pad=15, fontsize=13)
        ax.set_xlabel("")
        ax.set_ylabel("Sales")
        ax.tick_params(axis="x", labelrotation=28)
        for label in ax.get_xticklabels():
            label.set_ha("right")
        style_axis(ax)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
else:
    with chart_cols[0]:
        st.info("Add a Category column to view sales by category.")

if "region" in filtered_df.columns:
    with chart_cols[1]:
        region_profit = filtered_df.groupby("region")["profit"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor(WHITE)
        colors = [GREEN if value >= 0 else RED for value in region_profit.values]
        region_profit.plot(kind="bar", ax=ax, color=colors, width=.68)
        ax.set_title("Profit by region", loc="left", pad=15, fontsize=13)
        ax.set_xlabel("")
        ax.set_ylabel("Profit")
        ax.tick_params(axis="x", labelrotation=0)
        style_axis(ax)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
else:
    with chart_cols[1]:
        st.info("Add a Region column to view profit by region.")

if "order_date" in filtered_df.columns:
    filtered_df["order_date"] = pd.to_datetime(filtered_df["order_date"], errors="coerce")
    monthly = (
        filtered_df.dropna(subset=["order_date"])
        .set_index("order_date").resample("MS")["sales"].sum()
    )
    if not monthly.empty:
        fig, ax = plt.subplots(figsize=(12, 3.8))
        fig.patch.set_facecolor(WHITE)
        ax.fill_between(monthly.index, monthly.values, color="#F5CAD4", alpha=.45)
        ax.plot(monthly.index, monthly.values, color=RED, marker="o", markersize=4, linewidth=2.4)
        ax.set_title("Monthly sales trend", loc="left", pad=15, fontsize=13)
        ax.set_xlabel("")
        ax.set_ylabel("Sales")
        style_axis(ax)
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


# Discount Level vs Profit scatter plot
if "discount" in filtered_df.columns:
    with st.container():
        st.markdown("### Discount Level vs Profit")
        st.caption("Explore the relationship between discount percentages and profit.")

        discount_data = filtered_df.copy()
        discount_data["discount"] = pd.to_numeric(
            discount_data["discount"], errors="coerce"
        )
        discount_data = discount_data.dropna(
            subset=["discount", "profit"]
        )

        if not discount_data.empty:
            fig, ax = plt.subplots(figsize=(12, 4.5))
            fig.patch.set_facecolor(WHITE)
            ax.set_facecolor(WHITE)

            ax.scatter(
                discount_data["discount"] * 100,
                discount_data["profit"],
                color=RED,
                alpha=0.45,
                s=24,
                edgecolors="none"
            )

            ax.set_title(
                "Discount Level vs Profit",
                loc="left",
                pad=15,
                fontsize=13,
                color=INK,
                fontweight="bold"
            )
            ax.set_xlabel("Discount (%)")
            ax.set_ylabel("Profit")

            style_axis(ax)
            ax.grid(True, linestyle="--", linewidth=0.7,
                    alpha=0.45, color=BORDER)

            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("No valid discount and profit values are available.")
else:
    st.info("Add a Discount column to view Discount Level vs Profit.")


section_heading("4", "Business recommendations", "Rule-based prompts to help prioritise the next question to investigate.")
recommendations = []
if "category" in filtered_df.columns:
    cat_profit = filtered_df.groupby("category")["profit"].sum().sort_values(ascending=False)
    if not cat_profit.empty:
        best_category = cat_profit.index[0]
        recommendations.append((
            "Top-performing category",
            f"Review what is working in {best_category}. Consider validating its pricing, product mix and stock availability before scaling similar practices."
        ))
        loss_categories = cat_profit[cat_profit < 0]
        if not loss_categories.empty:
            loss_names = ", ".join(map(str, loss_categories.index[:4]))
            recommendations.append((
                "Investigate loss-making categories",
                f"Check discounts, supplier costs and product-level margins in: {loss_names}."
            ))
if "region" in filtered_df.columns:
    reg_profit = filtered_df.groupby("region")["profit"].sum().sort_values()
    if not reg_profit.empty:
        weakest_region = reg_profit.index[0]
        weakest_value = reg_profit.iloc[0]
        recommendations.append((
            "Regional performance review",
            f"Review costs, product mix and pricing in {weakest_region}. Its total profit is {weakest_value:,.0f} for the selected records."
        ))
if profit_margin < 10:
    recommendations.append((
        "Protect profitability",
        f"The current profit margin is {profit_margin:.2f}%. Review discounting and high-cost items to understand the pressure on margin."
    ))
if not recommendations:
    recommendations.append((
        "Unlock deeper insights",
        "Add Category, Region and Order Date fields to your dataset for more detailed comparisons."
    ))

rec_cols = st.columns(min(3, len(recommendations)))
for i, (title, copy) in enumerate(recommendations):
    with rec_cols[i % len(rec_cols)]:
        st.markdown(
            f'<div class="insight-card"><div class="insight-label">Insight {i+1:02d}</div>'
            f'<div class="insight-title">{title}</div><div class="insight-copy">{copy}</div></div>',
            unsafe_allow_html=True,
        )
st.caption("Recommendations are generated from simple rules and should be validated before making business decisions.")

section_heading("5", "Download your results", "Export the filtered dataset and a compact KPI summary for your report.")
d1, d2 = st.columns(2)
with d1:
    st.download_button(
        "↓  Download analysed data",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="retailiq_analysed_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
with d2:
    summary = pd.DataFrame({
        "Metric": ["Total Sales", "Total Profit", "Profit Margin (%)", "Records Analysed"],
        "Value": [total_sales, total_profit, round(profit_margin, 2), len(filtered_df)],
    })
    st.download_button(
        "↓  Download KPI summary",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="retailiq_kpi_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown(
    '<div class="footer"><span><b>RETAILIQ</b> · Retail intelligence for better decisions</span>'
    '<span>Built with Python · Pandas · NumPy · Matplotlib · Streamlit</span></div>',
    unsafe_allow_html=True,
)
