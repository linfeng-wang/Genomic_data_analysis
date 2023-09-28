
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
from tqdm import tqdm

#%% extract file names
# with open('tb-json_names.csv', 'w') as f:
#     subprocess.run("cd /mnt/storage7//jody/tb_ena/tbprofiler/latest/results/; ls", shell=True, stdout=f, text=True)

#! remove file name that ends with .txt in tb-json_names.csv - otherwise JSONDecodeError: Expecting value: line 2 column 1 (char 1)
#%%
NAME_FILE='tb-json_names.csv'
FOLDER_PATH = "/mnt/storage7//jody/tb_ena/tbprofiler/latest/results"
NAME_FILE='clinical_sample_name.txt'


#%% get the names of the samples - tb-json_names.csv
# with open(NAME_FILE, "r") as f:
#     json_names = []
#     for line in f:
#         data_line = line.rstrip().split('\n')
#         json_names.append(data_line[0])

# get the names of the samples - tb-json_names.csv
with open(NAME_FILE, "r") as f:
    json_names = []
    for line in f:
        data_line = line.rstrip().split('\n')
        name = data_line[0]+'.results.json'
        json_names.append(name)

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
mixed_infection_id = []
mixed_major_strain = {}
mixed_minor_strain = {}
mixed_infection_comb = []
mixed_infection_sub_comb = []
multi_infection = []


for x in tqdm(json_names):
    FILE_PATH = os.path.join(FOLDER_PATH, x)
    json_results = json.load(open(FILE_PATH))
    id = json_results['id']
    sublin = json_results["sublin"]
    comb = sublin
    sublin = sublin.split(';')
    if "" in sublin:
        sublin.remove("")
    if len(sublin) > 1:
        # print(sublin)
        # print("=======Mix infection!=======")
        if 'lineage4.3.2' in sublin or 'lineage4.3.2.1' in sublin:
            print(id)
            print(sublin)
        mixed_infection_sub_comb.append(sublin)
        minor_allele_freq.append(minorStrainFreq(json_results))
        mixed_infection_count += 1
        mixed_infection_sub.append(sublin[0])
        mixed_infection_sub.append(sublin[1])
        mixed_infection_id.append(id)
        mixed_infection_comb.append(comb)
        sublineages = {}
        for lin in json_results['lineage']:
            if lin['lin']== sublin[0] or lin['lin']== sublin[1]:
                sublineages[lin["lin"]] = lin["frac"]
        
        
        #     mixed_minor_strain[list(sublineages.keys())[1]] = list(sublineages.values())[1]
        if list(sublineages.values())[0] > list(sublineages.values())[1]:
            mixed_major_strain[id] = [list(sublineages.keys())[0], list(sublineages.values())[0]]
            mixed_minor_strain[id] = [list(sublineages.keys())[1], list(sublineages.values())[1]]
            
        else:            
            mixed_major_strain[id] = [list(sublineages.keys())[1], list(sublineages.values())[1]]
            mixed_minor_strain[id] = [list(sublineages.keys())[0], list(sublineages.values())[0]]
    elif len(sublin) > 2:
        multi_infection.append(f'{id}+{sublin}')
        
    if len(sublin) == 1:
        single_infection_sub.append(sublin[0])

    # sublineages.append(sublin[0])
#%%
for x in mixed_infection_sub_comb:
    if 'lineage4.3.2' in x or 'lineage4.3.2.1' in x:
        print(x)
    


#%%
sublin_MSI_df =pd.DataFrame()
sublin_MSI_df['id'] = mixed_major_strain.keys()
sublin_MSI_df['Major_sublin'] = mixed_major_strain.values()
sublin_MSI_df['Minor_sublin'] = mixed_minor_strain.values()
sublin_MSI_df.to_csv('sublin_MSI_df.csv')
#%%
if mixed_infection_count > 0:
    print("Mixed infection identified")
else:
    print("No mixed infection detected")

#%%
mixed_infection_comb_main = []
for x in mixed_infection_comb:
    mix = x.split(';')
    mix_out = []
    for x in mix:
        mix_out.append(x.split('.')[0])
    mix_out = ';'.join(mix_out)
    mixed_infection_comb_main.append(mix_out)
#%%
def top_count(input_list):
    rank = {}
    for x in np.unique(input_list):
        rank[x] = input_list.count(x)
    rank = dict(sorted(rank.items(), key=lambda item: item[1]))
    return rank

rank = top_count(mixed_infection_comb_main)

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

#adding a table - accession number - major strain name(sublineage name) - minor strain name(sublineage name)  - major frequency 
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
total_count = []
for x in sublin_count.keys():
    if x in single_sublin_count.keys():
        duplicate_list.append(x)

sublin_ratios = {}
for x in duplicate_list:
    # sublin_ratios[x] = sublin_count[x] / (single_sublin_count[x] +sublin_count[x])
    sublin_ratios[x] = []
    sublin_ratios[x].append(sublin_count[x] / (single_sublin_count[x] +sublin_count[x]))
    sublin_ratios[x].append(single_sublin_count[x] +sublin_count[x])
    
lin_count = dict(sorted(sublin_ratios.items(), key=lambda item: item[1], reverse=True))

lin_count = dict(itertools.islice(lin_count.items(), 20))

#%%
count_ = []
for x,y in zip(percent, total):
    count_.append(x*y)
    
    
percent = []
total = []
for k, v in lin_count.items():
    percent.append(v[0])
    total.append(v[1])


colors = {'A':'#1f77b4',
          'B':'firebrick'}

fig = go.Figure()
fig.add_trace(go.Bar(x = np.arange(1,len(lin_count),1), y = percent,  text=count_, textposition="outside"))
# sublin_ratios.keys()
# fig.update_traces(hoverinfo='label', textinfo='value', textfont_size=20,)
fig.add_trace(go.Bar(x = np.arange(1,len(lin_count),1), y = np.zeros([len(lin_count)])
,  text=total, textposition="outside", marker_color=colors['A'], textfont_color= 'white'))
# sublin_ratios.keys()
# fig.update_traces(hoverinfo='label', textinfo='value', textfont_size=20,)
# fig.update_layout(
#     xaxis = dict(
#         tickmode = 'array',
#         tickvals = np.arange(1,len(lin_count),1),
#         ticktext = tuple(lin_count.keys()),
#         tickangle=45,
#         tickfont = dict(size=12)
fig.update_yaxes(range=[0, 0.68])

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
    yaxis_title="Fraction involved in MSI",
    font=dict(
        family="Courier New, monospace",
        size=13,
        color="RebeccaPurple"
    ),
    barmode='overlay',
    showlegend=False
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
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)
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
