import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="fastapi_simple"
    )

def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT
        )
    """)
    db.commit()
    cursor.close()
    db.close()