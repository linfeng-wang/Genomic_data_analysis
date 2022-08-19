#%%
import argparse
import numpy as np
# import pathogenprofiler as pp
from sklearn.mixture import GaussianMixture
from sklearn.metrics import mean_squared_error, confusion_matrix, f1_score
# import fastq2matrix as fm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from scipy.stats import norm
import subprocess
from scipy.stats import kurtosis, skew
import re
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from icecream import ic
from uuid import uuid4
import sys

#%%
import tb_profiler 
import gmm_model

#%% testing
# json_file = '../strain_analysis/test_data/ERR6634978-ERR6635032-3070.results.json' #file used for targeting and error checking
# vcf_file = '../strain_analysis/test_data/ERR6634978-ERR6635032-3070.vcf.gz' #file used creating the model

#%%
parser = argparse.ArgumentParser(description='Mixed_infection_GMM',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-vcf", "--vcf", help='VCF file')
parser.add_argument("-json", "--json", help='tb-profiler output json file')
parser.add_argument("-g", "--graph", help='alternative snp frequency histogram', action='store_true')

args = parser.parse_args()

graph_option = args.graph
json_file = args.json
vcf_file = args.vcf

#%%
tb_pred_result, contamination = tb_profiler.tb_pred(json_file)
dr_dict = tb_profiler.tb_dr(json_file)

if contamination:
    sys.exit(f"Programme halted, there is a contamination! in {vcf_file}")

gmm_pred_result, model = gmm_model.model_pred(vcf_file, tail_cutoff = list(tb_pred_result.values())[1], graph = graph_option)

mse = gmm_model.mse_cal(tb_pred_result, gmm_pred_result)

#%%
strains = list(tb_pred_result.keys())
strains[0] = {}
strains[1] = {}
unknown = {}
for key, value in dr_dict.items(): #key is freqs value is dr
    prob = model.predict_proba(np.array(float(key)).reshape(-1,1))
    prob = prob[0] #the output from predict_proba is a list of a list
    if prob[0] > prob[1]:
        strains[0][value] = prob[0]
    elif prob[0] < prob[1]:
        strains[1][value] = prob[1]
    else:
        unknown[value] = prob

strains[0] = dict(sorted(strains[0].items(), key=lambda item: item[1], reverse=True))
strains[1] = dict(sorted(strains[1].items(), key=lambda item: item[1], reverse=True))

#%%
dr_output = {list(tb_pred_result.keys())[0]:strains[0],
            list(tb_pred_result.keys())[1]:strains[1]}

name = vcf_file.split('/')[-1].split('.vcf')[0]

output_file = "".join([name, ".mix.json"])

with open(output_file, 'w') as f:
    json.dump(dr_output, f, indent=2)

print("=======================================================================")
print(name)
print(dr_output)
print("=======================================================================")




# def tb_profiler_dr(json_file):
#     for var in json_results['dr_variants']:
#         cluster = assign_variant_to_distrib(gm, var['freq'], cutoff=0)
#         if cluster[0] == 0:
#             var['probs']= cluster
#             strain0.append(var)
#         elif cluster[0] == 1:
#             var['probs']= cluster
#             strain1.append(var)
#         else:
#             var['probs']= cluster[1:]
#             strainU.append(var)

#     strain_0 = [(v['drugs'][0]['drug']) for v in strain0]
#     strain_1 = [(v['drugs'][0]['drug']) for v in strain1]

# # %%
# def assign_variant_to_distrib(gm,freq,cutoff=0.95):
#     probs = gm.predict_proba([[freq]])
#     pred = gm.predict([[freq]])
#     if probs[0][pred][0]>cutoff: #put the prediction probability through cutoff threshold
#         return pred[0], probs[0][pred][0]
#     else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
#         return None, pred[0], probs[0][pred][0]






# %%
