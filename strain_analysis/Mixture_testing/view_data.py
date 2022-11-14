#this is to view the info and extract sublin info from the json file 
#created - 08.08.2022
#%%
from re import sub
from unittest import result
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
from statistics import mean

#%% extract file names
with open('tb-json_names.csv', 'w') as f:
    subprocess.run("cd /mnt/storage7//jody/tb_ena/tbprofiler/latest/results/; ls", shell=True, stdout=f, text=True)

#! remove file name that ends with .txt
#%%
NAME_FILE='tb-json_names.csv'
FOLDER_PATH = "/mnt/storage7//jody/tb_ena/tbprofiler/latest/results"

#%% get the names of the samples
with open(NAME_FILE, "r") as f:
    json_names = []
    for line in f:
        data_line = line.rstrip().split('\n')
        json_names.append(data_line[0])


#%%
def minorStrainFreq(json_results):
    sublin_dict = {}
    for x in json_results['lineage']:
        if x['lin'] == sublin[0] or x['lin'] == sublin[1]:
            lineage = x['lin']
    #add lineage-frac to dictionary if the lineage don't exist, add it first
            sublin_dict[lineage] = x['frac']
    # contamination = len(sublin) > 2 #report that there is likely contamination
    return min(sublin_dict.values())

# %% sublineage mixinfection data import from json files (tb-p output)
# sublineages = []
mixed_infection_sub = []
single_infection_sub = []
mixed_infection_count = 0
minor_allele_freq = []
#%%
for x in json_names:
    FILE_PATH = os.path.join(FOLDER_PATH, x)
    json_results = json.load(open(FILE_PATH))
    sublin = json_results["sublin"]
    sublin = sublin.split(';')
    if "" in sublin:
        sublin.remove("")
    if len(sublin) > 1:
        print(sublin)
        # print("=======Mix infection!=======")
        minor_allele_freq.append(minorStrainFreq(json_results))
        mixed_infection_count += 1
        mixed_infection_sub.append(sublin[0])
        mixed_infection_sub.append(sublin[1])

    if len(sublin) == 1:
        single_infection_sub.append(sublin[0])

    # sublineages.append(sublin[0])
#%%
if mixed_infection_count > 0:
    print("Mixed infection identified")
else:
    print("No mixed infection detected")


# %%
def uniq_lin(lin_):
    lin_unique = set(lin_)
    lin_count = {}
    for x in lin_unique:
        lin_count[x] = lin_.count(x)

    return lin_count, lin_unique

#%%
import plotly.express as px

fig = px.histogram(minor_allele_freq)

fig.update_layout(bargap=0.2)
fig.update_layout(
title="Histogram of Minor Allele Frequency of mixed-infectinon sample",
    xaxis_title="Minor Allel Frequency",
    yaxis_title="Sample Count"
)

fig.show()
#%%

len(minor_allele_freq)
len(json_names)

# %% mainlineage mixinfection data import from json files (tb-p output)
# mix_infect = 0
# mixed_infection_main =[]
# main_lineages = []
# minor_allele_freq = []

# for x in json_names:
#     FILE_PATH = os.path.join(FOLDER_PATH, x)
#     json_results = json.load(open(FILE_PATH))
#     minor_allele_freq.append(minorStrainFreq(json_results))
#     mainlin = json_results["main_lin"]
#     mainlin = mainlin.split(';')
#     if len(mainlin) > 1 and mainlin[-1] != '':
#         print("=======Mix infection!=======")
#         mix_infect = 1
#         mixed_infection_main.append(mainlin)
#     main_lineages.append(mainlin)

# print("mix_infect:",mix_infect)


#%% 
sublin_count, sublin_unique = uniq_lin(mixed_infection_sub)
single_sublin_count, single_sublin_unique = uniq_lin(single_infection_sub)

#%%
duplicate_list = []

for x in sublin_count.keys():
    if x in single_sublin_count.keys():
        duplicate_list.append(x)

sublin_ratios = {}
for x in duplicate_list:
    sublin_ratios[x] = sublin_count[x] / (single_sublin_count[x] +sublin_count[x])

lin_count = dict(sorted(sublin_ratios.items(), key=lambda item: item[1], reverse=True))

lin_count = dict(itertools.islice(lin_count.items(), 20))




#%%
fig = go.Figure()
fig.add_trace(go.Bar(x = np.arange(1,len(lin_count),1), y = list(lin_count.values())))
# sublin_ratios.keys()
# fig.update_traces(hoverinfo='label', textinfo='value', textfont_size=20,)
fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = np.arange(1,len(lin_count),1),
        ticktext = tuple(lin_count.keys()),
        tickangle=45,
        tickfont = dict(size=12)
    ),
    yaxis = dict(titlefont = dict(size = 5)),
    title="Ratio of Sublineage involved in mixed infection",
    xaxis_title="Sublineages",
    yaxis_title="Proportion involved in mixed infection",
    font=dict(
        family="Courier New, monospace",
        size=13,
        color="RebeccaPurple"
    )
)
fig.show()


# %%
def piechart(lin_count, highest=True):
    total = sum(lin_count.values())
    if highest:
        lin_count = dict(sorted(lin_count.items(), key=lambda item: item[1], reverse=True))
        rest_count = list(lin_count.values())[10:-1]
        lin_count = dict(itertools.islice(lin_count.items(),10))
        lin_count["Rest"] = sum(rest_count)

    labels = []
    sizes = []
    for x, y in lin_count.items():
        labels.append(x)
        sizes.append(y/total)
    # print(lin_count)

    fig = go.Figure(data=[go.Pie(labels=labels,
                                values=sizes)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,)
    fig.show()

# %%
piechart(sublin_count)

# %%
# piechart(mainlin_count)
# %%
def minorStrainHist(lin_count, highest=True):
    total = sum(lin_count.values())
    if highest:
        lin_count = dict(sorted(lin_count.items(), key=lambda item: item[1], reverse=True))
        rest_count = list(lin_count.values())[10:-1]
        lin_count = dict(itertools.islice(lin_count.items(),10))
        lin_count["Rest"] = sum(rest_count)

    labels = []
    sizes = []
    for x, y in lin_count.items():
        labels.append(x)
        sizes.append(y/total)
    # print(lin_count)

    fig = go.Figure(data=[go.Pie(labels=labels,
                                values=sizes)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,)
    fig.show()


#%%
minorStrainHist(lin_count)

# %%
def minorAFreq_graph(freqs):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x = freqs))

    fig.update_layout(
        title="Alternative allele GMM distribution",
        xaxis_title="Alternative SNP freqency",
        yaxis_title="Count",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    fig.show()
# %%
minorAFreq_graph(minor_allele_freq)# %%

# %%
