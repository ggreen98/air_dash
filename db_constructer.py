import pandas as pd  
from pathlib import Path  
import os
import sqlite3

# List of species to search for in filenames
species_cat = ['voc', 'o3', 'pm', 'met', 'ch4', 'nox']
sites = ['LUR', 'LNM', 'TFS']  

species_cat = ['voc']
sites = ['LUR']  
data_path = '/Users/gabegreenberg/Boulder_AIR/CSV_Structer_Clone/data'

# def file_grab(sites: list, species_cat: list, data_path: str):
#     """
#     Collects file paths grouped by site and species based on filenames.

#     This function searches for files in a given directory for specific sites and species.
#     The files are assumed to be non-recursively located within subdirectories named after
#     the site. Filenames are expected to contain both the site and species names, and 
#     matching files are collected into a dictionary.

#     Args:
#         sites (list): A list of site names (strings) representing directories to search within.
#         species_cat (list): A list of species names (strings) to look for within the filenames.
#         data_path (str): The root directory path where site-specific directories are located.

#     Returns:
#         dict: A dictionary where each key is a site name, and the value is another dictionary
#               where keys are species names and values are lists of file paths that match
#               the site and species in their filenames.

#     Example:
#         sites = ['LUR', 'LNM', 'TFS']
#         species = ['voc', 'o3', 'pm', 'met', 'ch4', 'nox']
#         data_path = '/Users/username/data'
        
#         file_grab(sites, species, data_path)
#         # Returns a dictionary grouping the files by site and species
#     """
        
#     # Initialize a dictionary to store the files grouped by site and species
#     dir_dict = {}
#     # Loop through each site (directory)
#     for site in sites:
#         species_dict = {}  # Dictionary to store files for each species at this site
#         dir_dict[site] = species_dict  # Add this dictionary to the main dictionary
#         # Loop through each species
#         for ss in species_cat:
#             file_lst = []  # Initialize an empty list to store the file paths for this species
#             # Loop through all files in the directory (non-recursively)
#             for file in Path(f'{data_path}/{site}').glob('*'):
#                 # Check if both the site and species are in the filename
#                 if site in str(file) and ss in str(file):
#                     file_lst.append(str(file))  # Convert the PosixPath to a string and append it to the list
#             # Store the list of file paths in the species dictionary
#             species_dict[ss] = file_lst
#     return dir_dict
            
# dir_dict = file_grab(sites, species_cat, data_path)

# for site in sites:
#     for ss in species_cat:
#         if len(dir_dict[site][ss]) != 0:
#             fname_lst = []
#             for file_path in dir_dict[site][ss]:
#                directory, file_name = os.path.split(file_path)
#                fname_lst.append(file_name)
#             unique_names_dict = {fname[:-7] : [] for fname in fname_lst}
#             correct_files_lst = []
#             for fname in fname_lst:
#                 try:
#                     unique_names_dict[fname[:-7]].append(float(fname[-7:-4]))
#                 except: # this will likeley need to be updated for finalized files with the f tag!!!
#                     unique_names_dict[fname[:-7]].append(fname[-7:-4])
#             for fname in unique_names_dict.keys():
#                 best_vnum = max(unique_names_dict[fname])
#                 correct_files_lst.append(f'{directory}/{fname}{str(best_vnum)}.csv')

#             print(correct_files_lst) 
#             print(len(correct_files_lst))



class DataProcessor:
    def __init__(self, data_path: str, species_catigories: list[str], site: str):
        self.data_path = data_path
        self.species_catigories = species_catigories
        self.site = site
    
    def get_files(self):
        """
        Searches for files in the specified data path that match the current site and species categories.
        
        The method loops through the directory of the given site and collects files whose filenames contain
        the site and species name. The files are then grouped by species and stored in a dictionary.
        
        Returns:
            dict: A dictionary where keys are species categories and values are lists of file names.
        """
        
        species_files_dict = {}  # Initialize an empty dictionary to hold files for each species category
        
        # Loop through each species category (e.g., 'voc', 'o3', etc.)
        for cat in self.species_catigories:
            file_lst = []  # Initialize a list to store the file names for this species
            
            # Loop through all files in the site directory (non-recursively)
            for file in Path(f'{self.data_path}/{self.site}').glob('*'):
                # Check if both the site and species category are in the filename
                if self.site in str(file.name) and cat in str(file.name):
                    file_lst.append(str(file.name))  # Add the file name to the list
            
            # Store the list of file names under the species category
            species_files_dict[cat] = file_lst
        
        # Store the result as an instance attribute and return it
        self.species_files_dict = species_files_dict
        return species_files_dict
    
    def get_version_num(self): 
        """
        Identifies the highest version number of files for each species category
        based on their filenames.

        Note: Ensure `get_files` has been called to populate `self.species_files_dict`
        before calling this method.
        """
        if not hasattr(self, 'species_files_dict') or not self.species_files_dict:
            raise ValueError("You need to run `get_files` before calling `get_version_num`.")

        # Loop through each species category
        for cat in self.species_catigories:
            correct_files_lst = []
            unique_names_dict = {}

            # Process each file in the species category
            for fname in self.species_files_dict[cat]:
                base_name = fname[:-7]  # Remove the last 7 characters (assuming "_vX.X.csv" format)
                version_num = float(fname[-7:-4])  # Extract version number this may fail and need a new mothod for string version like finilized data "v_f"

                # Add version number to the corresponding base name in the dictionary
                if base_name not in unique_names_dict and any(q in base_name for q in ["q1", "q2", "q3", "q4"]):
                    unique_names_dict[base_name] = []
                try:
                    unique_names_dict[base_name].append(version_num)
                except:
                    pass

            # Find the highest version for each base name and construct the filename
            for base_name, versions in unique_names_dict.items():
                best_vnum = max(versions)
                correct_files_lst.append(f'{base_name}{best_vnum:.1f}.csv')

            # Update the species files dictionary with the highest version files
            self.species_files_dict[cat] = correct_files_lst
            return self.species_files_dict

    def db_data_readin_and_load(self):
         if not hasattr(self, 'species_files_dict') or not self.species_files_dict:
            raise ValueError("You need to run `get_files` before calling `get_version_num`.")
         
         # Open a database connection
         db_path = 'air_database.db'
         conn = sqlite3.connect(db_path)
         cursor = conn.cursor()


         for cat in self.species_files_dict:
            for fname in self.species_files_dict[cat]:
                df = pd.read_csv(rf'{self.data_path}/{self.site}/{fname}', header=1)
                df['time'] = pd.to_datetime(df['time'], unit='s')

               # Ensure that the site and species exist in the database
                cursor.execute('SELECT site_id FROM sites WHERE site_name = ?', (self.site,))
                site_id = cursor.fetchone()
                if not site_id:
                    cursor.execute('INSERT INTO sites (site_name) VALUES (?)', (self.site,))
                    site_id = cursor.lastrowid
                else:
                    site_id = site_id[0]
                  # Loop through each species column (excluding the 'time' column)
            for column in df.columns:
                if column == 'time':
                    continue  # Skip the time column
                
                # Ensure that the species exists in the database
                cursor.execute('SELECT species_id FROM species WHERE species_name = ?', (column,))
                species_id = cursor.fetchone()
                if not species_id:
                    cursor.execute('INSERT INTO species (species_name) VALUES (?)', (column,))
                    species_id = cursor.lastrowid
                else:
                    species_id = species_id[0]

                # Prepare batch insertions
                data_to_insert = []

                # Insert each row's data into the 'data' table
                  # Use itertuples() to iterate over the DataFrame
                for row in df.itertuples(index=False):
                    # Convert 'time' to string format for SQLite
                    datetime_str = getattr(row, 'time').strftime('%Y-%m-%d %H:%M:%S')
                    value = row[df.columns.get_loc(column)]
                    data_to_insert.append((site_id, species_id, datetime_str, value))

                # Batch insert data into the 'data' table using executemany()
                cursor.executemany('''
                    INSERT INTO data (site_id, species_id, datetime, value)
                    VALUES (?, ?, ?, ?)
                ''', data_to_insert)

         conn.commit()
         conn.close()

    
    # def prep_data_for_db(self):

test = DataProcessor(data_path, ['voc', 'pm'], 'LUR')
test.get_files()
test.db_data_readin_and_load()
    
    
    # def get_version_num(self):

    # def read_in_data(self):
    
    # def prep_data_for_db(self):

# class LURDataProcessor(DataProcessor):

    


