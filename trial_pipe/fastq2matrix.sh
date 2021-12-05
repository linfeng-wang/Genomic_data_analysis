#fast2matrix analysis

BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
#reference file
REFGENOME='refgenome/MTB-h37rv_asm19595v2-eg18.fa'


##activating fast2matrix enviroment
eval "$(conda shell.bash hook)"
conda activate fastq2matrix

mkdir cd ~/$PROCESSED/sep_f4m/$1
cd ~/$PROCESSED/sep_f4m/$1
#Maping out variant
echo "***Maping out variant***"
fastq2vcf.py all --read1 ~/$RAW/$1_1.fastq.gz --read2 ~/$RAW/$1_2.fastq.gz --ref ~/$REFGENOME --prefix $1

#End of process for this file
echo "======End of process for $1======"
cp ~/$PROCESSED/sep_f4m/$1/* ~/$PROCESSED/pool_f4m
