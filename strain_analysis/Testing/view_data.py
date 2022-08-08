#this is to view the info and extract sublin info from the json file

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
    sublin = [i for i in sublin]
    if len(sublin) > 1:
        print("=======Mix infection!=======")
    sublineages.append(sublin)

# %%
sublineages_unique = set(sublineages)
sublin_count = {}
for x in sublineages_unique:
    sublin_count[x] = sublineages.count(x)

# %%
sublin_count
# %%
