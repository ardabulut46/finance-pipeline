WITH daily_returns AS (
    SELECT
        symbol,
        trade_date,
        sector,
        close,
        (close - LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date)) 
            / NULLIF(LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date), 0) * 100 AS daily_return_pct
    FROM {{ ref('stg_stock_prices') }}
)

SELECT
    symbol,
    trade_date,
    sector,
    close,
    STDDEV(daily_return_pct) OVER (
        PARTITION BY symbol 
        ORDER BY trade_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS volatility_30d
FROM daily_returns