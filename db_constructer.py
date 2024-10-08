import pandas as pd  # Import pandas for data manipulation
from pathlib import Path  # Import Path for working with file paths

# List of species to search for in filenames
species = ['voc', 'o3', 'pm', 'met', 'ch4', 'nox']

# List of sites to search in (directories within the data path)
# sites = ['LUR', 'TFS', 'LNM']
sites = ['LUR', 'LNM', 'TFS']  # Limiting the search to 'LUR' and 'LNM'

# The base directory where the CSV files are stored
data_path = '/Users/gabegreenberg/Boulder_AIR/CSV_Structer_Clone/data'

# Initialize a dictionary to store the files grouped by site and species
dir_dict = {}

# Loop through each site (directory)
for site in sites:
    species_dict = {}  # Dictionary to store files for each species at this site
    dir_dict[site] = species_dict  # Add this dictionary to the main dictionary
    
    # Loop through each species
    for ss in species:
        file_lst = []  # Initialize an empty list to store the file paths for this species
        
        # Loop through all files in the directory (non-recursively)
        for file in Path(f'{data_path}/{site}').glob('*'):
            # Check if both the site and species are in the filename
            if site in str(file) and ss in str(file):
                file_lst.append(str(file))  # Convert the PosixPath to a string and append it to the list
        
        # Store the list of file paths in the species dictionary
        species_dict[ss] = file_lst

        print(len(file_lst))


print(dir_dict)

            
