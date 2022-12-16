#%%
from re import sub
from icecream import ic
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import re
import os
import json
import subprocess
import itertools
from multiprocessing import Pool

#%%
#load the corresponding lineage sample files names and mixture ratio
lin1 = ['ERR752118', 'ERR752118',  'ERR752118', 'ERR2864235', 'ERR2864235', 'ERR038260', 'ERR751848', 'ERR751848', 'ERR751848', 'ERR2864244', 'ERR2864244', 'ERR038260',
'ERR2864288', 'ERR2864232', 'ERR2864235', 'ERR2864232', 'ERR2864288', 'ERR2864288', 'ERR2864237', 'ERR038260', 'ERR2864244', 'ERR038260', 'ERR2864237', 'ERR2864237',
]

lin2 = ['ERR2864288', 'ERR2864232', 'ERR2864235', 'ERR2864232', 'ERR2864288', 'ERR2864288', 'ERR2864237', 'ERR038260', 'ERR2864244', 'ERR038260', 'ERR2864237', 'ERR2864237',
'ERR752118', 'ERR752118',  'ERR752118', 'ERR2864235', 'ERR2864235', 'ERR038260', 'ERR751848', 'ERR751848', 'ERR751848', 'ERR2864244', 'ERR2864244', 'ERR038260',

]

ratio1 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
ratio2 = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50]

#%%
def running(l1, l2):
    ratio1 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    ratio2 = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50]
    for r1, r2 in zip(ratio1, ratio2):
    # subprocess.call("./seqtk_new.sh {r1} {r2} {l1} {l2}".format(r1=r1, r2=r2, l1=l1, l2=l2, shell=True))
        subprocess.call("./seqtk_new.sh %s %s %s %s" % (r1, r2, l1, l2), shell=True)        

# %%
#running the mixture generation script script iteratively
subprocess.run('cd /mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/strain_analysis/Artificial_mixture_creation', shell=True)

with Pool(10) as pool:
    M = pool.starmap(running, zip(lin1, lin2))
    
#%%
