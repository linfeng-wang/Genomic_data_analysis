#fast2matrix parallel file running script
#cd ~/pipelines/Genomic_data_analysis/trial_pipe

#BASE ='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
PIPELINE='pipelines/Genomic_data_analysis/trial_pipe'
REFGENOME='refgenome/MTB-h37rv_asm19595v2-eg18.fa'


##activating fast2matrix enviroment
echo "===activating fast2matrix enviroment==="
eval "$(conda shell.bash hook)"
conda activate fastq2matrix

#create a file with all the name of the samples
cd ~/$RAW
ls | grep -E '_1' | cut -f 1 -d "_" > sample_name.txt
cd ~/$PIPELINE

cat ~/$RAW/sample_name.txt | parallel -j 1 "~/$PIPELINE/fastq2matrix.sh {}"

cd ~/$PROCESSED/pool_f4m/

#Merging VCF files #can this merge_vcf python file be found this way since we are not in its directory
echo "***Merging VCF files***"
merge_vcfs.py import --sample-file ~/$RAW/sample_name.txt --ref ~/$REFGENOME --prefix trial --vcf-dir #only run once, because it merges all samples

#Join genotyping
echo "***Joining genotyping***"
merge_vcfs.py genotype --ref ~/$REFGENOME --prefix trial

#Convert to VCF format
echo "***Converting to desirable format***"
bcftools query -f '%POS\t%REF\t%ALT[\t%GT]\n' trial.2020_06_24.genotyped.vcf.gz | head #output into a table formated VCF format

#convert to fasta format
echo "***Converting to fasta format"
vcf2fasta.py --vcf trial.vcf.gz --ref ~/$REFGENOME

#Next - Use iqtree to visualise