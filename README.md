# Superstore Data Analytics Project

An end-to-end data analytics project based on the Superstore sales dataset. The project cleans the raw data, creates dimension and fact tables, loads them into SQLite, and runs SQL queries for business insights.

## Project Overview

The analysis uses data about orders, customers, products, sales, discounts, shipping, and profit. The dataset is transformed into a star-schema-style structure containing four dimension tables and one fact table.

## Project Structure

```text
DA/
|-- data/
|   |-- raw_data/
|   |   `-- Sample - Superstore.csv
|   `-- processed_data/
|       |-- dim_customer.csv
|       |-- dim_date.csv
|       |-- dim_order.csv
|       |-- dim_product.csv
|       `-- fact_sales.csv
|-- database/
|   |-- superstore.db
|   |-- superstore_db.sql
|   `-- category_sales_query.sql
|-- Docs/
|   `-- Superstore_End_to_End_Data_Analytics_Project_Guide.pdf
|-- scripts/
|   |-- SuperStore_DA.ipynb
|   `-- load_processed_data_to_sql.py
`-- README.md
```

## Data Model

| Table | Type | Description | Primary Key |
|---|---|---|---|
| `dim_customer` | Dimension | Customer, segment, and location data | `customer_id` |
| `dim_product` | Dimension | Product name, category, and sub-category data | `product_id` |
| `dim_order` | Dimension | Order and shipping dates | `order_id` |
| `dim_date` | Dimension | Calendar values and date keys | `date_key` |
| `fact_sales` | Fact | Sales transactions, quantity, discount, and profit | `row_id` |

The fact table connects to the customer, product, and order dimensions through foreign keys.

## Dataset Size

- Sales fact records: 9,994
- Customers: 793
- Products: 1,862
- Orders: 5,009
- Date records: 1,434

## Exploratory Data Analysis

[SuperStore_DA.ipynb](/Users/naveenajakka/DA/scripts/SuperStore_DA.ipynb) performs the initial analysis and data transformation. Typical steps include:

- Loading and inspecting the raw Superstore CSV
- Checking data types and missing values
- Creating dimension and fact tables
- Exporting processed tables to CSV files
- Exploring sales and profit distributions

## Creating the SQLite Database

No external database server or third-party Python package is required.

From the project folder, run:

```bash
python3 scripts/load_processed_data_to_sql.py
```

The script:

1. Reads the five CSV files from `data/processed_data`
2. Creates [superstore.db](/Users/naveenajakka/DA/database/superstore.db)
3. Creates tables, primary keys, foreign keys, and indexes
4. Loads the processed data
5. Generates [superstore_db.sql](/Users/naveenajakka/DA/database/superstore_db.sql)

## Running SQL Queries

### VS Code

1. Install the SQLite extension by `alexcvzz`.
2. Open [superstore.db](/Users/naveenajakka/DA/database/superstore.db).
3. Open [category_sales_query.sql](/Users/naveenajakka/DA/database/category_sales_query.sql).
4. Use **SQLite: Run Query**, or right-click and choose the extension's query command.
5. Select an individual query before running it if the file contains multiple statements.

### Python

```bash
python3 - <<'PY'
import sqlite3
from pathlib import Path

query = Path("database/category_sales_query.sql").read_text()

with sqlite3.connect("database/superstore.db") as connection:
    for row in connection.execute(query):
        print(row)
PY
```

The SQLite database can also be opened with DB Browser for SQLite for a graphical query interface.

## Available Business Insights

[category_sales_query.sql](/Users/naveenajakka/DA/database/category_sales_query.sql) contains queries for:

- Category sales, profit, and profit margin
- Monthly sales trends
- Top 10 customers by sales
- Top 10 products by profit
- Products generating losses
- Customer segment performance
- Shipping mode performance
- The impact of discounts on sales and profit

## Example Query

```sql
SELECT
    p.category,
    ROUND(SUM(f.sales), 2) AS total_sales,
    ROUND(SUM(f.profit), 2) AS total_profit
FROM fact_sales AS f
INNER JOIN dim_product AS p
    ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;
```

## Power BI Connection

Power BI Desktop can connect to this SQLite database only when SQLite connectivity support is configured. CSV files can also be loaded directly into Power BI.

The recommended data model for Power BI is:

- `fact_sales`
- `dim_customer`
- `dim_product`
- `dim_order`
- `dim_date`

## Requirements

- Python 3
- Pandas and NumPy for notebook analysis
- Matplotlib and Seaborn for visualization
- Jupyter Notebook or VS Code with the Jupyter extension
- SQLite or a SQLite-compatible database tool

Install the Python packages with:

```bash
python3 -m pip install -r requirements.txt
```

## Future Improvements

- Add more exploratory visualizations
- Create a Power BI dashboard
- Add automated tests for database loading
- Add data-quality and missing-value checks
- Parameterize database and file paths
