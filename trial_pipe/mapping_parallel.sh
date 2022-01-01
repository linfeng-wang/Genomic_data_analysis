# mappping&variant detection parallel file running script
#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe


RAW='../../../data/raw_fastq'
PROCESSED='../../../data/processed'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'



#activating environment
eval "$(conda shell.bash hook)"
conda activate mapping

#indexing reference genome
echo "***indexing reference genome***"  #-- performed only once, hence preventing indexing at different rate when using >1 threads
bwa index $REFGENOME #<-done only once, hence preventing indexing at different rate when using >1 threads

cd $RAW

ls | grep -E '_1' | cut -f 1 -d "_" > sample_name.txt

eval "$(conda shell.bash hook)"
conda activate base

cd ~/$PIPELINE

cat $RAW/sample_name.txt | parallel -j 5 "$PIPELINE/mapping.sh {}"

