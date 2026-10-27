
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="RETAILIQ | Retail Intelligence",
    page_icon="📊",
    layout="wide"
)

# ---------------- PAGE DESIGN ----------------


st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8F7F2;
    }

    h1, h2, h3 {
        color: #334E68;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E1E7E5;
    }

    .stButton > button {
        background-color: #52796F;
        color: white;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("RETAILIQ")
st.subheader("Retail Sales & Profitability Intelligence")
st.write(
    "Transform retail transaction data into meaningful business insights."
)

st.divider()

# ---------------- DATA UPLOAD ----------------

st.header("1. Upload your dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.info(
        "Upload a dataset to begin. "
        "For this prototype, use the provided retail dataset."
    )
    st.stop()

try:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

except Exception as error:
    st.error(f"Unable to read this file: {error}")
    st.stop()

# Standardise column names
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

st.success("Dataset uploaded successfully!")
st.caption(f"{len(df):,} rows | {len(df.columns)} columns")

with st.expander("Preview uploaded data"):
    st.dataframe(df.head(10), use_container_width=True)

# ---------------- VALIDATION ----------------

required_columns = ["sales", "profit"]
missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )
    st.write("Available columns:", df.columns.tolist())
    st.info(
        "Please ensure your file contains Sales and Profit columns, "
        "or map your column names to these required fields."
    )
    st.stop()

# Convert numeric fields safely
for column in ["sales", "profit"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=["sales", "profit"]).copy()

if df.empty:
    st.error("No valid sales and profit records were found.")
    st.stop()

# ---------------- FILTERS ----------------

st.header("2. Explore your business")

filtered_df = df.copy()

filter_columns = [
    col for col in ["category", "region"]
    if col in filtered_df.columns
]

filter_cols = st.columns(len(filter_columns)) if filter_columns else []

for index, column in enumerate(filter_columns):
    with filter_cols[index]:
        options = sorted(
            filtered_df[column].dropna().astype(str).unique().tolist()
        )
        selected = st.multiselect(
            f"Filter by {column.replace('_', ' ').title()}",
            options,
            default=options,
            key=f"filter_{column}"
        )
        filtered_df = filtered_df[
            filtered_df[column].astype(str).isin(selected)
        ]

if filtered_df.empty:
    st.warning("No records match your selected filters.")
    st.stop()

# ---------------- KPI CARDS ----------------

total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Sales", f"{total_sales:,.2f}")
kpi2.metric("Total Profit", f"{total_profit:,.2f}")
kpi3.metric("Profit Margin", f"{profit_margin:.2f}%")
kpi4.metric("Records Analysed", f"{len(filtered_df):,}")

st.divider()

# ---------------- VISUAL ANALYTICS ----------------

st.header("3. Performance dashboard")

if "category" in filtered_df.columns:
    category_sales = (
        filtered_df.groupby("category")["sales"]
        .sum().sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 4))
    category_sales.plot(kind="bar", ax=ax)
    ax.set_title("Sales by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Sales")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

if "region" in filtered_df.columns:
    region_profit = (
        filtered_df.groupby("region")["profit"]
        .sum().sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 4))
    region_profit.plot(kind="bar", ax=ax)
    ax.set_title("Profit by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Profit")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

if "order_date" in filtered_df.columns:
    filtered_df["order_date"] = pd.to_datetime(
        filtered_df["order_date"], errors="coerce"
    )

    monthly = (
        filtered_df.dropna(subset=["order_date"])
        .set_index("order_date")
        .resample("MS")["sales"]
        .sum()
    )

    if not monthly.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        monthly.plot(marker="o", ax=ax)
        ax.set_title("Monthly Sales Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ---------------- RECOMMENDATIONS ----------------

st.divider()
st.header("4. Business recommendations")

recommendations = []

if "category" in filtered_df.columns:
    category_profit = filtered_df.groupby("category")["profit"].sum()

    if not category_profit.empty:
        best_category = category_profit.idxmax()
        recommendations.append(
            f"Review the practices of {best_category}, "
            "the category with the highest total profit."
        )

        loss_categories = category_profit[category_profit < 0]

        for category in loss_categories.index:
            recommendations.append(
                f"Investigate {category}: its total profit is negative."
            )

if "region" in filtered_df.columns:
    region_profit = filtered_df.groupby("region")["profit"].sum()

    if not region_profit.empty:
        weakest_region = region_profit.idxmin()
        recommendations.append(
            f"Review costs, product mix and pricing in {weakest_region}, "
            "the region with the lowest total profit."
        )

if not recommendations:
    recommendations.append(
        "Add category and region columns to unlock more detailed insights."
    )

for number, recommendation in enumerate(recommendations, start=1):
    st.write(f"**{number}.** {recommendation}")

st.caption(
    "Recommendations are rule-based and should be reviewed "
    "before making business decisions."
)

# ---------------- DOWNLOADS ----------------

st.divider()
st.header("5. Download your results")

download1, download2 = st.columns(2)

with download1:
    st.download_button(
        "Download analysed data",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="retailiq_analysed_data.csv",
        mime="text/csv"
    )

with download2:
    summary = pd.DataFrame({
        "Metric": ["Total Sales", "Total Profit", "Profit Margin (%)"],
        "Value": [total_sales, total_profit, profit_margin]
    })

    st.download_button(
        "Download KPI summary",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="retailiq_summary.csv",
        mime="text/csv"
    )

st.divider()
st.caption("RETAILIQ | Retail intelligence for better decisions")
