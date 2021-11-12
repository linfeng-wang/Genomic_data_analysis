BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
REFGENOME ='refgenome/MTB-h37rv_asm19595-eg18.fa'
cd $RAW

##Mapping
conda activate mapping
echo =======Mapping=======
mkdir ~/$PROCESSED/sep/$1
cd ~/$PROCESSED/sep/$1


#trimmin
echo ***trimming***
trimmomatic PE $~/$RAW/$1_1.fastq.gz ~/$RAW/$1_2.fastq.gz -baseout ~/$PROCESSED/sep/$1 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:36

#indexing reference genome
echo ***indexing reference genome***
bwa index ~/$REFGENOME

#Transfer sam to binary and index the bam file
echo ***bwa***

bwa mem -c 100 -R "@RG\tID:$1\tSM:$1\tPL:Illumina" -M -T 50 ~/$REFGENOME $1_1P $2_2P | samtools view -b - | samtools sort -o $1.bam -samtools index $1.bam
#variant detection is done for this one
#"@RG\tID:$1\tSM:$1\tPL:Illumina" - ID and SM is needed for variant calling
 
# bwa mem ~/data/malaria/Pf3D7_05.fasta ~/data/malaria/IT.Chr5_1.fastq.gz ~/data/malaria/IT.Chr5_2.fastq.gz | samtools view -b - | samtools sort -o IT.Chr5.bam -
#variant detection is not done for this one

#flagging
echo ***flagging***
samtools flagstat $1.bam

echo Delete P&U file? [y/n]
read deletepu

if deletepu -eq y; then
    rm $1_1P $1_1U $1_2P $1_2U;


##Variant detection
conda activate variant_detection
echo ======Variant Detection======

#perform SNP and short indel calling
echo ***Performing SNP and short indel calling***
bcftools mpileup -B -Q 23 -d 2000 -C 50 -f ~/$REFGENOME ~/$PROCESSED/sep/$1/$1.bam | bcftools call --ploidy 1 -mvO v - > $1.raw.vcf

#Obtain a high quality set of variants in VCF format
echo ***Obtaining a high quality set of variants in VCF format***
cat $1.raw.vcf | vcfutils.pl varFilter -d 10 -D 2000 > $1.filt.vcf

#variant calling
cd ~/$PROCESSED/sep/$1
gatk HaplotypeCaller -R ~/$REFGENOME -I ~~/$PROCESSED/sep/$1/$1.bam -O 1$.gatk.raw.vcf -ploidy 1


#To index the resulting VCF files type
echo ***indexing the resulting VCF files type***

bgzip $1.filt.vcf
tabix -p vcf $1.filt.vcf.gz

#Detect structural variant
echo ***detecting structural variant***
delly call -o $1.delly.bcf -q 20 -s 3 -g ~/$REFGENOME ~/$PROCESSED/sep/$1/$1.bam

#Change from delly to .vcf file (so that it can be viewed in text editors)
echo ***converting file format from delly to VCF***
bcftools view $1.delly.bcf > $1.delly.vcf

bgzip $1.delly.vcf
tabix -p vcf $1.delly.vcf.gz