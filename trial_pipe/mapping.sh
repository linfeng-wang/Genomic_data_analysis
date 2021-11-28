#mapping and variant detection automation script
#paths
BASE='data/trial'
RAW='data/trial/raw_fastq'
PROCESSED='data/trial/processed'
#reference file
#REFGENOME ='refgenome/MTB-h37rv_asm19595v2-eg18.fa'

##Mapping
eval "$(conda shell.bash hook)"
conda activate mapping
echo =======Mapping=======
mkdir cd ~/$PROCESSED/sep/$1
cd ~/$PROCESSED/sep/$1

#Sample File found
echo sample file: $1
#trimming
echo ***trimming***
trimmomatic PE ~/$RAW/$1_1.fastq.gz ~/$RAW/$1_2.fastq.gz -baseout $1 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 MINLEN:36

#indexing reference genome
#echo ***indexing reference genome***
#bwa index ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa <-do this only once, it's done in the mapping_parallel script

#Transfer sam to binary and index the bam file
echo ***bwa: sam to bam***
bwa mem -c 100 -R "@RG\tID:$1\tSM:$1\tPL:Illumina" -M -T 50 ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa ${1}_1P ${1}_2P | samtools sort -o $1.bam -
samtools index $1.bam
#variant detection is going to be done for this one
#"@RG\tID:$1\tSM:$1\tPL:Illumina" - ID and SM is needed for variant calling
 
# bwa mem ~/data/malaria/Pf3D7_05.fasta ~/data/malaria/IT.Chr5_1.fastq.gz ~/data/malaria/IT.Chr5_2.fastq.gz | samtools view -b - | samtools sort -o IT.Chr5.bam -
#variant detection is not going to be done in this example
#flagging
echo ***flagging***
samtools flagstat $1.bam

# echo Delete P_U file? [y/n]
# read deletepu

# if [deletepu -eq y]; then
rm $1_1P $1_1U $1_2P $1_2U;


##Variant detection
eval "$(conda shell.bash hook)"
conda activate variant_detection
echo ======Variant Detection======

#perform SNP and short indel calling
echo ***Performing SNP and short indel calling***
bcftools mpileup -B -Q 23 -d 2000 -C 50 -f ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa ~/$PROCESSED/sep/$1/$1.bam | bcftools call --ploidy 1 -mvO v - > $1.raw.vcf

#Obtain a high quality set of variants in VCF format
echo ***Obtaining a high quality set of variants in VCF format***
cat $1.raw.vcf | vcfutils.pl varFilter -d 10 -D 2000 > $1.filt.vcf
#cat ERR6634978.raw.vcf | vcfutils.pl varFilter -d 10 -D 2000 > ERR6634978.filt.vcf
#variant calling
cd ~/$PROCESSED/sep/$1
gatk HaplotypeCaller -R ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa -I ~/$PROCESSED/sep/$1/$1.bam -O $1.gatk.raw.vcf -ploidy 1
# gatk HaplotypeCaller -R ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa -I ~/data/trial/processed/sep/ERR6634978/ERR6634978.bam -O ERR6634978.gatk.raw.vcf -ploidy 1

#conda
#To index the resulting VCF files type
echo ***indexing the resulting VCF files type***

bgzip $1.filt.vcf
tabix -p vcf $1.filt.vcf.gz

#Detect structural variant
echo ***detecting structural variant***
delly call -o $1.delly.bcf -q 20 -s 3 -g ~/refgenome/MTB-h37rv_asm19595v2-eg18.fa ~/$PROCESSED/sep/$1/$1.bam

#Change from delly to .vcf file (so that it can be viewed in text editors)
echo ***converting file format from delly to VCF***
bcftools view $1.delly.bcf > $1.delly.vcf

bgzip $1.delly.vcf
tabix -p vcf $1.delly.vcf.gz

#End of process for this file
echo ======End of process for $1======
cp ~/$PROCESSED/sep/$1/* ~/$PROCESSED/pool
conda activate base