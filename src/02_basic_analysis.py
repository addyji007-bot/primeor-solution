"""
02_basic_analysis.py

Basic sales/profit analysis on the cleaned Superstore dataset.
Reads data/Cleaned_data.csv (output of 01_clean_data.py) and prints
key business metrics.

Usage:
    python 02_basic_analysis.py --input data/Cleaned_data.csv
"""

import argparse
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    logger.info(f"Loaded shape: {df.shape}")
    return df


def total_sales(df: pd.DataFrame) -> float:
    return df["sales"].sum()


def total_profit(df: pd.DataFrame) -> float:
    return df["profit"].sum()


def average_discount(df: pd.DataFrame) -> float:
    return df["discount"].mean()


def top5_products_by_sales(df: pd.DataFrame) -> pd.Series:
    return (
        df.groupby("product_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )


def top5_loss_making_products(df: pd.DataFrame) -> pd.Series:
    return (
        df.groupby("product_name")["profit"]
        .sum()
        .sort_values()
        .head(5)
    )


def region_wise_sales(df: pd.DataFrame) -> pd.Series:
    return (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
    )


# ----- Additional analysis -----

def category_wise_sales_profit(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category")[["sales", "profit"]]
        .sum()
        .sort_values("sales", ascending=False)
    )


def profit_margin_by_category(df: pd.DataFrame) -> pd.Series:
    grouped = df.groupby("category")[["sales", "profit"]].sum()
    margin = (grouped["profit"] / grouped["sales"] * 100).round(2)
    return margin.sort_values(ascending=False)


def yearly_sales_trend(df: pd.DataFrame) -> pd.Series:
    return df.groupby("year")["sales"].sum().sort_index()


def segment_wise_profit(df: pd.DataFrame) -> pd.Series:
    return (
        df.groupby("segment")["profit"]
        .sum()
        .sort_values(ascending=False)
    )


def run_analysis(df: pd.DataFrame) -> None:
    logger.info(f"Total Sales: {total_sales(df):,.2f}")
    logger.info(f"Total Profit: {total_profit(df):,.2f}")
    logger.info(f"Average Discount: {average_discount(df):.2%}")

    logger.info("\nTop 5 Products by Sales:")
    logger.info(top5_products_by_sales(df))

    logger.info("\nTop 5 Loss-Making Products:")
    logger.info(top5_loss_making_products(df))

    logger.info("\nRegion-wise Sales:")
    logger.info(region_wise_sales(df))

    logger.info("\nCategory-wise Sales & Profit:")
    logger.info(category_wise_sales_profit(df))

    logger.info("\nProfit Margin % by Category:")
    logger.info(profit_margin_by_category(df))

    logger.info("\nYearly Sales Trend:")
    logger.info(yearly_sales_trend(df))

    logger.info("\nSegment-wise Profit:")
    logger.info(segment_wise_profit(df))


def main():
    parser = argparse.ArgumentParser(description="Run basic sales/profit analysis.")
    parser.add_argument("--input", required=True, help="Path to cleaned CSV file")
    args = parser.parse_args()

    df = load_data(args.input)
    run_analysis(df)


if __name__ == "__main__":
    main()
