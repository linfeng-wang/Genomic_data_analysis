#!/bin/bash
set -e
set -u
set -o pipefail

#this file is used to parallel run mix model pipeline
#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe

VCF='/mnt/storage7//jody/tb_ena/per_sample'
JSON='/mnt/storage7//jody/tb_ena/tbprofiler/latest/results/'
PROCESSED='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable_eval'
PIPELINE='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable'

cd $JSON
ls | grep -E '.results.json$' | cut -f 1 -d "." > $PROCESSED/sample_name.txt

##activating enviroment
# echo "===activating tb-profiler enviroment==="
# eval "$(conda shell.bash hook)"
# conda activate ml-s7

# mkdir $PROCESSED/tb-profiler/mix
cd $PROCESSED

#running parallel tb-profiler on bam files of samples
echo "***Running gmm model on sample files***"
cat sample_name.txt | parallel --bar -j 5 "python $PIPELINE/main.py -vcf $VCF/{}.g.vcf.gz -json $JSON/{}.results.json" -g -o $PROCESSED/results





