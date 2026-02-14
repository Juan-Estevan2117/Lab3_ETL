import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Configuración
fake = Faker()
NUM_SALES = 300       # Mínimo 200 requerido [cite: 105]
NUM_CUSTOMERS = 25    # Mínimo 20 requerido [cite: 107]
START_DATE = datetime(2025, 1, 1) # Inicio de los 4 meses

# 1. Generar Canales (Channels)
# Requisito: 3 canales (2 físicos + 1 online) [cite: 108]
channels_data = [
    {'channel_id': 1, 'channel': 'Physical Store - Centro'},
    {'channel_id': 2, 'channel': 'Physical Store - Norte'},
    {'channel_id': 3, 'channel': 'Online Store'}
]
df_channels = pd.DataFrame(channels_data)

# 2. Generar Clientes (Customers)
# Requisito: 3 países diferentes [cite: 107]
countries = ['Colombia', 'Mexico', 'Argentina']
customers_list = []

for i in range(1, NUM_CUSTOMERS + 1):
    customers_list.append({
        'customer_id': i,
        'name': fake.name(),
        'city': fake.city(),
        'country': random.choice(countries),
        'age': random.randint(18, 70)
    })
df_customers = pd.DataFrame(customers_list)

# 3. Generar Productos (Products)
# Requisito: Mínimo 4 marcas y 4 categorías [cite: 109]
# NOTA: Edita esta lista según el escenario de tu grupo (Pág. 6 del PDF)
products_data = [
    # Category: Laptops
    {'name': 'Laptop Pro 14', 'category': 'Computers', 'brand': 'TechBrand A', 'unit_price': 1200.00},
    {'name': 'Laptop Air 13', 'category': 'Computers', 'brand': 'TechBrand B', 'unit_price': 950.00},
    # Category: Peripherals
    {'name': 'Gaming Mouse', 'category': 'Peripherals', 'brand': 'GamerZ', 'unit_price': 60.00},
    {'name': 'Mechanical Keyboard', 'category': 'Peripherals', 'brand': 'GamerZ', 'unit_price': 100.00},
    # Category: Monitors
    {'name': 'Monitor 27in 4K', 'category': 'Monitors', 'brand': 'ViewBest', 'unit_price': 350.00},
    {'name': 'Monitor 24in FHD', 'category': 'Monitors', 'brand': 'ViewBest', 'unit_price': 180.00},
    # Category: Storage
    {'name': 'SSD 1TB', 'category': 'Storage', 'brand': 'FastDisk', 'unit_price': 120.00},
    {'name': 'HDD 4TB', 'category': 'Storage', 'brand': 'FastDisk', 'unit_price': 90.00}
]

# Añadir IDs y Costo unitario
for i, prod in enumerate(products_data, 1):
    prod['product_id'] = i
    # El costo suele ser menor al precio (ej. 70%)
    prod['unit_cost'] = round(prod['unit_price'] * 0.70, 2) 

df_products = pd.DataFrame(products_data)

# 4. Generar Ventas (Sales)
# Requisito: 4 meses consecutivos 
sales_list = []

for i in range(1, NUM_SALES + 1):
    # Seleccionar aleatoriamente FKs
    prod = random.choice(products_data)
    cust_id = random.randint(1, NUM_CUSTOMERS)
    chan_id = random.randint(1, 3)
    
    # Fecha aleatoria dentro de 4 meses (120 días)
    days_offset = random.randint(0, 120)
    sale_date = START_DATE + timedelta(days=days_offset)
    
    # Cantidad y precio de venta (puede tener un pequeño descuento vs precio lista)
    qty = random.randint(1, 5)
    discount = random.uniform(0.9, 1.0) # Entre 90% y 100% del precio original
    final_price = round(prod['unit_price'] * discount, 2)
    
    sales_list.append({
        'sale_id': i,
        'sale_date': sale_date.strftime('%Y-%m-%d'),
        'product_id': prod['product_id'],
        'customer_id': cust_id,
        'channel_id': chan_id,
        'quantity': qty,
        'unit_price_sale': final_price
    })

df_sales = pd.DataFrame(sales_list)

# 5. Exportar a CSV (Raw Layer)
df_channels.to_csv('channels.csv', index=False)
df_customers.to_csv('customers.csv', index=False)
df_products.to_csv('products.csv', index=False)
df_sales.to_csv('sales.csv', index=False)

print("✅ Archivos CSV generados exitosamente en la carpeta actual.")
print(f"Total Ventas: {len(df_sales)}")
print(f"Rango de Fechas: {df_sales['sale_date'].min()} a {df_sales['sale_date'].max()}")