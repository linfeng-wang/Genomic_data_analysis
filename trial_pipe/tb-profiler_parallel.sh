#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe


RAW='../../../data/raw_fastq'
PROCESSED='../../../data/processed'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'

##activating enviroment
echo "===activating tb-profiler enviroment==="
eval "$(conda shell.bash hook)"
conda activate tb-profiler

mkdir $PROCESSED/pool_f4m/tb-profiler
cd $PROCESSED/pool_f4m/tb-profiler

#running parallel tb-profiler on bam files of samples
echo "***Running tb-profiler on sample .bam files***"
cat $RAW/sample_name.txt | parallel --bar -j 5 "tb-profiler profile -a $PROCESSED/pool_f4m/{}.mkdup.bam -p {}"

#Collating results files
echo "***Collating results files***"
tb-profiler collate


