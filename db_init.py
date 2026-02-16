import os
import psycopg2
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# Connect to the AWS RDS PostgreSQL database
try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    # Open a cursor to perform database operations
    cur = conn.cursor()

    print("Successfully connected to AWS RDS!")

    # Create the hardware_pricing table
    cur.execute("""
                CREATE TABLE IF NOT EXISTS hardware_pricing (
                                                                id SERIAL PRIMARY KEY,
                                                                component_name VARCHAR(255) UNIQUE NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    current_price DECIMAL(10, 2) NOT NULL
                    )
                """)
    print("Table 'hardware_pricing' checked/created.")

    # Insert some current, hardcoded market prices (Clear previous if any)
    cur.execute("TRUNCATE TABLE hardware_pricing RESTART IDENTITY;")

    hardware_data = [
        ('Ryzen 5 5600X', 'CPU', 135.00),
        ('Ryzen 7 7800X3D', 'CPU', 399.00),
        ('Core i7-13700K', 'CPU', 345.00),
        ('Core i5-12400F', 'CPU', 109.00),
        ('RTX 3070', 'GPU', 320.00),
        ('RTX 4090', 'GPU', 1999.00),
        ('RX 7800 XT', 'GPU', 510.00),
        ('RX 6700 XT', 'GPU', 330.00)
    ]

    # Execute the insert query
    insert_query = "INSERT INTO hardware_pricing (component_name, category, current_price) VALUES (%s, %s, %s)"
    cur.executemany(insert_query, hardware_data)

    # Commit the changes to the database
    conn.commit()
    print("Hardware pricing data successfully injected into the cloud database!")

    # Close communication with the database
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error connecting to the database: {e}")