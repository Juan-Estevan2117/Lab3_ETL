import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Styling
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_dashboard():
    """
    Generates a visual dashboard by reading SQL queries from the sql/queries.sql file.
    Ensures consistency between lab documentation and implementation.
    """
    print("Iniciando generación de Dashboard de Visualización...")
    
    # Load environment variables
    load_dotenv()
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    encoded_password = quote_plus(DB_PASSWORD)
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    try:
        # --- LOAD QUERIES FROM THE SQL FILE ---
        # The script parses the sql/queries.sql file to avoid hardcoded redundancy.
        with open('sql/queries.sql', 'r') as f:
            sql_file_content = f.read()
            # Split by semicolon and clean each query
            raw_queries = [q.strip() for q in sql_file_content.split(';') if q.strip()]
            
        # 1. Income by Category (Query 1)
        df_cat = pd.read_sql(raw_queries[0], con=engine)
        
        # 2. Distribution by Channel (Query 2)
        df_channel = pd.read_sql(raw_queries[1], con=engine)

        # 3. Monthly Sales Trend (Query 3)
        df_trend = pd.read_sql(raw_queries[2], con=engine)
        
        # 4. Most Profitable Brands (Query 4) - Replaces previous Category Margin
        df_brands = pd.read_sql(raw_queries[3], con=engine)

        # --- DASHBOARD CREATION ---
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dashboard de Inteligencia de Negocios - Supermercado "AbastoYa"', fontsize=20, fontweight='bold')

        # Chart 1: Revenue by Category
        sns.barplot(data=df_cat, x='revenue', y='category', ax=axes[0, 0], palette='viridis', hue='category', legend=False)
        axes[0, 0].set_title('Ingresos Totales por Categoría', fontsize=14)
        axes[0, 0].set_xlabel('Ingresos ($)')

        # Chart 2: Monthly Evolution (Revenue vs Profit)
        sns.lineplot(data=df_trend, x='month', y='revenue', marker='o', ax=axes[0, 1], label='Ingresos', color='blue')
        sns.lineplot(data=df_trend, x='month', y='profit', marker='s', ax=axes[0, 1], label='Ganancia', color='green')
        axes[0, 1].set_title('Tendencia Mensual: Ingresos vs Ganancias', fontsize=14)
        axes[0, 1].set_xticks(df_trend['month'])
        axes[0, 1].legend()

        # Chart 3: Channel Distribution (Pie Chart)
        axes[1, 0].pie(df_channel['revenue'], labels=df_channel['channel'], autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        axes[1, 0].set_title('Distribución de Ingresos por Canal', fontsize=14)

        # Chart 4: Most Profitable Brands (Fulfilling Req. 4 from PDF)
        sns.barplot(data=df_brands, x='total_profit', y='brand', ax=axes[1, 1], palette='flare', hue='brand', legend=False)
        axes[1, 1].set_title('Marcas más Rentables (Ganancia Total)', fontsize=14)
        axes[1, 1].set_xlabel('Ganancia ($)')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        # Save the dashboard
        output_path = 'visualization/dashboard_kpis.svg'
        plt.savefig(output_path)
        print(f"✅ Dashboard generado exitosamente en: {output_path}")
        
    except Exception as e:
        print(f"Error al generar el dashboard: {e}")

if __name__ == "__main__":
    create_dashboard()
