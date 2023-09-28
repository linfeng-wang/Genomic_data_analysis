#!/bin/bash
set -e
set -u
set -o pipefail

#this file is used to parallel run mix model pipeline
#local path: cd ~/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable_eval

VCF='/mnt/storage7/jody/tb_ena/per_sample'
JSON='/mnt/storage7/jody/tb_ena/tbprofiler/latest/results/'
PROCESSED='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable_eval'
PIPELINE='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable/gmm_model_tbp'

# cd $JSON
# ls | grep -E '.results.json$' | cut -f 1 -d "." > $PROCESSED/sample_name.txt

##activating enviroment
# echo "===activating tb-profiler enviroment==="
# eval "$(conda shell.bash hook)"
# conda activate ml-s7

# mkdir $PROCESSED/tb-profiler/mix
cd $PROCESSED

#running parallel tb-profiler on bam files of samples
echo "***Running gmm model on sample files***"
#cat invitro_mix_name.csv | parallel --bar -j 50 "python $PIPELINE/main.py -vcf $VCF/{}.gatk.vcf.gz -json $JSON/{}.results.json" -m -g -o $PROCESSED/results/2mix_infection
# cat three_mix.txt | parallel --bar -j 50 "python $PIPELINE/main_multi.py -vcf $VCF/{}.gatk.vcf.gz -json $JSON/{}.results.json" -m -g -o $PROCESSED/three_mixes
# cat extra_samples.txt | parallel --bar -j 20 "python $PIPELINE/main_multi.py -vcf $VCF/{}.gatk.vcf.gz" -g -m -o {} -op $PROCESSED/clinical_mix_multi_vcf_extra

# python /mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable/gmm_model_tbp/main_multi.py -vcf /mnt/storage7/jody/tb_ena/per_sample/DRR184902.gatk.vcf.gz -g -m -o DRR184902 -op /mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable_eval/test

python $PIPELINE/main_multi.py -vcf $VCF/ERR4796347.gatk.vcf.gz -g -m -o ERR4796347 -op $PROCESSED/clinical_mix_multi_vcf_test