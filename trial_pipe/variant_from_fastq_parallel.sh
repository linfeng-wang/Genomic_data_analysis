#!/bin/bash
set -e
set -u
set -o pipefail

#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe
echo start
RAW='/mnt/storage7/lwang/trial_tb_philippines/data/insilico_mix_mix'
PROCESSED='//mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk_new'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'

cd $RAW
ls | grep -E '.fastq.gz$' | cut -f 1 -d "_" > $PROCESSED/sample_name.txt

##activating enviroment
# echo "===activating tb-profiler enviroment==="
# eval "$(conda shell.bash hook)"
# conda activate tb-profiler

# mkdir $PROCESSED/tb-profiler/mix
cd $PROCESSED

#running parallel tb-profiler on bam files of samples
echo "***Running tb-profiler on sample .bam files***"
# cat $PROCESSED/tb_profiler/Sobkowiak_2018/sample_name.txt | parallel --bar -j 5 "tb-profiler profile -a $RAW/{}.bqsr.cram -p {}"
cat $PROCESSED/sample_name.txt | parallel --bar -j 5 "python $PIPELINE/variant_calling_from_fastq.py -1 $RAW/{}_1.fastq.gz -2 $RAW/{}_2.fastq.gz -r $REFGENOME -o {}"


python ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe/variant_calling_from_fastq.py -1 /mnt/storage7/lwang/trial_tb_philippines/data/insilico_mix_mix/ERR752118-ERR2864232-2080_1.fastq.gz -2 /mnt/storage7/lwang/trial_tb_philippines/data/insilico_mix_mix/ERR752118-ERR2864232-2080_2.fastq.gz -r ../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa -o testout