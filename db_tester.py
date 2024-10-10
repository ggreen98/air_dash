# import sqlite3

# # Connect to the SQLite database
# bairdb = sqlite3.connect('air_database.db')

# # Create a cursor object to execute SQL commands
# cursor = bairdb.cursor()

# # Execute a query to fetch all data from the table
# cursor.execute("SELECT pm10 FROM table1 LIMIT 10")

# # Fetch all results from the executed query
# results = cursor.fetchall()

# # Print the results
# for row in results:
#     print(row)

# # Close the cursor and database connection
# cursor.close()
# bairdb.close()
# print('plz work working?')

import sqlite3

# Connect to your SQLite database
db_path = 'air_database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Check if specific tables exist
expected_tables = {'sites', 'species', 'data'}
existing_tables = {table[0] for table in tables}

if expected_tables.issubset(existing_tables):
    print("\nAll expected tables were created successfully.")
else:
    print("\nSome tables are missing:", expected_tables - existing_tables)

# Optionally, print the schema of each table
for table in expected_tables:
    cursor.execute(f"PRAGMA table_info({table});")
    schema = cursor.fetchall()
    print(f"\nSchema of {table} table:")
    for column in schema:
        print(column)

# Close the connection
conn.close()

