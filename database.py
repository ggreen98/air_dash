import pandas as pd
import sqlite3
import os

print('here')

# Creating the database connection
db_path = 'air_database.db'
bairdb = sqlite3.connect(db_path)

cursor = bairdb.cursor()

# Create the 'sites' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sites (
        site_id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_name TEXT UNIQUE NOT NULL
    )
''')

# Create the 'species' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS species (
        species_id INTEGER PRIMARY KEY AUTOINCREMENT,
        species_name TEXT UNIQUE NOT NULL
    )
''')

# Create the 'data' table with foreign keys to 'sites' and 'species'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER,
        species_id INTEGER,
        datetime TEXT,
        value REAL,
        FOREIGN KEY (site_id) REFERENCES sites (site_id),
        FOREIGN KEY (species_id) REFERENCES species (species_id)
    )
''')

# Commit and close the connection
bairdb.commit()
bairdb.close()

print("Tables created successfully.")


