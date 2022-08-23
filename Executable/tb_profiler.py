#%%
import json
from statistics import mean
from unittest import result

#%% test files
# json_file = '../strain_analysis/test_data/ERR6634978-ERR6635032-3070.results.json' #file used for targeting and error checking


#%%
#function that inputs get the lineage fraction info tb-profiler output json file
def tb_pred(json_file):
    failed = 0
    sublin = {}
    json_results = json.load(open(json_file))
    sublin = json_results["sublin"]
    sublin = sublin.split(';')
    if len(sublin) == 2 and sublin[-1] != '':
        sublin_dict = {}
        for x in json_results['lineage']:
            if x['lin'] == sublin[0] or x['lin'] == sublin[1]:
                lineage = x['lin']
    #add lineage-frac to dictionary if the lineage don't exist, add it first
                sublin_dict[lineage] = x['frac']

        sublin_dict = dict(sorted(sublin_dict.items(), key=lambda item: item[1], reverse=True)) #get decending order so that we can know which is which corresponding to the model prediction
    
    elif len(sublin) > 2:
        failed = 1 #report that there is likely contamination or single strain infection
        sublin_dict = {}
    else:
        failed = 2
        sublin_dict = {}

    return sublin_dict, failed

# result, failed = tb_pred(json_file)
# # #%%
# print(result, failed)

# %%
#function that get the drug resistance info tb-profiler output json file

def tb_dr(json_file):
    dr_dict = {}
    json_results = json.load(open(json_file))
    for var in json_results['dr_variants']:
        drug_info = var["drugs"][0] #get the list inside the list
        dr_dict[var["freq"]] = drug_info["drug"]
    return dr_dict


