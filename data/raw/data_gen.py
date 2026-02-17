import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Configuración
fake = Faker()
NUM_SALES = 300       # Mínimo 200 requerido [cite: 105]
NUM_CUSTOMERS = 25    # Mínimo 20 requerido [cite: 107]
START_DATE = datetime(2025, 1, 1) # Inicio de los 4 meses [cite: 106]

# 1. Generar Canales (Channels)
# Adaptado a Supermercado: 2 Tiendas físicas + 1 App/Web [cite: 108]
channels_data = [
    {'channel_id': 1, 'channel': 'Supermercado - Sede Principal'},
    {'channel_id': 2, 'channel': 'Supermercado - Express Norte'},
    {'channel_id': 3, 'channel': 'App Domicilios / Online'}
]
df_channels = pd.DataFrame(channels_data)

# 2. Generar Clientes (Customers)
# Mínimo 3 países diferentes [cite: 107]
countries = ['Colombia', 'Perú', 'Ecuador']
customers_list = []

for i in range(1, NUM_CUSTOMERS + 1):
    customers_list.append({
        'customer_id': i,
        'name': fake.name(),
        'city': fake.city(),
        'country': random.choice(countries),
        'age': random.randint(18, 75)
    })
df_customers = pd.DataFrame(customers_list)

# 3. Generar Productos (Products) - ESCENARIO GROCERY CHAIN
# Requisito: Mínimo 4 marcas y 4 categorías 
products_data = [
    # Categoría: Dairy (Lácteos) - Marca: FreshFarm
    {'name': 'Whole Milk 1L', 'category': 'Dairy', 'brand': 'FreshFarm', 'unit_price': 1.20},
    {'name': 'Greek Yogurt Pack', 'category': 'Dairy', 'brand': 'FreshFarm', 'unit_price': 4.50},
    {'name': 'Cheddar Cheese Block', 'category': 'Dairy', 'brand': 'FreshFarm', 'unit_price': 5.00},
    
    # Categoría: Pantry (Despensa) - Marca: KitchenStaples
    {'name': 'Basmati Rice 1kg', 'category': 'Pantry', 'brand': 'KitchenStaples', 'unit_price': 2.80},
    {'name': 'Spaghetti 500g', 'category': 'Pantry', 'brand': 'KitchenStaples', 'unit_price': 1.10},
    {'name': 'Olive Oil 500ml', 'category': 'Pantry', 'brand': 'KitchenStaples', 'unit_price': 8.50},
    
    # Categoría: Produce (Frutas/Verduras) - Marca: GreenValley
    {'name': 'Bananas Organic (Bunch)', 'category': 'Produce', 'brand': 'GreenValley', 'unit_price': 1.50},
    {'name': 'Avocado Hass (Unit)', 'category': 'Produce', 'brand': 'GreenValley', 'unit_price': 1.80},
    {'name': 'Apples Red (1kg)', 'category': 'Produce', 'brand': 'GreenValley', 'unit_price': 3.00},
    
    # Categoría: Household (Aseo/Hogar) - Marca: CleanMax
    {'name': 'Dish Soap 750ml', 'category': 'Household', 'brand': 'CleanMax', 'unit_price': 3.20},
    {'name': 'Paper Towels (2 Rolls)', 'category': 'Household', 'brand': 'CleanMax', 'unit_price': 2.50},
    {'name': 'Laundry Detergent 1L', 'category': 'Household', 'brand': 'CleanMax', 'unit_price': 6.00}
]

# Añadir IDs y Costo unitario (margen menor en supermercados)
for i, prod in enumerate(products_data, 1):
    prod['product_id'] = i
    # En supermercados el margen suele ser pequeño, el costo es aprox 80-85% del precio
    prod['unit_cost'] = round(prod['unit_price'] * random.uniform(0.80, 0.85), 2)

df_products = pd.DataFrame(products_data)

# 4. Generar Ventas (Sales)
sales_list = []

for i in range(1, NUM_SALES + 1):
    prod = random.choice(products_data)
    cust_id = random.randint(1, NUM_CUSTOMERS)
    chan_id = random.randint(1, 3)
    
    # Fecha aleatoria
    days_offset = random.randint(0, 120)
    sale_date = START_DATE + timedelta(days=days_offset)
    
    # Cantidad: En supermercado la gente lleva más unidades (1 a 10)
    qty = random.randint(1, 10)
    
    # Descuentos ocasionales
    discount = 1.0
    if random.random() < 0.2: # 20% de probabilidad de descuento
        discount = 0.90 # 10% descuento
        
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
df_channels.to_csv('data/raw/channels.csv', index=False)
df_customers.to_csv('data/raw/customers.csv', index=False)
df_products.to_csv('data/raw/products.csv', index=False)
df_sales.to_csv('data/raw/sales.csv', index=False)

print("✅ Archivos CSV generados exitosamente para GROCERY CHAIN (Grupos 4, 9).")
print(f"Total Ventas: {len(df_sales)}")
print(f"Categorías: {df_products['category'].unique()}")