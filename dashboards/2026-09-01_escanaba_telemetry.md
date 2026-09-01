# Escanaba Fuel Market Intelligence Dashboard
**Date:** 2026-09-01 | **Location:** Escanaba, MI (ZIP 49829)

## Daily Market Summary (Escanaba ZIP 49829)
*   **Current Target Retail Price:** $3.97
*   **Active Station Count:** 2
*   **Local Price Spread:** $0.00
*   **Station Status:**
    *   **Kwik Trip (501 N Lincoln Rd):** $3.97
    *   **Krist (102 N Lincoln Rd):** $3.97
    *   *Note: Data for sites 95805 and 17459 are currently null/unavailable.*

## Key Macro & Regional Indicators
*   **Global Crude Benchmark:** 
    *   WTI: $86.79/bbl
    *   Brent: $88.90/bbl
*   **Regional Refineries:** 
    *   **California:** Significant capacity impact noted in Torrance refinery (supply constraint risk).
    *   **Midwest:** High refinery outage activity recorded; inventory levels below historical averages.
    *   **Whiting Refinery:** Operational but carries historical infrastructure complexity.
*   **Policy & Market:**
    *   **Summer Blend Mandate:** **ACTIVE** (Estimated Cost Premium: +$0.15).
    *   **Chicago Spot Market (RBOB):** $3.1215/gal.
*   **Taxation Layer:**
    *   Excise Tax: $0.309
    *   Estimated Tax Floor: $0.5148

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.3802
    *   **RMSE:** $0.3824
    *   **R² Score:** -85.82 (Alert: Significant model instability/low correlation detected).
*   **Margin Analysis:**
    *   **Current Gross Margin:** $0.8485
    *   **Historical Average:** $0.7044
    *   **Margin Drift:** +$0.1441
*   **⚠️ DRIFT ALERT:** **ACTIVE**. The current margin exceeds historical averages by 14.4%. Investigation into the underlying R2 variance and drift factor is recommended to recalibrate the prediction engine.