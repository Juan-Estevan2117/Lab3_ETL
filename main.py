import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Importar las fases del ETL
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data
from src.warehouse import dump_warehouse
from visualization.kpi_dashboard import create_dashboard

def run_pipeline():
    """
    Orquesta el pipeline de datos completo: 
    Data Gen -> Schema Creation -> Extract -> Transform -> Load -> Visualization.
    """
    print("="*50)
    print("🚀 Iniciando Pipeline ETL - AbastoYa BI")
    print("="*50)
    
    # 1. Cargar configuración
    load_dotenv(override=True)
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    print(f"DEBUG: Conectando como {DB_USER} a {DB_HOST}:{DB_PORT}")
    
    # 2. Generación de datos sintéticos (Opcional, si no existen)
    if not os.path.exists('data/raw/sales.csv'):
        print("🛠 Generando datos sintéticos...")
        os.system('python3 data/raw/data_gen.py')
    
    # 3. Crear Estructura de Base de Datos (DDL)
    print("📋 Ejecutando DDL para preparar el esquema...")
    encoded_password = quote_plus(DB_PASSWORD)
    # Primero nos conectamos sin base de datos para crearla si no existe
    engine_init = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/")
    
    with open('sql/create_tables.sql', 'r') as f:
        # Limpiar comentarios y separar por punto y coma
        sql_content = f.read()
        sql_commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
    
    with engine_init.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.execute(text(f"USE {DB_NAME}"))
        
        # Forzar recreación de tablas para asegurar que las nuevas columnas existan
        print("🧹 Recreando tablas para actualizar esquema...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("DROP TABLE IF EXISTS sale;"))
        conn.execute(text("DROP TABLE IF EXISTS customer;"))
        conn.execute(text("DROP TABLE IF EXISTS product;"))
        conn.execute(text("DROP TABLE IF EXISTS channel;"))
        conn.execute(text("DROP TABLE IF EXISTS date;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        
        for command in sql_commands:
            # Ignorar comandos USE ya que lo manejamos arriba
            if command.upper().startswith("USE"):
                continue
            conn.execute(text(command))
        
        conn.commit()
    print("✅ Esquema de base de datos actualizado.")

    # 4. EXTRACCIÓN
    raw_path = 'data/raw'
    df_chan, df_cust, df_prod, df_sales = extract_data(raw_path)
    
    if df_sales is None:
        print("❌ Error en la fase de extracción. Abortando.")
        return

    # 5. TRANSFORMACIÓN
    dim_channel, dim_customer, dim_product, dim_date, fact_sale = transform_data(
        df_chan, df_cust, df_prod, df_sales
    )

    # 6. CARGA
    load_data(dim_channel, dim_customer, dim_product, dim_date, fact_sale)

    # 7. RESPALDO (Warehouse Dump)
    dump_warehouse()

    # 8. VISUALIZACIÓN (Dashboard)
    create_dashboard()

    print("="*50)
    print("🎉 Pipeline finalizado exitosamente.")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()
