#freebayes bam->vcf conversion parallel file running script

BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
PIPELINE='pipelines/Genomic_data_analysis/trial_pipe'

#reference file
REFGENOME='refgenome/MTB-h37rv_asm19595v2-eg18.fa'

#activating variant_detection enviroment
echo 'activating variant_detection enviroment'
eval "$(conda shell.bash hook)"
conda activate variant_detection 

mkdir ~/$PROCESSED/freebayesVCF
cd ~/$PROCESSED/freebayesVCF


cat ~/$RAW/sample_name.txt | parallel -j 5 "~/$PIPELINE/freebayes.sh {}"