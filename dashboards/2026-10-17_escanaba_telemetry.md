# Escanaba Fuel Market Analysis Dashboard
**Date:** 2026-10-17 | **Region:** Delta County, MI | **Zip:** 49829

## 1. Daily Market Summary (Escanaba ZIP 49829)
The local retail market shows a variance of **$0.23** across the primary cluster. Pricing remains elevated above the wholesale baseline, influenced by regional logistics and refinery constraints.

| Station Name | Address | Price (USD) | Status |
| :--- | :--- | :--- | :--- |
| **Kwik Trip** | 501 N Lincoln Rd | $4.49 | Premium |
| **Krist** | 6344 US-2-41 MI-35 | $4.26 | Base |
| **Krist** | 102 N Lincoln Rd | $4.29 | Base |
| **Holiday** | 700 N Lincoln Rd | $4.28 | Base |

*   **Target Retail Average:** $4.33
*   **Traffic Impact Factor (US-2/US-41):** 1.25 (High)

## 2. Key Macro & Regional Indicators
*   **Global Crude Context:** 
    *   WTI: $101.41/bbl | Brent: $109.86/bbl
*   **Refinery & Supply Chain:**
    *   **Utilization:** 93.5% (High demand on existing capacity).
    *   **PADD 2 Constraints:** Active maintenance period in the Great Lakes region; high reliance on the Whiting Refinery hub.
    *   **Seasonality:** Summer blend mandate is **Inactive**, removing the seasonal cost premium.
*   **Logistics:** High regional demand indicated by the US-2/US-41 traffic index, likely contributing to the local price spread.

## 3. Model Performance & Margin Telemetry
**⚠️ ALERT: Drift Detected**

| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.1863 | Stable |
| **RMSE** | $0.202 | Stable |
| **R² Score** | -1.0261 | **Critical (Model Instability)** |
| **Gross Margin (Current)** | $1.0946 | High |
| **Margin Drift** | +$0.227 | **Alert Triggered** |

**Analyst Note:** The negative R² score combined with a positive margin drift suggests a significant divergence between the predictive model and real-time market data. This is likely driven by the non-linear impact of the PADD 2 refinery maintenance and the high traffic multiplier on the US-2/US-41 corridor. Immediate recalibration of the `PassThrough_HistGradientBoosting` weights is recommended.