#%%
import json
from statistics import mean
from unittest import result

#%% test files
# json_file = '../strain_analysis/test_data/ERR6634978-ERR6635032-3070.results.json' #file used for targeting and error checking


#%%
#function that inputs get the lineage fraction info tb-profiler output json file
def tb_pred(json_file):
    sublin = {}
    json_results = json.load(open(json_file))
    for x in json_results['lineage']:
        lineage = x['lin'].split(".")[0]
#add lineage-frac to dictionary if the lineage don't exist, add it first
        if lineage in sublin.keys(): 
            sublin[lineage].append(x['frac'])
        else:
            sublin[lineage] = []
            sublin[lineage].append(x['frac'])

    for key, value in sublin.items():
        sublin[key] = mean(value)
    sublin = dict(sorted(sublin.items(), key=lambda item: item[1], reverse=True)) #get decending order so that we can know which is which corresponding to the model prediction
    contamination = len(sublin) > 2 #report that there is likely contamination

    return sublin, contamination

# result, contamination = tb_pred(json_file)
# #%%
# print(result)

# %%
#function that get the drug resistance info tb-profiler output json file

def tb_dr(json_file):
    dr_dict = {}
    json_results = json.load(open(json_file))
    for var in json_results['dr_variants']:
        drug_info = var["drugs"][0] #get the list inside the list
        dr_dict[var["freq"]] = drug_info["drug"]
    return dr_dict


