#freebayes bam->vcf conversion parallel file running script
#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe

RAW='/mnt/storage7/jody/philippines/renamed'
PROCESSED='/mnt/storage7/lwang/Projects/Philipine_tb_report/vcf/freebayesVCF_new'
REFGENOME='/mnt/storage7/lwang/trial_tb_philippines/refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='~/trial_tb_philippines/pipelines/Genomic_data_analysis/trial_pipe'

#reference file
# REFGENOME='refgenome/MTB-h37rv_asm19595v2-eg18.fa'

#activating variant_detection enviroment
# echo 'activating variant_detection enviroment'
# eval "$(conda shell.bash hook)"
# conda activate variant_detection 

# mkdir $PROCESSED/freebayesVCF
cd $PROCESSED


cat /mnt/storage7/lwang/Projects/Philipine_tb_report/vcf/sample_name.txt | parallel -j 30 "$PIPELINE/freebayes.sh {}"


# "$PIPELINE/freebayes.sh {}"
