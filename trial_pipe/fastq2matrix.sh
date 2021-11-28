#fast2matrix analysis

BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
#reference file
REFGENOME='refgenome/MTB-h37rv_asm19595v2-eg18.fa'

mkdir cd ~/$PROCESSED/sep_f4m/$1
cd ~/$PROCESSED/sep_f4m/$1
#Maping out variant
echo ***Maping out variant***
stq2vcf.py all --read1 ~/$RAW/$1_1.fastq.gz --read2 ~/$RAW/$1_2.fastq.gz --ref ~/$REFGENOME --prefix $1

#Join genotyping
echo ***Joining genotyping***
merge_vcfs.py genotype --ref ~/$REFGENOME --prefix mtb

#Convert to VCF format
echo ***Converting to desirable format***
bcftools query -f '%POS\t%REF\t%ALT[\t%GT]\n' trial.vcf.gz | head #output into a table formated VCF format

#convert to fasta format
vcf2fasta.py --vcf trial.vcf.gz --ref ~/$REFGENOME

#End of process for this file
echo ======End of process for $1======
cp ~/$PROCESSED/sep_f4m/$1/* ~/$PROCESSED/pool_f4m


#Use iqtree to visualise