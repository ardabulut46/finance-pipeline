import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


TICKERS = [
    "AAPL", "MSFT", "GOOGL", "NVDA", "META",
    "JPM", "BAC", "GS",
    "AMZN", "TSLA","WMT",
    "JNJ", "UNH","PFE",
    "XOM", "CVX",
    "^GSPC" # S&P 500 index

]


RAW_DATA_PATH = Path(__file__).parent.parent / 'data' / 'raw'


def ingest_stock_data(tickers: list[str], years: int = 2)->pd.DataFrame:
    """
    pull stock data from yfinance and return a pandas dataframe
    historical data for given tickers and years    
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)

    all_data=[]

    for ticker in tickers:
        print(f"fetching data for {ticker}")
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)

            if df.empty:
                print(f"no data found for {ticker}")
                continue

            df = df.reset_index()
            df["symbol"] = ticker
            df = df.rename(columns={"Date":"date","Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})    
            df = df[["date", "symbol", "open", "high","low","close","volume"]]
            all_data.append(df)
            print(f"{len(df)} rows")

        except Exception as e:
            print(f"error fetching data for {ticker}: {e}")
        
    return pd.concat(all_data, ignore_index=True)


def save_to_parquet(df: pd.DataFrame, path:Path)-> None:
    """
    save df to parquet, if exists then overwrite -- idempotent
    """
    path.mkdir(parents=True, exist_ok=True)
    output_file = path / "stock_prices.parquet"
    df.to_parquet(output_file, index=False)
    print(f"saved {len(df)} rows to {output_file}")

def main():
    print("=" * 50)
    print("stock data ingestion")
    print("=" * 50)

    df = ingest_stock_data(TICKERS)
    save_to_parquet(df, RAW_DATA_PATH)

    print("\n📊 Data summary:")
    print(f"   Tickers: {df['symbol'].nunique()}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Total rows: {len(df)}")


if __name__ == "__main__":
    main()

