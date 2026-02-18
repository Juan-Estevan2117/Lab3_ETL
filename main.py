import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Import ETL stages
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data
from src.warehouse import dump_warehouse
from visualization.kpi_dashboard import create_dashboard

def run_pipeline():
    """
    Orchestrates the complete data pipeline:
    Data Gen -> Schema Creation -> Extract -> Transform -> Load -> Visualization.
    
    This function manages the entire workflow, from checking for raw data
    to generating the final visual dashboard.
    """
    print("="*50)
    print("🚀 Starting ETL Pipeline - AbastoYa BI")
    print("="*50)
    
    # 1. Load Configuration
    load_dotenv(override=True)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    print(f"DEBUG: Connecting as {DB_USER} to {DB_HOST}:{DB_PORT}")
    
    # 2. Synthetic Data Generation (Optional, if not exists)
    if not os.path.exists('data/raw/sales.csv'):
        print("🛠 Generating synthetic data...")
        try:
            import subprocess
            # Use sys.executable to ensure the correct Python interpreter is used (cross-platform compatibility)
            subprocess.run([sys.executable, 'data/raw/data_gen.py'], check=True)
        except Exception as e:
            print(f"❌ Error generating data: {e}")
            return
    
    # 3. Create Database Structure (DDL)
    print("📋 Executing DDL to prepare schema...")
    encoded_password = quote_plus(DB_PASSWORD)
    # Connect without specifying a database first to create it if it doesn't exist
    engine_init = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/")
    
    with open('sql/create_tables.sql', 'r') as f:
        # Clean comments and split by semicolon
        sql_content = f.read()
        sql_commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
    
    with engine_init.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.execute(text(f"USE {DB_NAME}"))
        
        # Force table recreation to ensure schema updates
        print("🧹 Recreating tables to update schema...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("DROP TABLE IF EXISTS sale;"))
        conn.execute(text("DROP TABLE IF EXISTS customer;"))
        conn.execute(text("DROP TABLE IF EXISTS product;"))
        conn.execute(text("DROP TABLE IF EXISTS channel;"))
        conn.execute(text("DROP TABLE IF EXISTS date;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        
        for command in sql_commands:
            # Ignore USE commands as we handle context above
            if command.upper().startswith("USE"):
                continue
            conn.execute(text(command))
        
        conn.commit()
    print("✅ Database schema updated.")

    # 4. EXTRACTION
    raw_path = 'data/raw'
    df_chan, df_cust, df_prod, df_sales = extract_data(raw_path)
    
    if df_sales is None:
        print("❌ Error in extraction phase. Aborting.")
        return

    # 5. TRANSFORMATION
    dim_channel, dim_customer, dim_product, dim_date, fact_sale = transform_data(
        df_chan, df_cust, df_prod, df_sales
    )

    # 6. LOAD
    load_data(dim_channel, dim_customer, dim_product, dim_date, fact_sale)

    # 7. BACKUP (Warehouse Dump)
    dump_warehouse()

    # 8. VISUALIZATION (Dashboard)
    create_dashboard()

    print("="*50)
    print("🎉 Pipeline finished successfully.")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()
