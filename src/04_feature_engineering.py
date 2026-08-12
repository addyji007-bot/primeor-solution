"""
Day 4 — Feature Engineering & Deeper EDA

This script:
1. Loads the cleaned Superstore dataset.
2. Creates analytical features:
   - shipping_days
   - profit_margin
   - year_month
   - quarter
   - year
   - month
   - month_name
   - shipping_outlier
3. Performs shipping analysis.
4. Performs profitability analysis.
5. Performs time-based analysis.
6. Performs discount vs profit analysis.
7. Performs sub-category analysis.
8. Performs outlier analysis.
9. Saves the engineered dataset and figures.

Input:
    data/Cleaned_data.csv

Outputs:
    data/engineered_data.csv
    reports/figures/04_*.png
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

INPUT_FILE = DATA_DIR / "Cleaned_data.csv"
OUTPUT_FILE = DATA_DIR / "engineered_data.csv"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. PLOT CONFIGURATION
# ============================================================

sns.set_theme(style="whitegrid")


# ============================================================
# 3. LOAD DATA
# ============================================================

print("=" * 60)
print("DAY 4 — FEATURE ENGINEERING & DEEPER EDA")
print("=" * 60)

print("\nLoading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Dataset loaded successfully.")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")


# ============================================================
# 4. DATE CONVERSION
# ============================================================

df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])


# ============================================================
# 5. FEATURE ENGINEERING
# ============================================================

print("\nCreating analytical features...")


# Shipping days
df["shipping_days"] = (
    df["ship_date"] - df["order_date"]
).dt.days


# Profit margin
df["profit_margin"] = np.where(
    df["sales"] != 0,
    (df["profit"] / df["sales"]) * 100,
    np.nan
)


# Time features
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.month_name()
df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
df["quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)


print("Features created:")
print(" - shipping_days")
print(" - profit_margin")
print(" - year")
print(" - month")
print(" - month_name")
print(" - year_month")
print(" - quarter")


# ============================================================
# 6. SHIPPING ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("SHIPPING ANALYSIS")
print("=" * 60)


# Overall shipping statistics
shipping_summary = pd.DataFrame({
    "Metric": [
        "Average Shipping Days",
        "Median Shipping Days",
        "Minimum Shipping Days",
        "Maximum Shipping Days"
    ],
    "Value": [
        df["shipping_days"].mean(),
        df["shipping_days"].median(),
        df["shipping_days"].min(),
        df["shipping_days"].max()
    ]
})

print("\nOverall Shipping Performance:")
print(shipping_summary.to_string(index=False))


# Shipping by ship mode
shipping_by_mode = (
    df.groupby("ship_mode")["shipping_days"]
    .agg(["count", "mean", "median", "min", "max"])
    .sort_values("mean")
)

print("\nShipping by Ship Mode:")
print(shipping_by_mode)


# Shipping by region
shipping_by_region = (
    df.groupby("region")["shipping_days"]
    .agg(["count", "mean", "median", "min", "max"])
    .sort_values("mean", ascending=False)
)

print("\nShipping by Region:")
print(shipping_by_region)


# Shipping by category
shipping_by_category = (
    df.groupby("category")["shipping_days"]
    .agg(["count", "mean", "median", "min", "max"])
    .sort_values("mean", ascending=False)
)

print("\nShipping by Category:")
print(shipping_by_category)


# ============================================================
# 7. IDENTIFY UNUSUALLY SLOW SHIPPING
# ============================================================

Q1_shipping = df["shipping_days"].quantile(0.25)
Q3_shipping = df["shipping_days"].quantile(0.75)

IQR_shipping = Q3_shipping - Q1_shipping

shipping_upper_bound = Q3_shipping + (1.5 * IQR_shipping)

df["shipping_outlier"] = np.where(
    df["shipping_days"] > shipping_upper_bound,
    "Slow",
    "Normal"
)

slow_shipments = (
    df[df["shipping_outlier"] == "Slow"]
    .sort_values("shipping_days", ascending=False)
)

print("\nShipping Outlier Analysis:")
print(f"Q1: {Q1_shipping:.2f}")
print(f"Q3: {Q3_shipping:.2f}")
print(f"IQR: {IQR_shipping:.2f}")
print(f"Upper Bound: {shipping_upper_bound:.2f}")
print(f"Slow shipments: {len(slow_shipments):,}")


# ============================================================
# 8. SHIPPING CHART — SHIP MODE
# ============================================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=shipping_by_mode.reset_index(),
    x="ship_mode",
    y="mean"
)

plt.title("Average Shipping Days by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Average Shipping Days")
plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_shipping_days_by_ship_mode.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 9. SHIPPING CHART — REGION
# ============================================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=shipping_by_region.reset_index(),
    x="region",
    y="mean"
)

plt.title("Average Shipping Days by Region")
plt.xlabel("Region")
plt.ylabel("Average Shipping Days")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_shipping_days_by_region.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 10. PROFITABILITY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PROFITABILITY ANALYSIS")
print("=" * 60)


# Category profitability
category_profitability = (
    df.groupby("category")
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
)

category_profitability["profit_margin"] = (
    category_profitability["profit"]
    / category_profitability["sales"]
    * 100
)

print("\nProfitability by Category:")
print(category_profitability.sort_values(
    "profit_margin",
    ascending=False
))


# Sub-category profitability
subcategory_profitability = (
    df.groupby("sub_category")
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
)

subcategory_profitability["profit_margin"] = (
    subcategory_profitability["profit"]
    / subcategory_profitability["sales"]
    * 100
)

subcategory_profitability = subcategory_profitability.sort_values(
    "profit_margin",
    ascending=False
)

print("\nProfitability by Sub-category:")
print(subcategory_profitability)


# Segment profitability
segment_profitability = (
    df.groupby("segment")
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
)

segment_profitability["profit_margin"] = (
    segment_profitability["profit"]
    / segment_profitability["sales"]
    * 100
)

print("\nProfitability by Segment:")
print(segment_profitability)


# Region profitability
region_profitability = (
    df.groupby("region")
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
)

region_profitability["profit_margin"] = (
    region_profitability["profit"]
    / region_profitability["sales"]
    * 100
)

print("\nProfitability by Region:")
print(region_profitability)


# ============================================================
# 11. PROFIT MARGIN — CATEGORY CHART
# ============================================================

plot_data = (
    category_profitability
    .sort_values("profit_margin", ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 6))

sns.barplot(
    data=plot_data,
    x="category",
    y="profit_margin"
)

plt.title("Profit Margin by Category")
plt.xlabel("Category")
plt.ylabel("Profit Margin (%)")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_profit_margin_by_category.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 12. PROFIT MARGIN — SUB-CATEGORY CHART
# ============================================================

plot_data = (
    subcategory_profitability
    .reset_index()
    .sort_values("profit_margin")
)

plt.figure(figsize=(10, 8))

sns.barplot(
    data=plot_data,
    x="profit_margin",
    y="sub_category"
)

plt.title("Profit Margin by Sub-category")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Sub-category")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_profit_margin_by_subcategory.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 13. MONTHLY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("TIME-BASED ANALYSIS")
print("=" * 60)


monthly_analysis = (
    df.groupby("year_month")
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)

print("\nMonthly Analysis:")
print(monthly_analysis.head())


# ============================================================
# 14. MONTHLY SALES CHART
# ============================================================

plt.figure(figsize=(14, 6))

sns.lineplot(
    data=monthly_analysis,
    x="year_month",
    y="sales"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Year-Month")
plt.ylabel("Sales")
plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 15. MONTHLY PROFIT CHART
# ============================================================

plt.figure(figsize=(14, 6))

sns.lineplot(
    data=monthly_analysis,
    x="year_month",
    y="profit"
)

plt.title("Monthly Profit Trend")
plt.xlabel("Year-Month")
plt.ylabel("Profit")
plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_monthly_profit_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 16. QUARTERLY ANALYSIS
# ============================================================

quarterly_analysis = (
    df.groupby(["year", "quarter"])
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
    .reset_index()
)

quarterly_analysis["sales_growth_pct"] = (
    quarterly_analysis["sales"]
    .pct_change()
    * 100
)

quarterly_analysis["profit_growth_pct"] = (
    quarterly_analysis["profit"]
    .pct_change()
    * 100
)

print("\nQuarterly Analysis:")
print(quarterly_analysis)


# ============================================================
# 17. DISCOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("DISCOUNT VS PROFIT ANALYSIS")
print("=" * 60)


# Discount by category
discount_by_category = (
    df.groupby("category")["discount"]
    .agg(["mean", "median", "min", "max"])
    .sort_values("mean", ascending=False)
)

print("\nAverage Discount by Category:")
print(discount_by_category)


# Discount by sub-category
discount_by_subcategory = (
    df.groupby("sub_category")["discount"]
    .agg(["mean", "median", "min", "max"])
    .sort_values("mean", ascending=False)
)

print("\nAverage Discount by Sub-category:")
print(discount_by_subcategory)


# Discount-profit correlation
discount_profit_corr = df["discount"].corr(df["profit"])

print(
    f"\nCorrelation between discount and profit: "
    f"{discount_profit_corr:.4f}"
)


# ============================================================
# 18. DISCOUNT VS PROFIT SCATTER PLOT
# ============================================================

plt.figure(figsize=(10, 7))

sns.scatterplot(
    data=df,
    x="discount",
    y="profit",
    alpha=0.4
)

plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_discount_vs_profit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 19. HIGH-DISCOUNT LOSS-MAKING ANALYSIS
# ============================================================

high_discount_threshold = df["discount"].quantile(0.75)

high_discount_loss = df[
    (df["discount"] >= high_discount_threshold)
    & (df["profit"] < 0)
]

print("\nHigh Discount + Loss-Making Analysis:")
print(f"High discount threshold: {high_discount_threshold:.4f}")
print(
    f"High-discount loss-making records: "
    f"{len(high_discount_loss):,}"
)


high_discount_loss_category = (
    high_discount_loss
    .groupby("category")
    .agg(
        orders=("order_id", "count"),
        sales=("sales", "sum"),
        loss=("profit", "sum"),
        avg_discount=("discount", "mean")
    )
    .sort_values("loss")
)

print("\nHigh Discount + Loss by Category:")
print(high_discount_loss_category)


# ============================================================
# 20. SUB-CATEGORY ANALYSIS
# ============================================================

subcategory_sales = (
    df.groupby("sub_category")["sales"]
    .sum()
    .sort_values(ascending=False)
)

subcategory_profit = (
    df.groupby("sub_category")["profit"]
    .sum()
    .sort_values(ascending=False)
)

top_10_subcategories = (
    subcategory_profit
    .head(10)
    .reset_index()
)

bottom_10_subcategories = (
    subcategory_profit
    .tail(10)
    .sort_values("profit")
    .reset_index()
)

print("\nTop 10 Profitable Sub-categories:")
print(top_10_subcategories)

print("\nBottom 10 Sub-categories:")
print(bottom_10_subcategories)


# ============================================================
# 21. PROFIT BY SUB-CATEGORY CHART
# ============================================================

plot_data = subcategory_profit.reset_index()

plt.figure(figsize=(10, 8))

sns.barplot(
    data=plot_data,
    x="profit",
    y="sub_category"
)

plt.title("Profit by Sub-category")
plt.xlabel("Total Profit")
plt.ylabel("Sub-category")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_profit_by_subcategory.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 22. OUTLIER ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("OUTLIER ANALYSIS")
print("=" * 60)


def outlier_summary(dataframe, column):
    """
    Calculate IQR-based outlier statistics for a numeric column.
    """

    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    outliers = dataframe[
        (dataframe[column] < lower_bound)
        | (dataframe[column] > upper_bound)
    ]

    return {
        "Column": column,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Lower Bound": lower_bound,
        "Upper Bound": upper_bound,
        "Outlier Count": len(outliers),
        "Outlier %": (len(outliers) / len(dataframe)) * 100
    }


outlier_columns = [
    "sales",
    "profit",
    "discount",
    "quantity",
    "shipping_cost",
    "shipping_days"
]

outlier_results = pd.DataFrame(
    [
        outlier_summary(df, column)
        for column in outlier_columns
    ]
)

print("\nOutlier Summary:")
print(outlier_results.to_string(index=False))


# ============================================================
# 23. OUTLIER BOXPLOTS
# ============================================================

for column in outlier_columns:

    plt.figure(figsize=(10, 4))

    sns.boxplot(x=df[column])

    plt.title(f"Outlier Analysis — {column}")
    plt.xlabel(column)

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / f"04_outlier_{column}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# 24. FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

print(f"\nFinal dataset shape: {df.shape}")

print("\nFeature columns:")
for column in [
    "shipping_days",
    "profit_margin",
    "year",
    "month",
    "month_name",
    "year_month",
    "quarter",
    "shipping_outlier"
]:
    print(f" - {column}")

print("\nMissing values in engineered columns:")

engineered_columns = [
    "shipping_days",
    "profit_margin",
    "year",
    "month",
    "month_name",
    "year_month",
    "quarter",
    "shipping_outlier"
]

print(df[engineered_columns].isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


# ============================================================
# 25. SAVE ENGINEERED DATASET
# ============================================================

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 60)
print("DAY 4 COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"\nEngineered dataset saved to:")
print(OUTPUT_FILE)

print("\nFigures saved to:")
print(FIGURES_DIR)