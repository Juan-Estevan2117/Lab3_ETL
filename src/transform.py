import pandas as pd

def transform_data(df_channels, df_customers, df_products, df_sales):
    """
    Transforms raw data into dimensional and fact tables for the Data Warehouse.
    
    This function performs cleaning, standardization, and enrichment of the data.
    It generates the necessary dimensions (Customer, Product, Channel, Date)
    and calculates derived metrics for the Fact Table.

    Args:
        df_channels (pd.DataFrame): Raw channel data.
        df_customers (pd.DataFrame): Raw customer data.
        df_products (pd.DataFrame): Raw product data.
        df_sales (pd.DataFrame): Raw sales data.

    Returns:
        tuple: A tuple containing the transformed DataFrames:
            - dim_channel (pd.DataFrame): Transformed Channel dimension.
            - dim_customer (pd.DataFrame): Transformed Customer dimension.
            - dim_product (pd.DataFrame): Transformed Product dimension.
            - dim_date (pd.DataFrame): Transformed Date dimension.
            - fact_sale (pd.DataFrame): Transformed Fact table with calculated metrics.
    """
    print("Starting Transformation process (Transform)...")
    
    # --- 1. STANDARDIZATION ---
    # Convert text fields to Title Case or Uppercase for consistency
    df_products['category'] = df_products['category'].str.strip().str.title()
    df_products['brand'] = df_products['brand'].str.strip().str.upper()
    df_customers['city'] = df_customers['city'].str.strip().str.title()
    df_customers['country'] = df_customers['country'].str.strip().str.title()
    
    # --- 2. SURROGATE KEYS (SK) PREPARATION ---
    # Rename columns to match the target Data Warehouse schema.
    # We use the original IDs as keys, ensuring they are clean and mapped correctly.
    dim_channel = df_channels.rename(columns={'channel_id': 'id_channel'})
    dim_customer = df_customers.rename(columns={'customer_id': 'id_customer'})
    dim_product = df_products.rename(columns={'product_id': 'id_product'})
    
    # --- 3. DATE DIMENSION GENERATION ---
    # Convert sale_date to datetime objects
    df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'])
    
    # Create the Date Dimension DataFrame
    dim_date = pd.DataFrame()
    # Create a unique ID for date (YYYYMMDD format)
    dim_date['id_date'] = df_sales['sale_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['day'] = df_sales['sale_date'].dt.day
    dim_date['month'] = df_sales['sale_date'].dt.month
    dim_date['year'] = df_sales['sale_date'].dt.year
    dim_date['quarter'] = df_sales['sale_date'].dt.quarter
    
    # Remove duplicates to ensure unique dates in the dimension
    dim_date = dim_date.drop_duplicates(subset=['id_date']).reset_index(drop=True)
    
    # --- 4. FACT TABLE ENRICHMENT & CALCULATION ---
    # Merge with products to get unit_cost for profit calculation
    df_sales_enriched = pd.merge(df_sales, df_products[['product_id', 'unit_cost']], on='product_id', how='left')
    
    # Calculate Total Amount: Quantity * Unit Price
    df_sales_enriched['total_amount'] = df_sales_enriched['quantity'] * df_sales_enriched['unit_price_sale']
    
    # Calculate Profit: Total Amount - (Quantity * Unit Cost)
    df_sales_enriched['profit'] = df_sales_enriched['total_amount'] - (df_sales_enriched['quantity'] * df_sales_enriched['unit_cost'])
    
    # Create the Date Foreign Key
    df_sales_enriched['date_iddate'] = df_sales_enriched['sale_date'].dt.strftime('%Y%m%d').astype(int)
    
    # Select and rename columns to match the DDL schema for the Fact Table
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
    
    print("✅ Transformation completed successfully (Standardization & Derived Attributes applied).")
    return dim_channel, dim_customer, dim_product, dim_date, fact_sale
