from database import get_connection


def seed_data():
    connection = get_connection()
    cursor = connection.cursor()

    # Insert products
    cursor.execute("""
        INSERT INTO products (id, name, category)
        VALUES
            (1, 'Laptop', 'Electronics'),
            (2, 'Mouse', 'Electronics')
        ON CONFLICT (id) DO NOTHING;
    """)

    # Insert sales
    sales = [
        (2, "2026-08-16", 22),
        (2, "2026-08-17", 24),
        (2, "2026-08-18", 27),
        (2, "2026-08-19", 26),
        (2, "2026-08-20", 25),
        (2, "2026-08-21", 30),
        (2, "2026-08-22", 28),
    ]

    cursor.executemany("""
        INSERT INTO sales (product_id, date, quantity_sold)
        VALUES (%s, %s, %s);
    """, sales)

    connection.commit()

    cursor.close()
    connection.close()

    print("Data inserted successfully!")


if __name__ == "__main__":
    seed_data()
