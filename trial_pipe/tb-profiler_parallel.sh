#!/bin/bash
set -e
set -u
set -o pipefail

#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe

RAW='/mnt/storage7/jody/tb_ena/per_sample'
PROCESSED='/mnt/storage7/lwang/trial_tb_philippines/data/processed/'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'

cd $RAW
ls | grep -E '.cram$' | cut -f 1 -d "." > $PROCESSED/tb_profiler/Sobkowiak_2018/sample_name.txt

##activating enviroment
# echo "===activating tb-profiler enviroment==="
# eval "$(conda shell.bash hook)"
# conda activate tb-profiler

# mkdir $PROCESSED/tb-profiler/mix
cd $PROCESSED/tb_profiler/Sobkowiak_2018

#running parallel tb-profiler on bam files of samples
echo "***Running tb-profiler on sample .bam files***"
cat $PROCESSED/tb_profiler/Sobkowiak_2018/sample_name.txt | parallel --bar -j 5 "tb-profiler profile -a $RAW/{}.bqsr.cram -p {}"

#Collating results files
echo "***Collating results files***"
tb-profiler collate


