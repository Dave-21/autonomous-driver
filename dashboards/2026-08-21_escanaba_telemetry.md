# Fuel Market Intelligence Report: Escanaba, MI (ZIP 49829)
**Report Date:** 2026-08-21 | **Status:** Active Monitoring

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.49 / gallon
*   **Chicago Spot Price:** $3.01 / gallon (Wholesale)
*   **Net Spread Analysis:** The current retail target reflects a narrow margin over the Chicago spot price, heavily influenced by local tax floors ($0.51) and the active Summer Blend mandate (+ $0.15). 
*   **Local Dynamics:** High traffic volume on US-2/US-41 (Index: 1.44) indicates significant regional demand, necessitating stable inventory management at the Lincoln Rd cluster to maintain retail competitiveness.

## Key Macro & Regional Indicators
*   **Crude Oil Outlook:** WTI ($86.20) and Brent ($93.20) remain elevated; volatility expected as refineries enter a heavy maintenance cycle for 2026.
*   **Supply Chain Constraints:** 
    *   **Refinery Activity:** Upcoming high utilization rates and scheduled outages in the U.S. refinery network may tighten regional supply downstream.
    *   **Midwest Infrastructure:** The Whiting Refinery’s ongoing legacy of heavy-crude processing influences the Great Lakes corridor's pricing stability.
*   **Regulatory Factors:** 
    *   **Summer Blend Mandate:** **ACTIVE**. Adds a confirmed $0.15 premium to local supply costs.
    *   **Taxation:** Michigan excise taxes and associated floors contribute significantly (~$0.31 - $0.51) to the final retail price.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Margin Analysis:**
    *   **Current Gross Margin:** $0.4792
    *   **Historical Avg. Margin:** $0.5525
    *   **Margin Drift:** -0.0733 (Downward trend detected)
*   **Alert Status:** **FALSE** (No immediate system alerts; however, the downward margin drift indicates increasing cost pressures from crude and environmental compliance).

**Analyst Note:** While current retail prices are stable at $3.49, the -0.0733 margin drift suggests that retailer profitability is being squeezed by the combination of high wholesale costs and mandated seasonal blends. Monitor the "Refinery Outage" factor closely over the next 60 days to anticipate potential spikes in regional demand-driven pricing.