# Fuel Market Intelligence Report: Escanaba, MI (ZIP 49829)
**Date:** August 24, 2026 | **Status:** Alert Active

## Daily Market Summary (Escanaba ZIP 49829)
*   **Current Average Retail:** $4.115 / gal
*   **Market Competition:** High density with 4 active stations in the Lincoln Rd cluster.
*   **Price Variance:** Minimal ($0.02 spread), indicating a highly synchronized local market.
*   **Primary Clusters:** Strong concentration around N. Lincoln Rd and US-2/41 corridors.

## Key Macro & Regional Indicators
*   **Crude Outlook:** WTI is trading at $85.41; Brent at $92.38. High global prices are being mitigated by regional refinery distribution.
*   **Refinery Constraints:** Anticipated maintenance schedules are tightening supply, creating upward pressure on local premiums. 
*   **Regulatory Impact:** Summer Blend Mandates remain **Active**, contributing an estimated $+0.15$ premium to the baseline cost.
*   **Midwest Hub Integrity:** The Whiting Refinery remains a primary stabilizing force for the Midwest region, despite downstream logistics challenges.
*   **Logistics & Demand:** A traffic index of 1.15 on US-2/US-41 indicates high transit volume, supporting consistent local demand volumes.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.3133
    *   **RMSE:** $0.4431
*   **Critical Alert:** **R² Score of -1.0** indicates a significant failure in model fit/predictive correlation. Immediate recalibration required.
*   **Margin Drift Analysis:**
    *   **Current Gross Margin:** $1.1274
    *   **Historical Avg:** $0.5672
    *   **Variance:** +$0.5602 (**Drift Alert Triggered**)
*   **Action Item:** The positive drift in margins coupled with the negative R² suggests that current market volatility is outstripping the model's training parameters; manual override or retraining on recent 30-day windows is recommended.