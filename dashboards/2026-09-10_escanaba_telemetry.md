# Fuel Market Intelligence Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-10 | **Status:** ⚠️ DRIFT ALERT DETECTED

## Daily Market Summary (Escanaba ZIP 49829)
*   **Retail Price Average:** $4.275
*   **Active Cluster Size:** 4 Stations
*   **Local Price Spread:** $0.02 (High Competition)
*   **Price Points:**
    *   Kwik Trip: $4.27
    *   Krist (Site 1): $4.29
    *   Krist (Site 2): $4.27
    *   Holiday: $4.27
*   **Market Sentiment:** Tight competition. Retailers are maintaining a narrow margin of variance, suggesting a highly price-sensitive local corridor.

## Key Macro & Regional Indicators
*   **Crude Dynamics:** WTI is trading at $100.33/bbl; Brent at $105.67/bbl.
*   **Refinery Capacity:** U.S. refineries are operating at 97% capacity. Global supply constraints due to regional conflicts are exerting upward pressure on refined products.
*   **Infrastructure Health:** The Whiting Refinery (Midwest hub) remains a critical high-capacity asset (440k bbl/day), though the 2026 maintenance schedule and global supply tightening create a volatile "squeeze" on inventory.
*   **Regulatory & Logistics:** 
    *   **Summer Blend Mandate:** ACTIVE (+$0.15 premium).
    *   **Midwest Supply Hubs:** Stable logistics confirmed via Green Bay terminals.
    *   **Taxation:** Michigan excise tax of $0.309 with a total tax floor of $0.5178.
*   **Spot Market:** RBOB Wholesale is holding at $3.1703/gal.

## Model Performance & Margin Telemetry
*   **Model Type:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.1047
    *   **RMSE:** $0.1366
    *   **R² Score:** -0.7361 (Warning: Low predictive correlation)
*   **Margin Analysis:**
    *   **Current Gross Margin:** $1.1047
    *   **Historical Average:** $0.7753
    *   **Margin Drift:** +$0.3294
*   **⚠️ DRIFT ALERT:** **TRUE**. The model is experiencing significant drift from historical baselines. The negative R² score and high margin drift suggest that external volatility (likely related to the refinery squeeze and global supply disruptions) is currently outstripping the model's historical training features. 

**Action Item:** Immediate review of feature weights for "Refinery Outages" and "Global Conflict Impact" is recommended to recalibrate the prediction engine.