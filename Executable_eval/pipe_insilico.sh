#!/bin/bash
set -e
set -u
set -o pipefail

#this file is used to parallel run mix model pipeline
#local path: cd /mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable_eval

VCF='/mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk_new'
JSON='/mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk_new/tb-profiler/results'
PROCESSED='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable_eval'
PIPELINE='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable'

cd $JSON
ls | grep -E '.results.json$' | cut -f 1 -d "." > $PROCESSED/insilico_sample_name.txt

# activating enviroment
# echo "===activating ml-s7 enviroment==="
# eval "$(conda shell.bash hook)"
# conda activate ml-s7

cd $PROCESSED

#running parallel tb-profiler on bam files of samples
echo "***Running gmm model on sample files***"
#cat invitro_mix_name.csv | parallel --bar -j 50 "python $PIPELINE/main.py -vcf $VCF/{}.gatk.vcf.gz -json $JSON/{}.results.json" -g -o $PROCESSED/results/2mix_infection
cat insilico_sample_name.txt | parallel --bar -j 50 "python $PIPELINE/main.py -vcf $VCF/{}.vcf.gz -json $JSON/{}.results.json" -g -o $PROCESSED/results/insilico_mix_new



# python /mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable/main.py -vcf /mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk/ERR6634978-ERR6635032-3070.g.vcf.gz -json /mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk/freebayesVCF/results/ERR6634978-ERR6635032-3070.results.json