import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus 

def load_data(dim_channel, dim_customer, dim_product, dim_date, fact_sale):
    """
    Carga los datos transformados a la base de datos MySQL.
    """
    print("Iniciando proceso de Carga (Load)...")
    
    # Cargar variables de entorno dentro de la función para asegurar frescura
    load_dotenv(override=True)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    encoded_password = quote_plus(DB_PASSWORD)
    
    # Conexión al motor MySQL
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    try:
        # Cargar dimensiones primero (orden importante por Foreign Keys)
        dim_channel.to_sql('channel', con=engine, if_exists='append', index=False)
        print(" -> Tabla 'channel' cargada.")
        
        dim_customer.to_sql('customer', con=engine, if_exists='append', index=False)
        print(" -> Tabla 'customer' cargada.")
        
        dim_product.to_sql('product', con=engine, if_exists='append', index=False)
        print(" -> Tabla 'product' cargada.")
        
        dim_date.to_sql('date', con=engine, if_exists='append', index=False)
        print(" -> Tabla 'date' cargada.")
        
        # Cargar tabla de hechos al final
        fact_sale.to_sql('sale', con=engine, if_exists='append', index=False)
        print(" -> Tabla de hechos 'sale' cargada.")
        
        print("✅ Carga completada con éxito.")
        
    except Exception as e:
        print(f"Error durante la carga: {e}")
        raise e
