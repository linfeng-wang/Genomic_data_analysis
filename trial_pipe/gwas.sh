#BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
PIPELINE='pipelines/Genomic_data_analysis/trial_pipe'

#activating environment
eval "$(conda shell.bash hook)"
conda activate gwas


mkdir ~/$PROCESSED/plink
cd ~/$PROCESSED/plink

#generates plink file
echo 'generating plink file'
# bgzip ~/$PROCESSED/freebayesVCF/$1_q20.recode.vcf
plink --vcf ~/$PROCESSED/freebayesVCF/$1_q20.recode.vcf --make-bed --out $1 --allow-extra-chr
