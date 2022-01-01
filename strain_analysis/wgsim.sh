#script for generating a number of simulated fastq file with set amount of mutations
#local path: cd ~/trial_tb_philippines/pipelines/Genomic_data_analysis/strain_analysis

#Parameters to be configured
########################
declare -i read_len=150
declare mut_rate=0.05
declare -i sample_num=10
########################

RAW='/mnt/storage7/lwang/trial_tb_philippines/data/wgsim/wgsim_150bp_0.05mutation'
PROCESSED='/mnt/storage7/lwang/trial_tb_philippines/data/processed/wgsim/wgsim_150bp_0.05mutation'
REFGENOME='/mnt/storage7/lwang/trial_tb_philippines/refgenome/MTB-h37rv_asm19595v2-eg18.fa'
PIPELINE='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/strain_analysis'

#activating fast2matrix enviroment
echo "===activating variant_detection enviroment==="
eval "$(conda shell.bash hook)"
conda activate variant_detection

#creating a new file in the data folder
mkdir $RAW/../wgsim
mkdir $RAW/../wgsim/wgsim_${read_len}bp_${mut_rate}mutation   #change this folder name when creating new files
cd $RAW/../wgsim/wgsim_${read_len}bp_${mut_rate}mutation

#creating wgsim simulated files
for ((i=1; i<=$sample_num; i++)); do
    wgsim -1 $read_len -2 $read_len -r $mut_rate -R 0 -X 0 -e 0 $REFGENOME simulated${i}_1.fastq simulated${i}_2.fastq
    bgzip simulated${i}_1.fastq 
    bgzip simulated${i}_2.fastq 
done

#save all sample name in a txt file
ls | grep -E '_1' | cut -f 1 -d "_" > sample_name.txt
