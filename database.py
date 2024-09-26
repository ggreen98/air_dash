import pandas as pd
import sqlite3
import os


in_dir = '/Users/gabegreenberg/Boulder_AIR/BoulderAIR_data/ECC/pm'
df_lst = []
for file in os.listdir('/Users/gabegreenberg/Boulder_AIR/BoulderAIR_data/ECC/pm'):
    df = pd.read_csv(rf'{in_dir}/{file}', header=1)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df_lst.append(df)
    
data = pd.concat(df_lst)
data = data.sort_values('time')
print(data)

# Creating the database connection
airdb = sqlite3.connect('air_database.db')

# Write dataframes to the SQLite database
data.to_sql('table1', airdb, if_exists='replace', index=False)
print('here')