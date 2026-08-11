import yfinance as yf
import pandas as pd

def fetch_macro_data():
    # Fetch WTI Crude and Brent Crude futures
    tickers = yf.Tickers('CL=F BZ=F')
    hist = tickers.history(period='5d')
    
    latest_wti = hist['Close']['CL=F'].iloc[-1]
    latest_brent = hist['Close']['BZ=F'].iloc[-1]
    
    print(f"[MACRO DATA] WTI Crude: ${latest_wti:.2f}/bbl | Brent Crude: ${latest_brent:.2f}/bbl")
    return {"wti": latest_wti, "brent": latest_brent}

if __name__ == "__main__":
    fetch_macro_data()