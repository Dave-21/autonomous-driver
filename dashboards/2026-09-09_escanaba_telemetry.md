# Escanaba, MI Fuel Market Analysis | 2026-09-09

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.12
*   **Active Station Count:** 4
*   **Local Price Spread:** $0.30
*   **Current Pricing Data:**
    *   **Kwik Trip:** $4.27 (Highest)
    *   **Holiday:** $4.17
    *   **Krist (Lincoln Rd):** $4.07
    *   **Krist (US-2-41):** $3.97 (Lowest)
*   **Market Dynamics:** The cluster shows significant variance ($0.30 spread), suggesting high competition or varying overhead costs between the Kwik Trip and the Krist locations.

## Key Macro & Regional Indicators
*   **Global Crude Indices:**
    *   **WTI:** $95.21/bbl
    *   **Brent:** $100.66/bbl
*   **Refinery & Supply Chain:**
    *   **Capacity:** U.S. refineries are operating at high utilization (97%).
    *   **Geopolitical Impact:** Global conflicts are tightening the refined product market, creating upward pressure on regional spot prices.
    *   **Infrastructure:** Green Bay terminals remain a critical supply hub; current focus remains on regional stability despite historical pipeline vulnerabilities.
*   **Regulatory & Regional Factors:**
    *   **Summer Blend Mandate:** **ACTIVE** (Estimated +$0.15 cost premium).
    *   **Chicago Spot Market:** $3.0956/gal.
    *   **Michigan Tax Floor:** $0.5133 (includes $0.309 excise).

## Model Performance & Margin Telemetry
*   **Model Type:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.0692
    *   **RMSE:** $0.096
    *   **R² Score:** **-0.9934** ⚠️ *(Critical: Negative R² indicates model failure to capture trend; immediate retraining recommended).*
*   **Margin Analysis:**
    *   **Current Gross Margin:** $1.0244
    *   **Historical Average:** $0.7520
    *   **Margin Drift:** +$0.2724
    *   **Drift Alert:** 🚨 **ACTIVE**
*   **MLOps Action:** The significant margin drift and extremely low R² score indicate that current market volatility (likely driven by the 97% refinery utilization and summer blend costs) is outperforming the current model's training logic. Update model weights for 2026 variables immediately.