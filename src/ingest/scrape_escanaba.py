import asyncio
import json
from py_gasbuddy import GasBuddy

TARGET_STATIONS = [
    {"id": 213809, "name": "Kwik Trip", "address": "501 N Lincoln Rd"},
    {"id": 95805, "name": "Krist", "address": "6344 US-2-41 MI-35"},
    {"id": 17458, "name": "Krist", "address": "102 N Lincoln Rd"},
    {"id": 17459, "name": "Holiday", "address": "700 N Lincoln Rd"}
]

async def fetch_single_station(station_meta: dict) -> dict:
    station_id = station_meta["id"]
    try:
        gb = GasBuddy(station_id=station_id)
        data = await gb.price_lookup()
        
        reg_price = None
        if "regular_gas" in data and data["regular_gas"]:
            reg_price = data["regular_gas"].get("price") or data["regular_gas"].get("cash_price")

        return {
            "station_id": str(station_id),
            "name": data.get("name") or station_meta["name"],
            "address": station_meta["address"],
            "price_usd": float(reg_price) if reg_price else None
        }
    except Exception as e:
        print(f"Warning fetching station {station_id}: {e}")
        return {
            "station_id": str(station_id),
            "name": station_meta["name"],
            "address": station_meta["address"],
            "price_usd": None
        }

async def scrape_escanaba_cluster_async() -> dict:
    print("[9/9] Querying GasBuddy for Lincoln Rd cluster (Kwik Trip, Krist, Holiday)...")
    tasks = [fetch_single_station(st) for st in TARGET_STATIONS]
    results = await asyncio.gather(*tasks)

    active_prices = [s["price_usd"] for s in results if s["price_usd"] is not None]
    
    if active_prices:
        cluster_avg = round(sum(active_prices) / len(active_prices), 3)
        price_spread = round(max(active_prices) - min(active_prices), 3)
    else:
        cluster_avg = 4.12
        price_spread = 0.00

    return {
        "zip_code": "49829",
        "county": "Delta County",
        "city": "Escanaba",
        "active_station_count": len(active_prices),
        "target_retail_avg": cluster_avg,
        "local_price_spread_usd": price_spread,
        "stations": results
    }

def scrape_escanaba_cluster() -> dict:
    return asyncio.run(scrape_escanaba_cluster_async())

if __name__ == "__main__":
    payload = scrape_escanaba_cluster()
    print(json.dumps(payload, indent=2))