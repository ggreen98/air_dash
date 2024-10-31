import mysql.connector

def create_tables():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='airbase'  # Add your database name here
    )
    
    cursor = connection.cursor()

    # Create a table for sites
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sites (
        site_id INT AUTO_INCREMENT PRIMARY KEY,
        site_name VARCHAR(255) UNIQUE NOT NULL
    )
    ''')

    # Create a table for species
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS species (
        species_id INT AUTO_INCREMENT PRIMARY KEY,
        species_name VARCHAR(255) UNIQUE NOT NULL
    )
    ''')

    # Create a table for data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        site_id INT,
        species_id INT,
        datetime DATETIME,
        value FLOAT,
        FOREIGN KEY (site_id) REFERENCES sites(site_id),
        FOREIGN KEY (species_id) REFERENCES species(species_id)
    )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    create_tables()
