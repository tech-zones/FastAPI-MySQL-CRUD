from fastapi import FastAPI, HTTPException
from database import get_db, create_table
import mysql.connector

app = FastAPI()

# Create table on startup
create_table()

@app.post("/items/")
def create_item(name: str, description: str = None):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO items (name, description) VALUES (%s, %s)",
        (name, description)
    )
    db.commit()
    item_id = cursor.lastrowid
    cursor.close()
    db.close()
    return {"id": item_id, "name": name, "description": description}

@app.get("/items/")
def read_items():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return {"items": items}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    db.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, description: str = None):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE items SET name = %s, description = %s WHERE id = %s",
        (name, description, item_id)
    db.commit()
    affected = cursor.rowcount
    cursor.close()
    db.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated"}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    db.commit()
    affected = cursor.rowcount
    cursor.close()
    db.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}