#freebayes bam to vcf conversion
#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe

RAW='../../../data/raw_fastq'
PROCESSED='../../../data/processed'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'


#activating variant_detection enviroment
echo 'activating variant_detection enviroment'
eval "$(conda shell.bash hook)"
conda activate variant_detection 

mkdir $PROCESSED/freebayesVCF
cd $PROCESSED/freebayesVCF

#Converting bam to vcf file
echo 'converting .bam to .vcf for sample' $1 
freebayes -f $REFGENOME $PROCESSED/pool_f4m/$1.mkdup.bam > $PROCESSED/freebayesVCF/$1.vcf


#freebayes -f $REFGENOME $PROCESSED/pool_f4m/ERR6634978.mkdup.bam > $PROCESSED/freebayesVCF/ERR6634978.vcf

#Quality filtering
echo 'Quality filtering' $1 
vcftools --vcf $PROCESSED/freebayesVCF/$1.vcf --minQ 20 --recode --recode-INFO-all --out $1_q20


