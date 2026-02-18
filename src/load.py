import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus 

def load_data(dim_channel, dim_customer, dim_product, dim_date, fact_sale):
    """
    Loads transformed data into the MySQL Data Warehouse.

    This function establishes a connection to the database and appends the 
    DataFrame content to the corresponding tables. It strictly follows a 
    specific order to satisfy Foreign Key constraints.

    Args:
        dim_channel (pd.DataFrame): Transformed Channel dimension data.
        dim_customer (pd.DataFrame): Transformed Customer dimension data.
        dim_product (pd.DataFrame): Transformed Product dimension data.
        dim_date (pd.DataFrame): Transformed Date dimension data.
        fact_sale (pd.DataFrame): Transformed Fact table data.
    
    Raises:
        Exception: Propagates any error that occurs during the database transaction.
    """
    print("Starting Load process (Load)...")
    
    # Reload environment variables to ensure fresh configuration
    load_dotenv(override=True)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    encoded_password = quote_plus(DB_PASSWORD)
    
    # Create SQLAlchemy engine connection
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    try:
        # Load Dimension Tables first (Critical for Referential Integrity)
        dim_channel.to_sql('channel', con=engine, if_exists='append', index=False)
        print(" -> Table 'channel' loaded.")
        
        dim_customer.to_sql('customer', con=engine, if_exists='append', index=False)
        print(" -> Table 'customer' loaded.")
        
        dim_product.to_sql('product', con=engine, if_exists='append', index=False)
        print(" -> Table 'product' loaded.")
        
        dim_date.to_sql('date', con=engine, if_exists='append', index=False)
        print(" -> Table 'date' loaded.")
        
        # Load Fact Table last
        fact_sale.to_sql('sale', con=engine, if_exists='append', index=False)
        print(" -> Fact Table 'sale' loaded.")
        
        print("✅ Load completed successfully.")
        
    except Exception as e:
        print(f"Error during load: {e}")
        raise e
