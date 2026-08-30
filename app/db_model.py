from database import get_connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            date DATE NOT NULL,
            quantity_sold INTEGER NOT NULL
        );
    """)

    connection.commit()

    cursor.close()
    connection.close()

    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()
