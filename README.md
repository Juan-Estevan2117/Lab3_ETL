# ETL Lab 3: Dimensional Data Modeling for Retail BI

## Overview
This project implements a complete **End-to-End ETL Pipeline** for a retail company's Business Intelligence system. It transforms raw transactional data (OLTP) into a dimensional Data Warehouse (OLAP) using a **Star Schema** in MySQL. The goal is to provide strategic insights through Key Performance Indicators (KPIs) and visual dashboards.

## Architecture & Dimensional Model
The project follows a Star Schema design to optimize analytical queries:
- **Fact Table (`sale`):** Contains quantitative data like quantity, total amount, and profit.
- **Dimensions:**
  - `product`: Details about categories, brands, and prices.
  - `customer`: Demographic info (city, country, age).
  - `channel`: Sales source (Physical Store, Online).
  - `date`: Time hierarchy (day, month, year, quarter).

## Technical Implementation
The pipeline is divided into specialized modules:
1. **Extraction (`etl/extract.py`):** Reads raw CSV files from `data/raw/`, performs basic validation, and handles path resolution.
2. **Transformation (`etl/transform.py`):** 
   - Generates the **Date Dimension** from sale dates.
   - Calculates derived attributes: `total_amount` (quantity * sale_price) and `profit` (amount - cost).
   - Standardizes categorical values and prepares surrogate keys.
3. **Loading (`etl/load.py`):** Uses `SQLAlchemy` and `pandas` to load data into MySQL, ensuring referential integrity by loading dimensions before the fact table.
4. **Warehouse Backup (`etl/warehouse.py`):** Automates a `mysqldump` to export the final Data Warehouse state to `data/warehouse/warehouse_dump.sql`.
5. **Visualization (`visualization/kpi_dashboard.py`):** Connects to the OLAP schema to compute KPIs and generates a multi-chart dashboard using `Seaborn` and `Matplotlib`.

## Prerequisites
- **Python 3.10+**
- **MySQL Server** installed and running.
- `mysqldump` utility available in the system PATH.

## Setup & Execution

### 1. Environment Configuration
Create a `.env` file in the root directory with your database credentials:
```env
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=etl_lab_3
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Pipeline
Execute the main orchestrator to run the full process (Data Gen -> Schema -> ETL -> Backup -> Viz):
```bash
python3 main.py
```

## Deliverables
- **`sql/create_tables.sql`**: DDL for schema creation.
- **`data/warehouse/warehouse_dump.sql`**: Complete database state backup.
- **`visualization/dashboard_kpis.png`**: Visual dashboard with business insights.
- **`sql/queries.sql`**: SQL scripts for manual KPI verification.

---
**Course:** ETL (G01) - Faculty of Engineering and Basic Sciences (UAO)
