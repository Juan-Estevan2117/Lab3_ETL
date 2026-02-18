import pandas as pd

def transform_data(df_channels, df_customers, df_products, df_sales):
    """
    Transforma los datos y prepara las tablas dimensionales y de hechos.
    Incluye: Estandarización, Atributos Derivados y Claves Subrogadas.
    """
    print("Iniciando proceso de Transformación (Transform)...")
    
    # --- 1. ESTANDARIZACIÓN ---
    # Convertir categorías y marcas a Mayúsculas/Título para consistencia
    df_products['category'] = df_products['category'].str.strip().str.title()
    df_products['brand'] = df_products['brand'].str.strip().str.upper()
    df_customers['city'] = df_customers['city'].str.strip().str.title()
    df_customers['country'] = df_customers['country'].str.strip().str.title()
    
    # --- 2. GENERACIÓN DE CLAVES SUBROGADAS (SK) ---
    # Aunque ya tenemos IDs, creamos SKs para cumplir con el estándar de DW
    # Nota: En este lab usaremos los IDs originales como SKs por simplicidad en el DDL,
    # pero asegurando que sean únicos y limpios.
    dim_channel = df_channels.rename(columns={'channel_id': 'id_channel'})
    dim_customer = df_customers.rename(columns={'customer_id': 'id_customer'})
    dim_product = df_products.rename(columns={'product_id': 'id_product'})
    
    # --- 3. DIMENSIÓN DE FECHA ---
    df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'])
    dim_date = pd.DataFrame()
    dim_date['id_date'] = df_sales['sale_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['day'] = df_sales['sale_date'].dt.day
    dim_date['month'] = df_sales['sale_date'].dt.month
    dim_date['year'] = df_sales['sale_date'].dt.year
    dim_date['quarter'] = df_sales['sale_date'].dt.quarter
    dim_date = dim_date.drop_duplicates(subset=['id_date']).reset_index(drop=True)
    
    # --- 4. TABLA DE HECHOS Y ATRIBUTOS DERIVADOS ---
    # Merge con productos para obtener el costo unitario y poder calcular el profit
    df_sales_enriched = pd.merge(df_sales, df_products[['product_id', 'unit_cost']], on='product_id', how='left')
    
    # Cálculo de total_amount: cantidad * precio de venta
    df_sales_enriched['total_amount'] = df_sales_enriched['quantity'] * df_sales_enriched['unit_price_sale']
    
    # Cálculo de profit: total_amount - (cantidad * costo unitario)
    df_sales_enriched['profit'] = df_sales_enriched['total_amount'] - (df_sales_enriched['quantity'] * df_sales_enriched['unit_cost'])
    
    # Añadir el id_date
    df_sales_enriched['date_iddate'] = df_sales_enriched['sale_date'].dt.strftime('%Y%m%d').astype(int)
    
    # Selección y renombre de columnas según DDL
    fact_sale = df_sales_enriched[[
        'sale_id', 'quantity', 'unit_price_sale', 'total_amount', 'profit',
        'customer_id', 'product_id', 'channel_id', 'date_iddate'
    ]].copy()
    
    fact_sale = fact_sale.rename(columns={
        'sale_id': 'id_sale',
        'customer_id': 'customer_idcustomer',
        'product_id': 'product_idproduct',
        'channel_id': 'channel_idchannel'
    })
    
    print("✅ Transformación completada con éxito (Estandarización y Atributos Derivados aplicados).")
    return dim_channel, dim_customer, dim_product, dim_date, fact_sale