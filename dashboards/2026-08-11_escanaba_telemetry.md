# 📊 Fuel Price Intelligence Dashboard: Escanaba, MI (49829)
**Report Date:** 2026-08-11 | **Status:** Monitoring Active

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Price:** $3.49 / gal
*   **Wholesale Benchmark (RBOB):** $2.8842 / gal
*   **Local Dynamics:** The spread between wholesale and retail is heavily influenced by the **Summer Blend Mandate (+0.15)** and local Michigan tax floors (~$0.50). 
*   **Logistics Note:** Proximity to Green Bay distribution hubs (Sunoco LP) provides a stable supply line, though regional demand is currently impacted by an elevated traffic index (1.15) on the US-2/US-41 corridor.

## 2. Key Macro & Regional Indicators
*   **Global Crude Outlook:** 
    *   WTI: **$83.19** | Brent: **$88.85**
*   **Regulatory Impact:** Summer Blend Mandate is **ACTIVE**. This adds a confirmed premium to the regional delivery costs.
*   **Midwest Supply Chain:** High refinery capacity in the region (notably the **Whiting Refinery**) provides significant domestic buffering against West Coast outages (e.g., Torrance refinery issues).
*   **Infrastructure Factor:** Connectivity via Green Bay terminals remains a primary logistical stabilizer for Michigan's Upper Peninsula supply chain.

## 3. Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.0065 | **RMSE:** $0.0067 (Highly precise on point estimates).
    *   **R² Score: -2.6667** ⚠️ *Action Required:* The negative R² indicates the model is currently failing to capture the underlying variance of the data or is over-fitted to noise; investigation into feature weights for "Seasonal" and "Wholesale" components is recommended.
*   **Margin Analytics:**
    *   **Current Margin:** $0.6058
    *   **Historical Average:** $0.5892
    *   **Drift:** +$0.0166 (Steady upward trend, currently below alert threshold).