import pandas as pd
import os

def extract_data(raw_data_path):
    """
    Extracts data from CSV files located in the raw data layer.

    This function reads the source CSV files for channels, customers, products, 
    and sales, loading them into Pandas DataFrames for further processing.

    Args:
        raw_data_path (str): The directory path where the raw CSV files are stored.

    Returns:
        tuple: A tuple containing four Pandas DataFrames:
            - df_channels (pd.DataFrame): Data from channels.csv.
            - df_customers (pd.DataFrame): Data from customers.csv.
            - df_products (pd.DataFrame): Data from products.csv.
            - df_sales (pd.DataFrame): Data from sales.csv.
            
        Returns (None, None, None, None) if an error occurs during extraction.
    """
    print("Starting Extraction process (Extract)...")
    
    try:
        # Read CSV files into DataFrames
        df_channels = pd.read_csv(os.path.join(raw_data_path, 'channels.csv'))
        df_customers = pd.read_csv(os.path.join(raw_data_path, 'customers.csv'))
        df_products = pd.read_csv(os.path.join(raw_data_path, 'products.csv'))
        df_sales = pd.read_csv(os.path.join(raw_data_path, 'sales.csv'))
        
        print("✅ Extraction completed successfully.")
        return df_channels, df_customers, df_products, df_sales
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None, None, None, None
