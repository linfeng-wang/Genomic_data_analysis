#freebayes bam to vcf conversion
#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe

RAW='/mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk_new'
PROCESSED='/mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk_new_vcf'
REFGENOME='../../../refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'


# #activating variant_detection enviroment
# echo 'activating variant_detection enviroment'
# eval "$(conda shell.bash hook)"
# conda activate variant_detection 

# mkdir $PROCESSED/freebayesVCF
# cd $PROCESSED/freebayesVCF

#Converting bam to vcf file
echo 'converting .bam to .vcf for sample' $1 
freebayes -f $REFGENOME $RAW/$1.bam > $PROCESSED/$1.vcf

bgzip -c $PROCESSED/$1.vcf > $PROCESSED/$1.vcf.gz
tabix -p vcf $PROCESSED/$1.vcf.gz

#freebayes -f $REFGENOME $PROCESSED/pool_f4m/ERR6634978.mkdup.bam > $PROCESSED/freebayesVCF/ERR6634978.vcf

#Quality filtering
# echo 'Quality filtering' $1 
# vcftools --vcf $PROCESSED/freebayesVCF/$1.vcf --minQ 20 --recode --recode-INFO-all --out $1_q20


# freebayes -f /mnt/storage7/lwang/trial_tb_philippines/refgenome/MTB-h37rv_asm19595v2-eg18.fa /mnt/storage7/lwang/trial_tb_philippines/data/processed/seqtk_new/ERR752118-ERR2864232-1585.bam > ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe/test/test1.vcf
