# fast2matrix parallel file running script
#cd ~/pipelines/trial_pipe

BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
PIPELINE='pipelines/trial_pipe'
REFGENOME='refgenome/MTB-h37rv_asm19595v2-eg18.fa'


##activating fast2matrix enviroment
echo ===activating fast2matrix enviroment===
eval "$(conda shell.bash hook)"
conda activate fast2matrix

ls | grep -E '_1' | cut -f 1 -d "_" > sample_name.txt

cd ~/$PIPELINE

#Merging VCF files
echo Merging VCF files
merge_vcfs.py import --sample-file ~/$RAW/sample_name.txt --ref ~/$REFGENOME --prefix mtb --vcf-dir #only run once, because it merges all samples


cat ~/$RAW/sample_name.txt | parallel -j 5 "~/$PIPELINE/fastq2matrix.sh {}"