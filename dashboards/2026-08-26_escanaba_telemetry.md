# Fuel Market Analysis Report: Escanaba, MI (49829)
**Date:** August 26, 2026
**Status:** ⚠️ **ALERT: High Margin Drift Detected**

---

## 1. Daily Market Summary (Escanaba ZIP 49829)
The local market in Escanaba remains stable but highly competitive, characterized by a narrow pricing spread and high consistency across major retailers.

*   **Current Average Retail:** $4.08 / gal
*   **Active Stations:** 4
*   **Price Variance:** $\pm$ $0.04 (Highly localized competition)
*   **Current Status:** Stable. Retailers (Kwik Trip, Krist, Holiday) are pricing in a tight band, reflecting stable local demand despite broader macro volatility.

---

## 2. Key Macro & Regional Indicators
The following factors are influencing the current price floor and regional logistics:

*   **Crude & Supply Chain:** 
    *   **WTI/Brent:** $81.48 / $86.20.
    *   **Refinery Risk:** High. Significant outages in California (Torrance) and a global "fragile energy crisis" due to 95%+ refinery utilization indicate potential upstream volatility.
*   **Regulatory & Seasonal:** 
    *   **Summer Blend:** Active (+$0.15 estimated cost premium).
    *   **Taxes:** Michigan excise tax of $0.309 ($0.502 total floor) remains a fixed pressure point.
*   **Midwest Logistics:**
    *   **Whiting Refinery:** Operating as a stable hub for local inventory.
    *   **Traffic Index:** 1.15 (Indicates elevated local logistics complexity for the US-2/US-41 corridor).

---

## 3. Model Performance & Margin Telemetry
**System Alert:** The model is reporting significant statistical anomalies and margin drift.

| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.5884 | Moderate |
| **RMSE** | $0.5886 | Moderate |
| **R² Score** | -1528.19 | **CRITICAL FAILURE** |
| **Gross Margin (Latest)** | $1.1719 | **HIGH** |
| **Margin Drift** | +$0.5175 | **ALERT** |

**MLOps Analysis:**
*   **Model Degradation:** The extreme negative $R^2$ value indicates that the current `HistGradientBoostingRegressor` model is failing to capture the relationship between inputs and target prices. This may be due to a sudden shift in regional macro factors not currently weighted in the feature set.
*   **Margin Alert:** The margin has drifted significantly ($0.5175) above the historical average ($0.6544). This suggests that while retail prices are steady, the cost of goods or logistics is moving faster than the model's predictive capability.
*   **Action Item:** Trigger manual review of the training weights for the "Refinery Outage" and "Summer Blend" features to recalibrate the model against current regional volatility.