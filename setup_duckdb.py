import duckdb
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
RAW_PATH = DATA_DIR / "raw" / "stock_prices.parquet"
DB_PATH = DATA_DIR / "warehouse.duckdb"

def setup_database():
    """
    create duckdb database and load parquet files
    """

    conn = duckdb.connect(DB_PATH)

    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

    conn.execute(f"""
    CREATE OR REPLACE TABLE raw.stock_prices AS
    SELECT * FROM read_parquet('{RAW_PATH}')
    """)

    result = conn.execute("SELECT COUNT(*) as rows, COUNT(DISTINCT symbol) as tickers FROM raw.stock_prices").fetchone()

    print(f"db created at {DB_PATH}")
    print(f"rows:{result[0]:,}")
    print(f"tickers:{result[1]}")

    print("\n📊 Sample query - Latest prices:")
    latest = conn.execute("""
        SELECT symbol, date, close 
        FROM raw.stock_prices 
        WHERE date = (SELECT MAX(date) FROM raw.stock_prices)
        ORDER BY symbol
        LIMIT 5
    """).fetchdf()
    print(latest.to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    setup_database()