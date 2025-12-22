# Top-K Universe Selection Methodology

This document outlines the criteria and methodology used to select the "Top-K" universe of stocks for ML modeling in Phase 2.

## 1. Objective

The goal is to select a subset of `K` stocks (defaulting to 50) from the broader S&P 500 universe that are most suitable for the trading strategy. The primary selection criterion is **liquidity**, as this ensures that the strategy can be realistically backtested and deployed without incurring excessive transaction costs or slippage.

## 2. Methodology

The selection process is as follows:

1.  **Load Universe**: The full S&P 500 constituent list is loaded from `data/universe/sp500_constituents.csv`.

2.  **Fetch Daily Data**: To assess liquidity, 90 days of historical daily market data (`Open`, `High`, `Low`, `Close`, `Volume`) is fetched for every stock in the universe using the `yfinance` library.

3.  **Calculate Average Dollar Volume**: For each stock, the **average daily dollar volume** is calculated over the 90-day period. This is computed as:
    ```
    Average(Daily Close Price * Daily Volume)
    ```
    Dollar volume is used as a robust proxy for liquidity.

4.  **Rank and Select**:
    - Stocks are ranked in descending order based on their average daily dollar volume.
    - The top `K` stocks from this ranked list are selected as the ML universe.

5.  **Save Deliverables**:
    - The list of the top `K` selected tickers and their corresponding company information is saved to `data/processed/topK_50.csv`.

## 3. Rationale & Considerations

-   **Why Dollar Volume?**: It's a more reliable indicator of liquidity than volume alone, as it accounts for the price of the stock. A stock trading 1 million shares at $1 is far less liquid than a stock trading 100,000 shares at $500.
-   **90-Day Window**: A 90-day (approx. 3 months) lookback period is used to provide a stable, recent measure of liquidity while smoothing out short-term anomalies.
-   **Reproducibility**: The process is deterministic. Given the same S&P 500 constituent list and a fixed end date, the selection will be the same.
-   **Future Enhancements (Phase 3+)**: This methodology is a significant improvement for Phase 2. In later phases, the selection criteria will be enhanced to include:
    - **Volatility metrics**: To filter for or against stocks with certain volatility profiles.
    - **Trendiness metrics**: To identify stocks that are more suitable for trend-following or momentum strategies.
    - **Dynamic Selection**: The universe may be re-selected periodically (e.g., monthly or quarterly) to adapt to changing market conditions.
