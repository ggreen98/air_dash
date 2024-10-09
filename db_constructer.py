import pandas as pd  
from pathlib import Path  
import os

# List of species to search for in filenames
species_cat = ['voc', 'o3', 'pm', 'met', 'ch4', 'nox']
sites = ['LUR', 'LNM', 'TFS']  

species_cat = ['voc']
sites = ['LUR']  
data_path = '/Users/gabegreenberg/Boulder_AIR/CSV_Structer_Clone/data'

def file_grab(sites: list, species_cat: list, data_path: str):
    """
    Collects file paths grouped by site and species based on filenames.

    This function searches for files in a given directory for specific sites and species.
    The files are assumed to be non-recursively located within subdirectories named after
    the site. Filenames are expected to contain both the site and species names, and 
    matching files are collected into a dictionary.

    Args:
        sites (list): A list of site names (strings) representing directories to search within.
        species_cat (list): A list of species names (strings) to look for within the filenames.
        data_path (str): The root directory path where site-specific directories are located.

    Returns:
        dict: A dictionary where each key is a site name, and the value is another dictionary
              where keys are species names and values are lists of file paths that match
              the site and species in their filenames.

    Example:
        sites = ['LUR', 'LNM', 'TFS']
        species = ['voc', 'o3', 'pm', 'met', 'ch4', 'nox']
        data_path = '/Users/username/data'
        
        file_grab(sites, species, data_path)
        # Returns a dictionary grouping the files by site and species
    """
        
    # Initialize a dictionary to store the files grouped by site and species
    dir_dict = {}
    # Loop through each site (directory)
    for site in sites:
        species_dict = {}  # Dictionary to store files for each species at this site
        dir_dict[site] = species_dict  # Add this dictionary to the main dictionary
        # Loop through each species
        for ss in species_cat:
            file_lst = []  # Initialize an empty list to store the file paths for this species
            # Loop through all files in the directory (non-recursively)
            for file in Path(f'{data_path}/{site}').glob('*'):
                # Check if both the site and species are in the filename
                if site in str(file) and ss in str(file):
                    file_lst.append(str(file))  # Convert the PosixPath to a string and append it to the list
            # Store the list of file paths in the species dictionary
            species_dict[ss] = file_lst
    return dir_dict
            
dir_dict = file_grab(sites, species_cat, data_path)

for site in sites:
    for ss in species_cat:
        if len(dir_dict[site][ss]) != 0:
            fname_lst = []
            for file_path in dir_dict[site][ss]:
               directory, file_name = os.path.split(file_path)
               fname_lst.append(file_name)
            unique_names_dict = {fname[:-7] : [] for fname in fname_lst}
            correct_files_lst = []
            for fname in fname_lst:
                try:
                    unique_names_dict[fname[:-7]].append(float(fname[-7:-4]))
                except: # this will likeley need to be updated for finalized files with the f tag!!!
                    unique_names_dict[fname[:-7]].append(fname[-7:-4])
            for fname in unique_names_dict.keys():
                best_vnum = max(unique_names_dict[fname])
                correct_files_lst.append(f'{directory}/{fname}{str(best_vnum)}.csv')

            print(correct_files_lst) 
            print(len(correct_files_lst))
            # good_names_dict = {}
            # print(unique_names)
            # for fname in fname_lst:
            #     try:
            #         vnum = float(fname[-7:-4])
            #         if (fname not in good_names_lst) and 
            #     except: # this will likley be needed to handle finilized file logic
            #         print("version number could not be converted to a float")
            #         pass 
                #print(fname[-7:-4])
            # unique_names.split('_')
            # print(unique_names)


