import csv
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = PROJECT_ROOT / "data" / "processed_data"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "superstore.db"
SQL_DUMP_PATH = DATABASE_DIR / "superstore_db.sql"


SCHEMA = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_order;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_customer (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT
);

CREATE TABLE dim_product (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT
);

CREATE TABLE dim_order (
    order_id TEXT PRIMARY KEY,
    order_date TEXT NOT NULL,
    ship_date TEXT NOT NULL,
    ship_mode TEXT
);

CREATE TABLE dim_date (
    date TEXT PRIMARY KEY,
    date_key INTEGER UNIQUE NOT NULL,
    year INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter TEXT,
    day INTEGER
);

CREATE TABLE fact_sales (
    row_id INTEGER PRIMARY KEY,
    order_id TEXT NOT NULL,
    order_date TEXT,
    ship_date TEXT,
    ship_mode TEXT,
    product_id TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    sales REAL NOT NULL,
    quantity INTEGER NOT NULL,
    discount REAL NOT NULL,
    profit REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES dim_order(order_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

CREATE INDEX idx_fact_sales_order ON fact_sales(order_id);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_id);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_id);
"""


def read_csv(file_name):
    with (CSV_DIR / file_name).open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def load_data(connection):
    customer_rows = read_csv("dim_customer.csv")
    connection.executemany(
        """
        INSERT INTO dim_customer
        (customer_id, customer_name, segment, country, city, state, postal_code)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                row["Customer ID"],
                row["Customer Name"],
                row["Segment"],
                row["Country"],
                row["City"],
                row["State"],
                str(row["Postal Code"]),
            )
            for row in customer_rows
        ],
    )

    product_rows = read_csv("dim_product.csv")
    connection.executemany(
        """
        INSERT INTO dim_product
        (product_id, product_name, category, sub_category)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                row["Product ID"],
                row["Product Name"],
                row["Category"],
                row["Sub-Category"],
            )
            for row in product_rows
        ],
    )

    order_rows = read_csv("dim_order.csv")
    connection.executemany(
        """
        INSERT INTO dim_order (order_id, order_date, ship_date, ship_mode)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                row["Order ID"],
                row["Order Date"],
                row["Ship Date"],
                row["Ship Mode"],
            )
            for row in order_rows
        ],
    )

    date_rows = read_csv("dim_date.csv")
    connection.executemany(
        """
        INSERT INTO dim_date
        (date, date_key, year, month, month_name, quarter, day)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                row["Date"],
                int(row["Date_Key"]),
                int(row["Year"]),
                int(row["Month"]),
                row["Month_Name"],
                row["Quarter"],
                int(row["Day"]),
            )
            for row in date_rows
        ],
    )

    sales_rows = read_csv("fact_sales.csv")
    connection.executemany(
        """
        INSERT INTO fact_sales
        (row_id, order_id, order_date, ship_date, ship_mode, product_id,
         customer_id, sales, quantity, discount, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                int(row["Row_ID"]),
                row["Order_ID"],
                row["Order_Date"],
                row["Ship_Date"],
                row["Ship_Mode"],
                row["Product_ID"],
                row["Customer_ID"],
                float(row["Sales"]),
                int(row["Quantity"]),
                float(row["Discount"]),
                float(row["Profit"]),
            )
            for row in sales_rows
        ],
    )


def export_sql_dump(connection):
    with SQL_DUMP_PATH.open("w", encoding="utf-8") as sql_file:
        for statement in connection.iterdump():
            sql_file.write(statement + ";\n")


def main():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.executescript(SCHEMA)
        load_data(connection)
        connection.commit()
        export_sql_dump(connection)

        print("Database:", DATABASE_PATH)
        print("SQL dump:", SQL_DUMP_PATH)
        for table in (
            "dim_customer",
            "dim_product",
            "dim_order",
            "dim_date",
            "fact_sales",
        ):
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            print(f"{table}: {count} rows")


if __name__ == "__main__":
    main()
