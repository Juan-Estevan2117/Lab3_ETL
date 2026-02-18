import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Configuración de estilos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_dashboard():
    """
    Genera un dashboard visual con los KPIs críticos del negocio.
    """
    print("Iniciando generación de Dashboard de Visualización...")
    
    # Cargar variables de entorno
    load_dotenv()
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    encoded_password = quote_plus(DB_PASSWORD)
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    try:
        # --- CONSULTAS ---
        
        # 1. Ingresos por Categoría
        df_cat = pd.read_sql("""
            SELECT p.category, SUM(s.total_amount) AS revenue 
            FROM sale s JOIN product p ON s.product_idproduct = p.id_product 
            GROUP BY p.category ORDER BY revenue DESC
        """, con=engine)
        
        # 2. Tendencia de Ventas Mensuales
        df_trend = pd.read_sql("""
            SELECT d.month, SUM(s.total_amount) AS revenue, SUM(s.profit) AS profit
            FROM sale s JOIN date d ON s.date_iddate = d.id_date
            GROUP BY d.month ORDER BY d.month
        """, con=engine)
        
        # 3. Canales más efectivos
        df_channel = pd.read_sql("""
            SELECT c.channel, SUM(s.total_amount) AS revenue
            FROM sale s JOIN channel c ON s.channel_idchannel = c.id_channel
            GROUP BY c.channel
        """, con=engine)
        
        # 4. KPI Adicional: Profit Margin per Category
        df_margin = pd.read_sql("""
            SELECT p.category, (SUM(s.profit) / SUM(s.total_amount)) * 100 AS margin
            FROM sale s JOIN product p ON s.product_idproduct = p.id_product
            GROUP BY p.category ORDER BY margin DESC
        """, con=engine)

        # --- CREACIÓN DEL DASHBOARD ---
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dashboard de Inteligencia de Negocios - Supermercado "AbastoYa"', fontsize=20, fontweight='bold')

        # Gráfico 1: Ingresos por Categoría
        sns.barplot(data=df_cat, x='revenue', y='category', ax=axes[0, 0], palette='viridis', hue='category', legend=False)
        axes[0, 0].set_title('Ingresos Totales por Categoría', fontsize=14)
        axes[0, 0].set_xlabel('Ingresos ($)')

        # Gráfico 2: Evolución Mensual
        sns.lineplot(data=df_trend, x='month', y='revenue', marker='o', ax=axes[0, 1], label='Ingresos', color='blue')
        sns.lineplot(data=df_trend, x='month', y='profit', marker='s', ax=axes[0, 1], label='Ganancia', color='green')
        axes[0, 1].set_title('Tendencia Mensual: Ingresos vs Ganancias', fontsize=14)
        axes[0, 1].set_xticks(df_trend['month'])
        axes[0, 1].legend()

        # Gráfico 3: Distribución por Canal (Pie Chart)
        axes[1, 0].pie(df_channel['revenue'], labels=df_channel['channel'], autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        axes[1, 0].set_title('Distribución de Ingresos por Canal', fontsize=14)

        # Gráfico 4: Margen de Utilidad por Categoría
        sns.barplot(data=df_margin, x='margin', y='category', ax=axes[1, 1], palette='magma', hue='category', legend=False)
        axes[1, 1].set_title('Margen de Utilidad (%) por Categoría', fontsize=14)
        axes[1, 1].set_xlabel('Margen (%)')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        # Guardar el dashboard
        output_path = 'visualization/dashboard_kpis.png'
        plt.savefig(output_path)
        print(f"✅ Dashboard generado exitosamente en: {output_path}")
        
    except Exception as e:
        print(f"Error al generar el dashboard: {e}")

if __name__ == "__main__":
    create_dashboard()
