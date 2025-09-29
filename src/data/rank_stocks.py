import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def compute_liquidity(df):
    return (df["Close"] * df["Volume"]).mean()


def compute_volatility(df):
    returns = df["Close"].pct_change().dropna()
    return returns.std() * np.sqrt(252)


def compute_trendiness(df):
    sma20 = df["Close"].rolling(20).mean()
    sma50 = df["Close"].rolling(50).mean()
    return (sma20 > sma50).mean()  # fraction of time bullish


def rank_stocks(limit=20):
    records = []
    for csv in RAW_DATA_DIR.glob("*_daily.csv"):
        sym = csv.stem.replace("_daily", "")
        try:
            df = pd.read_csv(csv, parse_dates=["Date"])
            liquidity = compute_liquidity(df)
            vol = compute_volatility(df)
            trend = compute_trendiness(df)

            records.append(
                {
                    "symbol": sym,
                    "liquidity": liquidity,
                    "volatility": vol,
                    "trendiness": trend,
                }
            )
        except Exception as e:
            print(f"[WARN] Skipped {sym}: {e}")

    scores = pd.DataFrame(records)

    # Normalize to 0–10
    for col in ["liquidity", "volatility", "trendiness"]:
        scores[col] = (
            10
            * (scores[col] - scores[col].min())
            / (scores[col].max() - scores[col].min())
        )

    # Weighted score
    scores["score"] = (
        scores["liquidity"] * 0.3
        + scores["volatility"] * 0.25
        + scores["trendiness"] * 0.2
    )

    scores = scores.sort_values("score", ascending=False)
    outpath = PROCESSED_DATA_DIR / "stock_universe.csv"
    scores.to_csv(outpath, index=False)
    print(f"[INFO] Saved ranked stock universe → {outpath}")

    return scores.head(limit)


if __name__ == "__main__":
    top_stocks = rank_stocks(limit=20)
    print(top_stocks)
