import pandas as pd
import os

#species = ['voc', 'o3', 'pm', 'met', 'ch4', 'nox']
species = ['voc']
#sites = ['LUR', 'TFS', 'LNM']
sites = ['LUR']
data_path = '/Users/gabegreenberg/Boulder_AIR/CSV_Structer_Clone/data'
paths_lst = []

for root, dirs, files in os.walk(data_path):
    site_dict = {}
    for site in sites:
        species_dict = {}  # Combine this outside the species loop
        for ss in species:
            file_path_lst = []
            for file in files:
                if file.endswith(".csv") and (site in file) and (ss in file):
                    file_path = os.path.join(root, file)
                    file_path_lst.append(file_path)
            if file_path_lst:  # Only add if the list is non-empty
                species_dict[ss] = file_path_lst
        if species_dict:  # Only add if species_dict has entries
            if site_dict.get(site) is None:  # Avoid duplicates by checking
                site_dict[site] = species_dict
                paths_lst.append(site_dict)

print(paths_lst)
print(len(paths_lst))

#print(file_lst)
            #file_path = os.path.join(root, file)  # Create the full file path


    # for file in files:
    #     if file.endswith(".csv"):
    #         for site in sites:
    #             for cat in categories:
    #                 if (site in root) & (cat in root):
    #                     print(root, file)


    # for file in files:
    #     if ".csv" in file:
    #         for site in sites_list:
    #             if site in file:
    #                 for cat in catigory:
    #                     if cat in file:
    #                         print(file)