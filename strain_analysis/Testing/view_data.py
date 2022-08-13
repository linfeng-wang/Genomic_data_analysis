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

#%% extract file names
with open('tb-json_names.csv', 'w') as f:
    subprocess.run("cd /mnt/storage7/jody/tb_ena/tbprofiler/lineage/results; ls", shell=True, stdout=f, text=True)


#%%
NAME_FILE='tb-json_names.csv'
FOLDER_PATH = "/mnt/storage7/jody/tb_ena/tbprofiler/lineage/results"

#%%
with open(NAME_FILE, "r") as f:
    json_names = []
    for line in f:
        data_line = line.rstrip().split('\n')
        json_names.append(data_line[0])


# %%
sublineages = []
  
for x in json_names:
    FILE_PATH = os.path.join(FOLDER_PATH, x)
    json_results = json.load(open(FILE_PATH))
    sublin = json_results["sublin"]
    sublin = sublin.split(',')
    if len(sublin) > 1:
        print("=======Mix infection!=======")
    sublineages.append(sublin[0])

# %%
def uniq_lin(lin_):
    lin_unique = set(lin_)
    lin_count = {}
    for x in lin_unique:
        lin_count[x] = lin_.count(x)

    return lin_count, lin_unique

# %%
sublin_count, sublin_unique = uniq_lin(sublineages)
# print(sublin_count,sublin_unique)

#%%
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
labels = []
sizes = []
for x, y in mainlin_count.items():
    labels.append(x)
    sizes.append(y)

fig = go.Figure(data=[go.Pie(labels=labels,
                             values=sizes)])
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,)
fig.show()

# %%
