SELECT 
    symbol,
    trade_date,
    sector,
    close,
    AVG(close) OVER (
        PARTITION BY symbol
        ORDER BY trade_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7,
    AVG(close) OVER(
        PARTITION BY symbol
        ORDER BY trade_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS ma_30
FROM {{ ref('stg_stock_prices')}}
