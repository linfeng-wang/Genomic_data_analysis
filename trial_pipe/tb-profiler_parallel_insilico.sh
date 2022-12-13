#!/bin/bash
set -e
set -u
set -o pipefail

#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe
echo start
RAW='/mnt/storage7/jody/tb_ena/per_sample'
PROCESSED='/mnt/storage7/lwang/trial_tb_philippines/data/seqtk_origin_json'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'

# cd $RAW
# ls | grep -E '.vcf.gz$' | cut -f 1 -d "." > $PROCESSED/sample_name.txt

##activating enviroment
# echo "===activating tb-profiler enviroment==="
# eval "$(conda shell.bash hook)"
# conda activate tb-profiler

# mkdir $PROCESSED/tb-profiler/mix
cd $PROCESSED

#running parallel tb-profiler on bam files of samples32
echo "***Running tb-profiler on sample files***"
# cat $PROCESSED/tb_profiler/Sobkowiak_2018/sample_name.txt | parallel --bar -j 5 "tb-profiler profile -a $RAW/{}.bqsr.cram -p {}"
cat $PROCESSED/sample_name.txt | parallel --bar -j 5 "tb-profiler profile -a $RAW/{}.bqsr.cram -p {}"
# cat $PROCESSED/sample_name.txt | parallel --bar -j 5 "tb-profiler profile --vcf $RAW/{}.vcf.gz -p {}"

#Collating results files
echo "***Collating results files***"
tb-profiler collate

# test
# tb-profiler profile -a /mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk/ERR6634978-ERR6635032-5050.mkdup.bam -p ERR6634978-ERR6635032-5050_new.json