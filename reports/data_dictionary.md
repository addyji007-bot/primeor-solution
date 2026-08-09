# Data Dictionary

The raw and cleaned datasets are excluded from this repository (`.gitignore`) 
since this is company-provided data from an internship task. This document 
describes the schema so the cleaning code in `src/` and `notebooks/` can be 
understood without needing access to the actual data.

| Column          | Type    | Description                                      |
|-----------------|---------|---------------------------------------------------|
| order_id        | string  | Order identifier. NOT unique per row — one order can contain multiple product line items. |
| order_date      | date    | Date the order was placed. |
| ship_date       | date    | Date the order was shipped. Should never be earlier than order_date. |
| ship_mode       | string  | Shipping method (e.g. Standard Class, First Class). |
| customer_name   | string  | Name of the customer who placed the order. |
| segment         | string  | Customer segment (Consumer, Corporate, Home Office). |
| state           | string  | State/province of the customer. |
| country         | string  | Country of the customer. |
| market          | string  | Broad market grouping (e.g. US, APAC, EMEA, LATAM, Africa). |
| region          | string  | Sub-region within the market. |
| product_id      | string  | Product identifier. |
| category        | string  | High-level product category. |
| sub_category    | string  | Product sub-category. |
| product_name    | string  | Full product name/description. |
| sales            | float  | Sale amount for the line item. |
| quantity        | int     | Number of units sold in the line item. |
| discount        | float   | Discount applied, expected range 0–1. |
| profit          | float   | Profit for the line item. Can be negative. |
| shipping_cost   | float   | Cost of shipping the line item. |
| order_priority  | string  | Priority level of the order (e.g. Medium, High). |
| year            | int     | Order year. |

**Row grain:** one row = one product line item within an order (not one row 
per order). `order_id` will legitimately repeat.
