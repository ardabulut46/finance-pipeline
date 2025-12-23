# Finance Analytics Pipeline

A simple ELT pipeline I built to learn data engineering concepts. Pulls stock data, transforms it with dbt, and visualizes it in a dashboard.

## What it does

- Ingests 2 years of daily stock data from Yahoo Finance
- Stores it in Parquet files and loads into DuckDB
- Transforms data using dbt (staging and mart layers)
- Serves a Streamlit dashboard for analysis

## Tech Stack

- **yfinance** - Free stock data API
- **DuckDB** - Embedded analytical database
- **dbt** - Data transformation framework
- **Streamlit** - Dashboard
- **Docker** - Containerization

## Project Structure

```
finance-pipeline/
├── ingestion/
│   └── ingest_stocks.py      # Pulls data from Yahoo Finance
├── data/
│   ├── raw/                  # Parquet files
│   └── warehouse.duckdb      # DuckDB database
├── dbt_project/
│   ├── models/
│   │   ├── staging/          # Clean raw data
│   │   └── marts/            # Analytics tables
│   └── profiles.yml
├── dashboard/
│   └── app.py                # Streamlit app
├── Dockerfile
└── docker-compose.yml
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run ingestion
python ingestion/ingest_stocks.py

# Setup database
python setup_duckdb.py

# Run dbt
cd dbt_project
dbt run
dbt test

# Start dashboard
streamlit run dashboard/app.py
```

## Docker

```bash
docker-compose up --build
```

Opens at http://localhost:8501

## Models

| Model | Description |
|-------|-------------|
| stg_stock_prices | Cleaned raw price data with sector labels |
| mart_moving_averages | 7-day and 30-day moving averages |
| mart_daily_performance | Daily returns compared to S&P 500 |
| mart_volatility | 30-day rolling standard deviation |

## Notes

Made this project out of curiosity to understand how data pipelines work. It covers the basics of ELT: extracting from an API, loading into an analytical database, transforming with dbt, and serving through a dashboard.

Not meant for production use.

