FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY ingestion/ ./ingestion/
COPY dbt_project/ ./dbt_project/
COPY dashboard/ ./dashboard/
COPY setup_duckdb.py .
COPY entrypoint.sh .

# Fix Windows line endings and make executable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Expose Streamlit port
EXPOSE 8501

# Run the full pipeline then start dashboard
ENTRYPOINT ["./entrypoint.sh"]