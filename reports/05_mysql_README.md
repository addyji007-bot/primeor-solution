# Import into MySQL & SQL Analysis 

## Overview

this moves the feature-engineered dataset (`data/engineered_data.csv`,
output of last day 04_) into a MySQL database, then runs SQL queries covering
the required business questions plus additional queries useful for the
Power BI and forecasting work coming up next.

- Table schema: `sql/schema.sql`
- Import script: `src/05_import_to_mysql.py`
- All queries: `sql/queries.sql`
- Credentials template: `.env.example` (copy to `.env`, which is git-ignored)

---

## Setup

1. Install dependencies:
   ```bash
   pip install pymysql sqlalchemy python-dotenv pandas
   ```
2. Create the database (in MySQL Workbench, CLI, or any MySQL client):
   ```sql
   CREATE DATABASE primeor_solution;
   ```
3. Copy `.env.example` to `.env` and fill in your local MySQL
   credentials. **`.env` is git-ignored — never commit real credentials.**
4. (Optional) Run `sql/schema.sql` manually first if you want the table
   pre-created with explicit types and indexes. Otherwise, the import
   script (step below) will create the table automatically from the
   CSV's inferred types.

**Note on MySQL version:** the additional queries (section B) use
window functions (`LAG`, `RANK`, `OVER`), which require **MySQL 8.0+**.
Check your version with:
```sql
SELECT VERSION();
```
If you're on MySQL 5.7 or earlier, those specific queries will need to
be rewritten using subqueries or user-defined variables instead —
flag this if it applies to you and it can be adapted.

---

## Import

```bash
python src/05_import_to_mysql.py --input data/engineered_data.csv
```

This loads `engineered_data.csv` into a table called `orders`, replacing
it if it already exists (so you can re-run this safely after any
upstream change to Day 4's output).

**Verify the import:**
```sql
SELECT COUNT(*) FROM orders;
SELECT * FROM orders LIMIT 5;
```

---

## Required Queries

All in `sql/queries.sql`, section A:

1. Top 10 profitable products
2. Top 10 customers by sales
3. Region-wise total sales
4. Category-wise average profit
5. Highest discount category
6. Orders with negative profit
7. Monthly sales trend
8. Market-wise revenue analysis
9. Top-performing sub-categories
10. Ship mode usage analysis

*(Run each query and paste your actual result summary/insight here
once you've executed them — e.g. "Top profitable product is X,
contributing $Y in total profit.")*

---

## Additional Queries (Section B)

These go beyond the required list, chosen specifically because they'll
be needed once this data reaches Power BI and forecasting:

| # | Query | Why it matters later |
|---|---|---|
| 11 | Year-over-year sales growth | Forecasting needs growth rate, not just totals |
| 12 | Running total of monthly sales | Standard Power BI KPI card metric |
| 13 | Customer purchase frequency | Foundation for customer segmentation / RFM |
| 14 | Heavily discounted + loss-making products | SQL version of the Day 4 discount-vs-profit finding |
| 15 | Sub-category rank within category | Powers a "best performer per category" BI visual |
| 16 | Segment × Region sales matrix | Shape needed for a Power BI matrix/heatmap visual |
| 17 | Shipping days by region + ship mode | Operations/logistics dashboard input |
| 18 | Quarterly profit margin trend | Shows if profitability is improving or eroding over time |

Queries 11, 12, and 15 use **window functions** — in MySQL these are
written with a subquery first (to pre-aggregate), then the window
function applied on top, since MySQL doesn't allow window functions
directly on aggregated `GROUP BY` columns in the same `SELECT` the way
some other databases do. Worth understanding this pattern — it comes
up constantly in real analytics SQL.

---

## Notes

- `customer_name = 'Unknown Customer'` rows (from Day 1's missing-value
  handling) are excluded from customer-level queries (2, 13) since they
  don't represent a real, identifiable customer.
- All monetary aggregates are rounded to 2 decimal places for
  readability; `profit_margin` and growth percentages to 2 decimals as well.
- The `orders` table is rebuilt (`if_exists="replace"`) on every import
  run, so it always reflects the latest `Featured_data.csv` — no manual
  cleanup needed between runs.
- No actual query *results* (real sales/profit figures) should be
  hardcoded into this README if this repo is public and the data is
  confidential — describe findings in relative/percentage terms where
  possible (e.g. "Central region leads by roughly 40% over the next
  closest region") rather than exact dollar figures, unless you've
  confirmed with your internship that aggregate figures are fine to share.

---

## How to Reproduce

```bash
# 1. Import
python src/05_import_to_mysql.py --input data/Featured_data.csv

# 2. Run queries (MySQL Workbench, CLI, or any MySQL client)
mysql -u root -p primeor_solution < sql/queries.sql
```
