#this is to view the info and extract sublin info from the json file 
#created - 08.08.2022
#%%
from icecream import ic
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import os
import json
import subprocess
import itertools

#%% extract file names
with open('tb-json_names.csv', 'w') as f:
    subprocess.run("cd /mnt/storage7//jody/tb_ena/tbprofiler/latest/results/; ls", shell=True, stdout=f, text=True)


#%%
NAME_FILE='tb-json_names.csv'
FOLDER_PATH = "/mnt/storage7//jody/tb_ena/tbprofiler/latest/results"

#%% get the names of the samples
with open(NAME_FILE, "r") as f:
    json_names = []
    for line in f:
        data_line = line.rstrip().split('\n')
        json_names.append(data_line[0])


# %%
sublineages = []
mixed_infection = []
mixed_infection_count = 0
for x in json_names:
    FILE_PATH = os.path.join(FOLDER_PATH, x)
    json_results = json.load(open(FILE_PATH))
    sublin = json_results["sublin"]
    sublin = sublin.split(';')
    if len(sublin) > 1:
        # print("=======Mix infection!=======")
        mixed_infection_count += 1
        mixed_infection.append(sublin)
        sublineages.append(sublin[0])
        sublineages.append(sublin[1])

    sublineages.append(sublin[0])

if mixed_infection_count > 0:
    print("Mixed infection identified")
else:
    print("No mixed infection detected")


#%%
mixed_infection_count


#%% creating flat list so that number of each sublineage can be counted
mixed_infection
flat_mixed_infection = [item for sublist in mixed_infection for item in sublist]

# %%
def uniq_lin(lin_):
    lin_unique = set(lin_)
    lin_count = {}
    for x in lin_unique:
        lin_count[x] = lin_.count(x)

    return lin_count, lin_unique

#%%
sublin_count, sublin_unique = uniq_lin(flat_mixed_infection)
# print(sublin_count,sublin_unique)

#%%
print(sublin_count)

#%% main_lineage count
mix_infect = 0
main_lineages = []
for x in json_names:
    FILE_PATH = os.path.join(FOLDER_PATH, x)
    json_results = json.load(open(FILE_PATH))
    mainlin = json_results["main_lin"]
    mainlin = mainlin.split(',')
    if len(mainlin) > 1:
        print("=======Mix infection!=======")
        mix_infect = 1
    main_lineages.append(mainlin[0])

print("mix_infect:",mix_infect)


# %%
mainlin_count, mainlin_unique = uniq_lin(main_lineages)
print(mainlin_count)

# %%
def piechart(lin_count, highest=True):
    if highest:
        lin_count = dict(sorted(lin_count.items(), key=lambda item: item[1], reverse=True))
        lin_count = dict(itertools.islice(lin_count.items(),10))

    labels = []
    sizes = []
    for x, y in lin_count.items():
        labels.append(x)
        sizes.append(y)

    fig = go.Figure(data=[go.Pie(labels=labels,
                                values=sizes)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,)
    fig.show()

# %%
piechart(sublin_count)

# %% sublineages that are most prevalently involved in sublineages
sort_sublin_count = dict(sorted(sublin_count.items(), key=lambda item: item[1], reverse=True))

#%%
sort_sublin_count[:5]
# %%
first_two_items = dict(itertools.islice(sort_sublin_count.items(),2))

# %%
first_two_items
# %%
