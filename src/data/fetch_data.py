import yfinance as yf
import pandas as pd
from pathlib import Path
import requests
from bs4 import BeautifulSoup

RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_sp500_symbols():
    """Scrape the S&P 500 tickers from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    tickers = [row.find_all("td")[0].text.strip() for row in table.find_all("tr")[1:]]
    return tickers

def fetch_stock_data(symbol, period="1y"):
    """Download 1 year of daily OHLCV and save as CSV."""
    try:
        df = yf.download(symbol, period=period, interval="1d", auto_adjust=True)
        if df.empty:
            print(f"[WARN] No data for {symbol}")
            return None
        df.reset_index(inplace=True)
        outpath = RAW_DATA_DIR / f"{symbol}_daily.csv"
        df.to_csv(outpath, index=False)
        print(f"[INFO] Saved {symbol} → {outpath}")
        return outpath
    except Exception as e:
        print(f"[ERROR] Failed {symbol}: {e}")
        return None

if __name__ == "__main__":
    symbols = get_sp500_symbols()
    print(f"[INFO] Found {len(symbols)} S&P 500 symbols")

    for sym in symbols:
        fetch_stock_data(sym, period="1y")
