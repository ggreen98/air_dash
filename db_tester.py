import sqlite3

# Connect to the SQLite database
bairdb = sqlite3.connect('air_database.db')

# Create a cursor object to execute SQL commands
cursor = bairdb.cursor()

# Execute a query to fetch all data from the table
cursor.execute("SELECT pm10 FROM table1 LIMIT 10")

# Fetch all results from the executed query
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the cursor and database connection
cursor.close()
bairdb.close()
