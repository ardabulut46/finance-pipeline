SELECT 
    symbol,
    date::DATE AS trade_date,
    open,
    high,
    low,
    close,
    volume,
    CASE 
        WHEN symbol IN ('AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META') THEN 'Tech'
        WHEN symbol IN ('JPM', 'BAC', 'GS') THEN 'Finance'
        WHEN symbol IN ('AMZN', 'TSLA', 'WMT') THEN 'Consumer'
        WHEN symbol IN ('JNJ', 'UNH', 'PFE') THEN 'Healthcare'
        WHEN symbol IN ('XOM', 'CVX') THEN 'Energy'
        WHEN symbol = '^GSPC' THEN 'Index'
    END AS sector
FROM raw.stock_prices