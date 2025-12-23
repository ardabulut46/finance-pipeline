SELECT
    symbol,
    trade_date,
    sector,
    close,
    STDDEV(close) OVER (
        PARTITION BY symbol 
        ORDER BY trade_date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS volatility_30d
FROM {{ ref('stg_stock_prices') }}