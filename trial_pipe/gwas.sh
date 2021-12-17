#local path: cd ~/trial_tb_philippines/trial pipelines/Genomic_data_analysis/trial_pipe


#BASE='data/trial'
RAW='../../../data/raw_fastq'
PROCESSED='../../../data/processed'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/trial pipelines/Genomic_data_analysis/trial_pipe'


#activating environment
eval "$(conda shell.bash hook)"
conda activate gwas


mkdir $PROCESSED/plink
cd $PROCESSED/plink

#generates plink file
echo 'generating plink file'
# bgzip $PROCESSED/freebayesVCF/$1_q20.recode.vcf
plink --vcf $PROCESSED/freebayesVCF/$1_q20.recode.vcf --make-bed --out $1 --allow-extra-chr
