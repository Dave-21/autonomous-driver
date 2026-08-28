# ⛽ Escanaba, MI Fuel Market Intelligence Report
**Date:** 2026-08-28 | **Region:** Delta County (Zip 49829)

---

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.062
*   **Active Station Count:** 4
*   **Local Price Spread:** $0.04 (Indicates high local competition and price parity)
*   **Cluster Status:** High. Prices at Kwik Trip ($4.05) and Holiday ($4.05) are currently at the floor, while Krist leads the cluster at $4.09.
*   **Actionable Insight:** The tight spread suggests a "price-taker" environment where retailers are responding rapidly to regional benchmarks.

---

## 2. Key Macro & Regional Indicators
| Factor | Data Point | Impact Analysis |
| :--- | :--- | :--- |
| **Global Crude (WTI/Brent)** | $83.53 / $89.70 | Stable baseline; high Brent premium persists. |
| **RBOB Spot Market** | $3.3842 / gal | Primary driver for regional retail volatility. |
| **Summer Blend Mandate** | **Active** (+$0.15) | Ongoing cost premium remains factored into retail. |
| **Refinery Health** | High Utilization | High utilization expected in 2026; monitoring Whiting Refinery capacity. |
| **Supply Logistics** | Green Bay Hubs | Stable downstream supply via Sunoco LP terminals. |
| **Traffic Index** | 1.44 | Moderate local demand pressure on transit corridors. |
| **Michigan Tax Floor** | $0.5306 | Included in total retail calculation. |

---

## 3. Model Performance & Margin Telemetry
| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.504 | Stable |
| **RMSE** | $0.5043 | Stable |
| **R² Score** | -751.51 | ⚠️ **CRITICAL ALERT** |
| **Gross Margin (Current)** | $0.6778 | Stable |
| **Margin Drift** | -0.003 | No Action Required |

**MLOps Note:** The **R² score of -751.51** indicates a severe model degradation or a significant distribution shift in the underlying features (likely related to the transition in refinery outage reporting or volatility in the RBOB spot market). **Immediate retraining or feature re-engineering is recommended for the HistGradientBoostingRegressor model.**