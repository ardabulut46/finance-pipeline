FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt plotly

# Copy project files
COPY ingestion/ ./ingestion/
COPY dbt_project/ ./dbt_project/
COPY dashboard/ ./dashboard/
COPY data/ ./data/
COPY setup_duckdb.py .

# Expose Streamlit port
EXPOSE 8501

# Run dashboard
CMD ["streamlit", "run", "dashboard/app.py", "--server.address", "0.0.0.0"]