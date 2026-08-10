# Basic Analysis Report — Superstore Dataset

## Overview

This task performs foundational business metrics analysis on the cleaned 
dataset (`data/Cleaned_data.csv`, output of Day 1's cleaning pipeline). 
The exploratory work is in `notebooks/02_basic_analysis.ipynb`; the final 
reusable script is `src/02_basic_analysis.py`.

---

## Core Metrics (as required by the task)

| Metric | Description |
|---|---|
| Total Sales | Sum of `sales` across all rows |
| Total Profit | Sum of `profit` across all rows |
| Average Discount | Mean of `discount` across all rows |
| Top 5 Products by Sales | Products grouped and summed by `sales`, descending |
| Top 5 Loss-Making Products | Products grouped and summed by `profit`, ascending (most negative first) |
| Region-wise Sales | `sales` summed and grouped by `region` |

---

## Additional Analysis (beyond the core task)

These were added to give the numbers more context — a raw total or a 
single ranking doesn't tell you *why* something performs the way it does. 
Each addition below answers a follow-up question the six core metrics 
raise but don't answer on their own.

### Category-wise Sales & Profit
Region tells you *where* sales come from; category tells you *what* is 
actually driving revenue and profit. Useful to compare against region 
results — e.g. a region can look strong purely because it sells a 
high-volume category, not because it performs well across the board.

### Profit Margin % by Category
Total profit alone can be misleading — a category with high profit can 
still have a poor margin if its sales are proportionally much higher. 
Margin (`profit / sales`) shows efficiency, not just scale.

### Yearly Sales Trend
Using the existing `year` column to see whether sales are growing, 
flat, or declining over time — a basic but necessary check before 
drawing any other conclusions from the data.

### Segment-wise Profit
Segment (Consumer / Corporate / Home Office) is a common way businesses 
evaluate customer types. Checking profit by segment (rather than just 
sales) can reveal a segment that generates high revenue but low or 
negative profit.

---

## Notes

- All calculations use `data/Cleaned_data.csv` — the output of the Day 1 
  cleaning pipeline (`src/01_clean_data.py`) — not the raw data.
- The `profit_estimated` flag from Day 1 (rows where profit was estimated 
  due to missing values) was **not excluded** from these totals. For a 
  more conservative report, these could be filtered out with:
  ```python
  df_observed_only = df[df['profit_estimated'] == False]
  ```
- Top 5 product rankings are based on aggregated totals across all 
  transactions for that product, not single largest transactions.

---

## How to Reproduce

```bash
python src/02_basic_analysis.py --input data/Cleaned_data.csv
```
