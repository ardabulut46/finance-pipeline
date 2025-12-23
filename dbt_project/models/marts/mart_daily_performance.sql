WITH stock_returns AS (
    SELECT
        symbol,
        trade_date,
        sector,
        close,
        LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date) AS prev_close,
        (close - LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date)) 
            / LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date) * 100 AS daily_return_pct
    FROM {{ ref('stg_stock_prices') }}
),

sp500_returns AS (
    SELECT trade_date, daily_return_pct AS sp500_return
    FROM stock_returns
    WHERE symbol = '^GSPC'
)

SELECT 
    s.symbol,
    s.trade_date,
    s.sector,
    s.close,
    s.daily_return_pct,
    sp.sp500_return,
    s.daily_return_pct - sp.sp500_return AS alpha
FROM stock_returns s
LEFT JOIN sp500_returns sp ON s.trade_date = sp.trade_date
WHERE s.symbol != '^GSPC'