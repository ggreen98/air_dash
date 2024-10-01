import pandas as pd
import os

species = ['voc', 'o3', 'pm', 'met', 'ch4', 'nox']
species = ['voc']
#sites = ['LUR', 'TFS', 'LNM']
sites = ['LUR']
data_path = '/Users/gabegreenberg/Boulder_AIR/CSV_Structer_Clone/data'
num = 0
file_lst = []
for root, dirs, files in os.walk(data_path):
    for file in files:
        if file.endswith(".csv"):  # Check if the file is a CSV
            for site in sites:
                site_dict = {}
                for ss in species:
                    species_dict = {}
                    file_path_lst = []
                    if (site in file) & (ss in file) & ('diagnostic' not in root):
                        file_path = os.path.join(root, file)
                        file_path_lst.append(file_path)
                if len(file_path_lst) > 0:
                    species_dict[ss] = file_path_lst
            site_dict[site] = species_dict
            file_lst.append(site_dict)
    

print(file_lst)
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