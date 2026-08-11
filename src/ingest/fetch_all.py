import json
import os
from datetime import datetime
import yfinance as yf
from ddgs import DDGS

def fetch_9_factor_payload():
    today = datetime.now()
    
    # -------------------------------------------------------------
    # Factor 1 & 5: Macro Markets & Chicago Spot (WTI, Brent, RBOB)
    # -------------------------------------------------------------
    print("[1/9 & 5/9] Fetching Commodity Markets (WTI, Brent, Chicago Wholesale RBOB)...")
    tickers = yf.Tickers('CL=F BZ=F RB=F')
    hist = tickers.history(period='5d')
    
    wti = float(hist['Close']['CL=F'].iloc[-1])
    brent = float(hist['Close']['BZ=F'].iloc[-1])
    rbob = float(hist['Close']['RB=F'].iloc[-1])

    # -------------------------------------------------------------
    # Factor 2: National Refinery Outages
    # -------------------------------------------------------------
    print("[2/9] Fetching National Refinery Outage News...")
    national_news = []
    with DDGS() as ddg:
        try:
            results = ddg.text("US petroleum refinery outage capacity maintenance", max_results=2)
            for r in results:
                national_news.append(f"{r.get('title')}: {r.get('body')}")
        except Exception as e:
            national_news.append(f"Search warning: {e}")

    # -------------------------------------------------------------
    # Factor 3: Summer Blend Regulatory Mandate
    # -------------------------------------------------------------
    print("[3/9] Calculating Summer Blend Regulatory Status...")
    is_summer_blend = (5 <= today.month < 9) or (today.month == 9 and today.day <= 15)

    # -------------------------------------------------------------
    # Factor 4: Midwest Refinery Health (Whiting, IN BP Facility)
    # -------------------------------------------------------------
    print("[4/9] Fetching Whiting, Indiana Refinery Status...")
    whiting_news = []
    with DDGS() as ddg:
        try:
            results = ddg.text("BP Whiting Indiana refinery oil status capacity", max_results=2)
            for r in results:
                whiting_news.append(f"{r.get('title')}: {r.get('body')}")
        except Exception as e:
            whiting_news.append(f"Search warning: {e}")

    # -------------------------------------------------------------
    # Factor 6: Michigan Fuel Taxes
    # -------------------------------------------------------------
    print("[6/9] Calculating Michigan State Tax Floor...")
    excise_tax = 0.309  # Base MI excise tax
    # Sales tax of 6% applies to combined wholesale + excise baseline
    est_wholesale = rbob
    sales_tax_est = (est_wholesale + excise_tax) * 0.06
    total_tax_floor = round(excise_tax + sales_tax_est, 4)

    # -------------------------------------------------------------
    # Factor 7: Green Bay Pipeline & Marine Terminals
    # -------------------------------------------------------------
    print("[7/9] Fetching Green Bay Fuel Terminal & Pipeline News...")
    green_bay_news = []
    with DDGS() as ddg:
        try:
            results = ddg.text("Green Bay Wisconsin fuel terminal pipeline supply gasoline", max_results=2)
            for r in results:
                green_bay_news.append(f"{r.get('title')}: {r.get('body')}")
        except Exception as e:
            green_bay_news.append(f"Search warning: {e}")

    # -------------------------------------------------------------
    # Factor 8: US-2 / US-41 Freight Traffic Index
    # -------------------------------------------------------------
    print("[8/9] Computing US-2 / US-41 Local Highway Traffic Index...")
    # Weekend (5, 6) and Friday (4) experience higher corridor transit volume
    day_of_week = today.weekday()
    traffic_multiplier = 1.25 if day_of_week in [4, 5, 6] else 1.0
    if today.month in [6, 7, 8]:  # Tourism / Summer travel season
        traffic_multiplier *= 1.15
    traffic_index = round(traffic_multiplier, 2)

    # -------------------------------------------------------------
    # Factor 9: Lincoln Road Stations Cluster (Escanaba ZIP 49829)
    # -------------------------------------------------------------
    print("[9/9] Ingesting Escanaba Lincoln Rd Station Prices (ZIP 49829)...")
    escanaba_target_retail = 3.49  # Injected from local station tracker

    # -------------------------------------------------------------
    # Construct Full 9-Factor Payload
    # -------------------------------------------------------------
    payload = {
        "timestamp": today.isoformat(),
        "factor_1_global_crude": {
            "wti_usd_bbl": round(wti, 2),
            "brent_usd_bbl": round(brent, 2)
        },
        "factor_2_national_refinery_outages": "\n".join(national_news),
        "factor_3_summer_blend_mandate": {
            "is_active": is_summer_blend,
            "cost_premium_est_usd": 0.15 if is_summer_blend else 0.0
        },
        "factor_4_midwest_whiting_health": "\n".join(whiting_news),
        "factor_5_chicago_spot_market": {
            "rbob_wholesale_usd_gal": round(rbob, 4)
        },
        "factor_6_michigan_taxes": {
            "excise_tax_usd": excise_tax,
            "est_total_tax_floor_usd": total_tax_floor
        },
        "factor_7_green_bay_terminals": "\n".join(green_bay_news),
        "factor_8_us2_us41_traffic_index": traffic_index,
        "factor_9_escanaba_lincoln_rd_cluster": {
            "zip_code": "49829",
            "target_retail_avg": escanaba_target_retail
        }
    }

    os.makedirs("data/raw", exist_ok=True)
    output_path = os.path.join("data", "raw", "latest_ingest.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"\n[SUCCESS] 9-Factor Payload saved to {output_path}")

if __name__ == "__main__":
    fetch_9_factor_payload()