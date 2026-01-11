# Pricing & Segment Performance Validation (UFC Odds-Based Market Data) 🥊

## Project Overview
This project analyzes 10+ years of UFC fight records and pre-fight pricing data to **evaluate segment-level performance differences** (descriptive analysis).  
I cleaned and standardized the dataset, computed return metrics, and built a Power BI dashboard to explore outcomes by **weight class**, **finish method**, and **title vs. non-title bouts**.

> Note: This analysis is **descriptive (not predictive)** and is presented for analytics portfolio purposes.

## Key Findings (Title Bouts)
- Favorites show **lower average return** in title bouts (**avg ROI -9.6%**, per defined stake model).
- Certain finish-method segments exhibit **consistently negative average return** (e.g., KO/TKO-related props in this dataset).
- Underdog returns vary significantly by weight class; some title-bout segments show **positive average ROI** (e.g., **Bantamweight +28%**, **Lightweight +25%**, **Women’s Bantamweight +36.85%**).

## Tech Stack
- **Python (Pandas):** data cleaning, normalization, QA checks (missing/duplicate handling)
- **SQL (PostgreSQL):** aggregations across multiple segment dimensions
- **Power BI (DAX):** KPI measures, slicers, drill-through, conditional formatting

## Dashboard
![Dashboard Preview](dashboard_screenshot.png)

## Method Summary
1. Cleaned and standardized fight-level records (dedupe, missing values, consistent labels).
2. Computed return metrics using a consistent stake model (defined below).
3. Segmented results by weight class, title bout flag, and finish type.
4. Delivered an interactive Power BI dashboard with time filtering (2010–2024).

## Metric Definitions
- **Profit:** net profit under the chosen stake model.
- **ROI (%):** `profit / stake * 100`  
  *(If your “profit” already assumes a 100-unit stake, state that clearly.)*

## Example SQL (Segment Return by Weight Class — Title Bouts)
```sql
SELECT
  weight_class,
  ROUND(AVG(underdog_roi_pct)::numeric, 2) AS avg_underdog_roi_pct
FROM fact_market_pricing
WHERE title_bout = TRUE
GROUP BY weight_class
ORDER BY avg_underdog_roi_pct DESC;
