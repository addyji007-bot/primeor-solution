"""
05_import_to_mysql.py

Imports the feature-engineered dataset (data/engineered_data.csv, output of
04_feature_engineering) into a MySQL table called `orders`.

Credentials are read from environment variables (via a local .env file,
which is git-ignored) -- never hardcode a password in this script.

Usage:
    python 05_import_to_mysql.py --input data/engineered_data.csv
"""

import argparse
import logging
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def get_engine():
    load_dotenv()  # reads .env file into environment variables

    host     = os.getenv("DB_HOST", "localhost")
    port     = os.getenv("DB_PORT", "3306")
    dbname   = os.getenv("DB_NAME")
    user     = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([dbname, user, password]):
        raise ValueError(
            "Missing DB credentials. Make sure .env exists and contains "
            "DB_NAME, DB_USER, DB_PASSWORD (see .env.example)."
        )

    conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(conn_str)


def import_data(input_path: str, table_name: str = "orders") -> None:
    logger.info(f"Reading {input_path}")
    df = pd.read_csv(input_path, parse_dates=["order_date", "ship_date"])
    logger.info(f"Loaded shape: {df.shape}")

    engine = get_engine()

    logger.info(f"Writing to MySQL table '{table_name}' (replace if exists)...")
    df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=5000)

    with engine.connect() as conn:
        result = conn.exec_driver_sql(f"SELECT COUNT(*) FROM {table_name}")
        row_count = result.scalar()

    logger.info(f"Import complete. {row_count} rows now in '{table_name}' table.")


def main():
    parser = argparse.ArgumentParser(description="Import featured dataset into MySQL.")
    parser.add_argument("--input", required=True, help="Path to Featured_data.csv")
    parser.add_argument("--table", default="orders", help="Target table name (default: orders)")
    args = parser.parse_args()

    import_data(args.input, args.table)


if __name__ == "__main__":
    main()
