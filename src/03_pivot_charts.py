"""
03_pivot_charts.py

Generates the core visualizations for the Superstore dataset:
- Sales by Region
- Profit by Category
- Segment-wise Sales
- Monthly Sales Trend

Reads data/Cleaned_data.csv (output of 01_clean_data.py) and saves
chart images to reports/figures/.

Usage:
    python 03_pivot_charts.py --input data/Cleaned_data.csv --outdir reports/figures
"""

import argparse
import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["order_date"] = pd.to_datetime(df["order_date"])
    logger.info(f"Loaded shape: {df.shape}")
    return df


def sales_by_region_chart(df: pd.DataFrame, outdir: str) -> None:
    region_sales = df.groupby("region")["sales"].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=region_sales.values, y=region_sales.index, palette="viridis")
    plt.title("Sales by Region")
    plt.xlabel("Total Sales")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "sales_by_region.png"), dpi=150)
    plt.close()
    logger.info("Saved sales_by_region.png")


def profit_by_category_chart(df: pd.DataFrame, outdir: str) -> None:
    category_profit = df.groupby("category")["profit"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=category_profit.index, y=category_profit.values, palette="coolwarm")
    plt.title("Profit by Category")
    plt.ylabel("Total Profit")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "profit_by_category.png"), dpi=150)
    plt.close()
    logger.info("Saved profit_by_category.png")


def segment_sales_chart(df: pd.DataFrame, outdir: str) -> None:
    segment_sales = df.groupby("segment")["sales"].sum().sort_values(ascending=False)

    plt.figure(figsize=(7, 7))
    plt.pie(segment_sales.values, labels=segment_sales.index, autopct="%1.1f%%", startangle=90)
    plt.title("Segment-wise Sales Share")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "segment_sales.png"), dpi=150)
    plt.close()
    logger.info("Saved segment_sales.png")


def monthly_sales_trend_chart(df: pd.DataFrame, outdir: str) -> None:
    df["month"] = df["order_date"].dt.to_period("M")
    monthly_sales = df.groupby("month")["sales"].sum()

    plt.figure(figsize=(14, 6))
    monthly_sales.plot(kind="line", marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "monthly_sales_trend.png"), dpi=150)
    plt.close()
    logger.info("Saved monthly_sales_trend.png")


def generate_all_charts(df: pd.DataFrame, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)
    sales_by_region_chart(df, outdir)
    profit_by_category_chart(df, outdir)
    segment_sales_chart(df, outdir)
    monthly_sales_trend_chart(df, outdir)


def main():
    parser = argparse.ArgumentParser(description="Generate pivot charts for the cleaned dataset.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV file")
    parser.add_argument("--outdir", required=True, help="Directory to save chart images")
    args = parser.parse_args()

    df = load_data(args.input)
    generate_all_charts(df, args.outdir)
    logger.info(f"All charts saved to {args.outdir}")


if __name__ == "__main__":
    main()
