import sqlite3
import os

db_path = os.path.join("database", "disaster.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()