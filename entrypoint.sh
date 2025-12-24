#!/bin/bash
set -e

DATA_DIR="/app/data"
PARQUET_FILE="$DATA_DIR/raw/stock_prices.parquet"
DB_FILE="$DATA_DIR/warehouse.duckdb"

# Step 1: Ingest stock data (skip if parquet already exists)
if [ ! -f "$PARQUET_FILE" ]; then
    echo "=========================================="
    echo "Step 1: Ingesting stock data..."
    echo "=========================================="
    python ingestion/ingest_stocks.py
else
    echo "✓ Stock data already exists, skipping ingestion"
fi

# Step 2: Setup DuckDB (skip if database already exists)
if [ ! -f "$DB_FILE" ]; then
    echo "=========================================="
    echo "Step 2: Setting up DuckDB..."
    echo "=========================================="
    python setup_duckdb.py
else
    echo "✓ DuckDB database already exists, skipping setup"
fi

# Step 3: Run dbt transformations
echo "=========================================="
echo "Step 3: Running dbt transformations..."
echo "=========================================="
cd dbt_project
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..

# Step 4: Start the dashboard
echo "=========================================="
echo "Step 4: Starting Streamlit dashboard..."
echo "=========================================="
exec streamlit run dashboard/app.py --server.address 0.0.0.0

