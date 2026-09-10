# Executive Market Analysis: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-10 | **Status:** ⚠️ **Margin Drift Alert Active**

## 1. Daily Market Summary (Escanaba ZIP 49829)
The local retail environment for Escanaba remains stable with low price variance across the identified cluster.

*   **Target Retail Average:** $4.275/gal
*   **Local Price Spread:** $0.02 (Tight competition)
*   **Station Breakdown:**
    *   **Kwik Trip:** $4.27
    *   **Krist (Unit 1):** $4.29 (Current market outlier)
    *   **Krist (Unit 2):** $4.27
    *   **Holiday:** $4.27
*   **Actionable Insight:** Competition is high; the $0.02 variance suggests a highly saturated local market where any price increase above $4.27 may result in immediate volume loss to adjacent competitors.

## 2. Key Macro & Regional Indicators
Market conditions are influenced by a mix of global crude volatility and regional infrastructure constraints.

*   **Crude Oil Context:** WTI is trading at $100.18/bbl; Brent at $105.62/bbl. High crude floor supports elevated retail prices.
*   **Supply Constraints:** 
    *   **Refinery Risk:** Significant outage noted at the Torrance refinery (CA). While geographically distant, it creates a tightening effect on the national gasoline and distillate supply.
    *   **Midwest Logistics:** Stability at the Whiting refinery remains a key regional anchor.
*   **Regulatory/Seasonal:**
    *   **Summer Blend:** Active (Estimated cost impact: +$0.15).
    *   **Michigan Tax Floor:** ~$0.5177 (Excise component: $0.309).
*   **Logistics Index:** US-2/US-41 Traffic Index is stable at 1.0.

## 3. Model Performance & Margin Telemetry
**System Alert:** The model is currently flagging a significant drift in gross margins.

*   **Model Type:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.1035
    *   **RMSE:** $0.1399
    *   **R² Score:** **-1.5171** (Critical: Negative R² indicates the model is performing worse than a horizontal baseline; retraining/re-calibration required).
*   **Margin Analytics:**
    *   **Current Margin:** $1.106
    *   **Historical Avg:** $0.7633
    *   **Margin Drift:** +$0.3427
*   **Alert Status:** 🚩 **DRIFT_ALERT_FLAG: TRUE**
*   **Action Item:** Immediate investigation of the `HistGradientBoostingRegressor` is required. The negative R² score suggests the model is failing to capture the correlation between the provided features (Crude, Outages, Summer Blend) and the local retail price in the 49829 zone.