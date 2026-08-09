# Data Cleaning Report — Superstore Dataset

## Overview

This project cleans a raw sales/order dataset (~51,000+ rows, 21 columns) 
as part of an internship data cleaning task. The full exploratory process 
is documented in `notebooks/01_data_cleaning.ipynb`; the final, reusable 
cleaning pipeline lives in `src/clean_data.py`.

The raw and cleaned data files are **not included in this repository** 
(company-confidential data). See `data_dictionary.md` for the column 
schema. Anyone cloning this repo can run the pipeline against their own 
CSV with the same column structure.

---

## Dataset

- **Rows:** ~51,325 (before cleaning)
- **Columns:** 21
- **Grain:** one row = one product line item within an order 
  (`order_id` is expected to repeat — it is **not** a unique row identifier)

---

## Cleaning Steps Performed

### 1. Fixed numeric columns stored as text
Some numeric fields (e.g. `sales`) contained thousands-separator commas 
(e.g. `"2,885"`), which caused them to load as `object` (text) instead of 
numeric type. These were stripped of commas and converted with 
`pd.to_numeric()`. This was caught only after it broke a downstream 
calculation — now checked immediately after load, before any other step.

### 2. Removed exact duplicate rows
Checked with `df.duplicated().sum()` — **54 exact duplicate rows** found 
(identical across all 21 columns) and removed.

**Explicitly avoided:** dropping duplicates on `order_id` alone (26,242 
"duplicates") or on `order_id` + `product_id` (39 "duplicates"). Both were 
inspected manually and found to be legitimate separate transactions 
(e.g. differing `shipping_cost`, `quantity`, or `profit` on the same 
order/product combination) — not data errors. Removing them would have 
deleted real sales records.

### 3. Handled missing values
Missing values were inspected before any action was taken (never blanket 
`dropna()` or blanket `fillna(mean)`):

- **`customer_name`** (several rows missing): no other column can recover 
  a customer's identity, so these were filled with `"Unknown Customer"` 
  rather than dropped — the sales/profit data in those rows is still valid 
  and worth keeping.
- **`profit`** (a small number of rows missing): `sales`, `quantity`, and 
  `discount` were present for these rows, so profit was estimated using 
  the average profit margin **per `sub_category`** (not a flat global mean, 
  which would ignore that different product types have very different 
  margins). A `profit_estimated` boolean flag column was added so these 
  estimated values remain distinguishable from originally observed data.

### 4. Standardized text columns
Columns such as `ship_mode`, `segment`, `state`, `country`, `market`, 
`region`, `category`, `sub_category`, `order_priority` were stripped of 
whitespace and title-cased. Remaining known typos/variants (e.g. 
inconsistent capitalization of the same category) were manually mapped 
to a single standard value after reviewing `.unique()` output per column.

### 5. Fixed date columns
`order_date` and `ship_date` were converted to proper datetime objects 
with `pd.to_datetime(errors='coerce')`. Rows where `ship_date` fell 
before `order_date` were flagged and inspected before any correction 
or removal.

### 6. Validated numerical values
`quantity`, `discount`, `sales`, `profit`, and `shipping_cost` were 
checked against expected ranges (e.g. `quantity > 0`, `discount` between 
0 and 1) using `.describe()` and targeted filters, rather than assumed.

### 7. Removed formatting inconsistencies
All text columns were stripped of leading/trailing whitespace as a final 
pass.

---

## Key Lesson From This Project

> A repeated value is not automatically a duplicate record.

The correct question is never *"does this ID repeat?"* — it's *"does this 
row represent the same real-world transaction as another row?"* Every 
cleaning decision in this project was made only after inspecting the 
actual rows involved, not from count numbers alone.

---

## How to Reproduce

```bash
python src/clean_data.py --input data/Raw_Dataset.csv --output data/Cleaned_data.csv
```

See `data_dictionary.md` for the expected column schema.
