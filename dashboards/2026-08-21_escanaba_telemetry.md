## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.49 / gal
*   **Market Context:** The local retail price reflects a complex interplay between the Chicago spot market ($3.009), Michigan state tax floors (~$0.51), and active seasonal mandates. 
*   **Primary Drivers:** High regional utilization at the Whiting Refinery and active Summer Blend Mandates are the primary volatility anchors for the current cycle.

## Key Macro & Regional Indicators
*   **Crude Inventory/Pricing:** WTI is trading at **$86.25/bbl**; Brent at **$93.20/bbl**.
*   **Refinery Outlook:** High utilization forecasted for 2026 due to deferred maintenance schedules. The Whiting Refinery remains a critical Midwest stability factor with a capacity of 440k bpd.
*   **Regulatory Impacts:** Summer Blend Mandate is **ACTIVE**, adding an estimated **+$0.15** premium to the cost basis.
*   **Logistics & Transit:** Traffic indices for the US-2/US-41 corridor are currently at **1.44**, influencing regional distribution costs from neighboring hubs like Green Bay.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Margin Analysis:** 
    *   **Current Gross Margin:** $0.481
    *   **Historical Average:** $0.557
    *   **Delta:** **-0.0764 (Shrinking Margin)**
*   **Alert Status:** `False` (No automated drift alert, but margin compression is trending downward). 
*   **Action Item:** Monitor the -$0.076 difference closely; while not triggering a system drift, it indicates tightening profitability for local distributors in the Escanaba cluster compared to historical averages.