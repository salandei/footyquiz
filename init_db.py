import sqlite3

connection = sqlite3.connect('database.db')

print("Initializing db...")
with open('db_schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
print("DONE!")