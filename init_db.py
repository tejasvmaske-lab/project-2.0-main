import mysql.connector
from mysql.connector import Error
from datetime import datetime
# Database Configuration - Update these!
db_config = {
    'host': 'mysql-843df0b-tejas-894a.b.aivencloud.com',
    'user': 'avnadmin',
    'password': '', # <-- Update this
    'port': 23555
}

DB_NAME = 'inventory_management' # Your database name

def init_db():
    """Initialize the MySQL database with required tables"""
    try:
        # 1. Connect to MySQL Server (without DB first to create it)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # 2. Create Database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        print(f"✓ Database '{DB_NAME}' ready!")

        # 3. Create CATEGORY TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
        ''')
        
        # 4. Create PRODUCT TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sku VARCHAR(100) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                category_id INT,
                price DECIMAL(10, 2) NOT NULL,
                quantity INT NOT NULL DEFAULT 0,
                shelf_number VARCHAR(100),
                reorder_level INT NOT NULL DEFAULT 10,
                barcode_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES category_table(id) ON DELETE SET NULL
            ) ENGINE=InnoDB;
        ''')
        
        # 5. Create STOCK MOVEMENT TABLE
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movement (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_id INT NOT NULL,
                type VARCHAR(50) NOT NULL,
                quantity INT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES product_table(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        ''')

        conn.commit()
        print("✓ Tables created successfully!")

        # 6. Insert sample categories if empty
        cursor.execute("SELECT COUNT(*) FROM category_table")
        if cursor.fetchone()[0] == 0:
            sample_categories = [
                ('Electronics',),
                ('Furniture',),
                ('Office Supplies',),
                ('Tools',),
            ]
            # Use %s for MySQL placeholders instead of ?
            cursor.executemany(
                "INSERT INTO category_table (name) VALUES (%s)",
                sample_categories
            )
            conn.commit()
            print("✓ Sample categories added")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("✓ MySQL connection closed")

if __name__ == '__main__':
    init_db()