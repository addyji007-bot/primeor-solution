"""
clean_data.py

Final data cleaning pipeline for Primeor Solutions dataset.

This script turns the exploratory work done in
notebooks/01_data_cleaning.ipynb into a reusable, non-interactive
pipeline. It does not do any new investigation — every decision here
(what to drop, what to fill, how to estimate) was already verified
against the actual data in the notebook. This script just applies
those decisions consistently and repeatably.

Usage:
    python clean_data.py --input data/Raw_Dataset.csv --output data/Cleaned_data.csv
"""

import argparse
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

NUMERIC_COLUMNS = ["sales", "quantity", "discount", "profit", "shipping_cost"]

TEXT_COLUMNS = [
    "ship_mode", "segment", "state", "country", "market",
    "region", "category", "sub_category", "order_priority",
]

# Known typo/variant fixes found during manual inspection in the notebook.
# Add to this dictionary if new inconsistencies are found in future data.
TEXT_VALUE_FIXES = {
    # "Fisrt Class": "First Class",
}


def load_data(path: str) -> pd.DataFrame:
    logger.info(f"Loading data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Loaded shape: {df.shape}")
    return df


def fix_numeric_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Some numeric columns may be read as text due to thousands-separator
    commas (e.g. '2,885'). Strip commas and coerce to numeric."""
    for col in NUMERIC_COLUMNS:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.replace(",", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def remove_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Only exact, full-row duplicates are removed. order_id and
    order_id+product_id are NOT unique row identifiers in this dataset
    (one order can have multiple product lines) -- do not deduplicate
    on those subsets."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    logger.info(f"Removed {removed} exact duplicate rows")
    return df


def handle_missing_customer_name(df: pd.DataFrame) -> pd.DataFrame:
    missing = df["customer_name"].isnull().sum()
    if missing:
        logger.info(f"Filling {missing} missing customer_name values")
        df["customer_name"] = df["customer_name"].fillna("Unknown Customer")
    return df


def estimate_missing_profit(df: pd.DataFrame) -> pd.DataFrame:
    """Estimate missing profit using the average profit margin for that
    row's sub_category (not a flat global mean, since margins vary a lot
    by product type). Flags estimated rows in profit_estimated."""
    df["profit_estimated"] = df["profit"].isnull()

    missing = df["profit_estimated"].sum()
    if missing == 0:
        return df

    logger.info(f"Estimating {missing} missing profit values via sub_category margin")

    margin_by_subcat = (
        df.dropna(subset=["profit"])
        .groupby("sub_category")
        .apply(lambda x: x["profit"].sum() / x["sales"].sum() if x["sales"].sum() else 0)
    )

    def fill_profit(row):
        if row["profit_estimated"]:
            margin = margin_by_subcat.get(row["sub_category"], 0)
            return row["sales"] * margin
        return row["profit"]

    df["profit"] = df.apply(fill_profit, axis=1)
    return df


def standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in TEXT_COLUMNS:
        df[col] = df[col].astype(str).str.strip().str.title()
        df[col] = df[col].replace(TEXT_VALUE_FIXES)
    return df


def fix_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", dayfirst=True)
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce", dayfirst=True)

    bad_dates = df["ship_date"] < df["order_date"]
    n_bad = bad_dates.sum()
    if n_bad:
        logger.info(f"Removing {n_bad} rows where ship_date is before order_date")
        df = df[~bad_dates]

    return df


def validate_numeric_ranges(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df[df["quantity"] > 0]
    df = df[(df["discount"] >= 0) & (df["discount"] <= 1)]
    removed = before - len(df)
    if removed:
        logger.info(f"Removed {removed} rows with invalid quantity/discount values")
    return df


def clean_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df


def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df = fix_numeric_dtypes(df)
    df = remove_exact_duplicates(df)
    df = handle_missing_customer_name(df)
    df = estimate_missing_profit(df)
    df = standardize_text_columns(df)
    df = fix_dates(df)
    df = validate_numeric_ranges(df)
    df = clean_whitespace(df)
    return df


def main():
    parser = argparse.ArgumentParser(description="Clean the Superstore order dataset.")
    parser.add_argument("--input", required=True, help="Path to raw CSV file")
    parser.add_argument("--output", required=True, help="Path to save cleaned CSV file")
    args = parser.parse_args()

    df = load_data(args.input)
    df = clean_pipeline(df)

    logger.info(f"Final shape: {df.shape}")
    logger.info(f"Remaining missing values:\n{df.isnull().sum()}")

    df.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}")


if __name__ == "__main__":
    main()
