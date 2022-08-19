#%%
import argparse
from ntpath import join
import uuid
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
# from scipy.stats import kurtodsdsis, skew
import re
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
# from cb91visuals import *
import gc
import pipe
from icecream import ic
from uuid import uuid4

#%%
#this model outputs the strain info depending if one value is still larger than the threshold after substracting the other prob value from it - not as good as not using it

#%%
# vcf_file = '../strain_analysis/test_data/ERR6634978-ERR6635032-3070.vcf.gz' #file used creating the model

#%%
#final model
def model_pred(vcf_file, tail_cutoff=0, graph = False):
    uuid_ = uuid4() #create random naming so that the script can be run in parallel
    uuid_file = "".join([str(uuid_), ".csv"])

    with open(uuid_file, 'w') as f:
        subprocess.run("bcftools view -c 1 -m2 -M2 -T ^new_exclusion.bed %s | bcftools query -f '%%POS\\t%%REF\\t%%ALT[\\t%%GT\\t%%AD\\n]'" % vcf_file, shell=True, stdout=f, text=True)
    pos = []
    freqs = []
    scatter = []
    with open(uuid_file, 'r') as f:
        for line in f: #get the relevant info including position, alt/ref snp count info
            row = line.strip().split()
            ads = [int(x) for x in row[4].split(",")]
            afs = [x/sum(ads) for x in ads]
            if afs[1]>1-tail_cutoff or afs[1]<tail_cutoff: #apply cut off value
                continue
            pos.append(int(row[0]))
            freqs.append([afs[1]])
            scatter.append(ads)

        # freqs = [[0.7],[0.6],[0.4]]    
        gm = GaussianMixture(n_components=2, random_state=0).fit(np.array(freqs).reshape(-1, 1))
        mu0 = gm.means_[1][0]
        mu1 = gm.means_[0][0]
        
        scatter = np.array(scatter)
        
        labels = gm.predict(freqs)
        mu0_ = len(labels[labels==0])/len(labels)
        mu1_ = len(labels[labels==1])/len(labels)
        
        prediction_prob = gm.predict_proba(freqs)
        
        
        anchored_array = np.concatenate((scatter, labels.reshape(-1,1)), axis=1) 
        lin1_ = anchored_array[anchored_array[:,2]==1]
        lin4_ = anchored_array[anchored_array[:,2]==0]

    if graph:
        flat_freqs = list(np.concatenate(freqs))
        plt.hist(flat_freqs)
        plt.title("Alternative allele GMM distribution")
        plt. xlabel("Alternative SNP freqency")
        plt. ylabel("Count")

        plt.imshow()

        # flat_freqs = list(np.concatenate(freqs))
        # fig = go.Figure()
        # fig.add_trace(go.Histogram(x = flat_freqs))
    
        # fig.update_layout(
        #     title="Alternative allele GMM distribution",
        #     xaxis_title="Alternative SNP freqency",
        #     yaxis_title="Count",
        #     font=dict(
        #         family="Courier New, monospace",
        #         size=18,
        #         color="RebeccaPurple"
        #     )
        # )
        # fig.show()

    # os.remove(os.path.join("/__pycache__", uuid_file))
    os.remove(uuid_file)

    if mu0 > mu1:
        return [mu0, mu1], gm #make sure the descending order corresponds to the output of tb_profiler.tb_pred()
    else:
        return [mu1, mu0], gm


# %%
def mse_cal(tb_prof, gmm_result):
    return mean_squared_error(list(tb_prof.values()), gmm_result)