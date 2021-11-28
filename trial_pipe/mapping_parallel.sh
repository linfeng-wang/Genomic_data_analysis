# mappping&variant detection parallel file running script

BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
PIPELINE='pipelines/trial_pipe'

#indexing reference genome
eval "$(conda shell.bash hook)"
conda activate mapping

echo ***indexing reference genome***  -- performed only once, hence preventing indexing at different rate when using >1 threads
bwa index ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa #<-done only once, hence preventing indexing at different rate when using >1 threads

cd ~/$RAW

ls | grep -E '_1' | cut -f 1 -d "_" > sample_name.txt

eval "$(conda shell.bash hook)"
conda activate base

cd ~/$PIPELINE

cat ~/$RAW/sample_name.txt | parallel -j 5 "~/$PIPELINE/fast2matrix.sh {}"

