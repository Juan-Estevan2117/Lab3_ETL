import pandas as pd
import os

def extract_data(raw_data_path):
    """
    Extrae los datos desde los archivos CSV de la capa cruda.
    """
    print("Iniciando proceso de Extracción (Extract)...")
    
    try:
        df_channels = pd.read_csv(os.path.join(raw_data_path, 'channels.csv'))
        df_customers = pd.read_csv(os.path.join(raw_data_path, 'customers.csv'))
        df_products = pd.read_csv(os.path.join(raw_data_path, 'products.csv'))
        df_sales = pd.read_csv(os.path.join(raw_data_path, 'sales.csv'))
        
        print("✅ Extracción completada con éxito.")
        return df_channels, df_customers, df_products, df_sales
        
    except Exception as e:
        print(f"Error durante la extracción: {e}")
        return None, None, None, None
