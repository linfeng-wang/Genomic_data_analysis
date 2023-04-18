
# mixed_samples='/mnt/storage7/lwang/trial_tb_philippines/data/insilico_mix_mix'
# VCF='/mnt/storage7/jody/tb_ena/per_sample'
# fastq='/mnt/storage7/lwang/trial_tb_philippines/data/raw_fastq'
fastq='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/QuantTB/in_vitro_samples/fastq'
# output='/mnt/storage7/lwang/Projects/Philipine_tb_report/gmm'
# output='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/QuantTB/mixed_clinical_rerun'
output='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/QuantTB/in_vitro_output'
sample_names='/mnt/storage7/lwang/trial_tb_philippines/pipelines/Genomic_data_analysis/Executable_eval/invitro_mix_name.csv'

# cd $mixed_samples

# ls | grep -E '_1.fastq.gz' | cut -f 1 -d "_" > $output/sample_names.txt 

cd $output
# cat $output/sample_name.txt | parallel -j 1 "quanttb quant -f $mixed_samples/{}_1.fastq.gz $mixed_samples/{}_2.fastq.gz -o {}.txt -op $output -abres"
# cat $sample_names | parallel -j 1 "quanttb quant -f $fastq/{}_1.fastq.gz $fastq/{}_2.fastq.gz -o $output/{}.txt -abres"
cat $sample_names | parallel -j 1 "quanttb quant -f $fastq/{}_1.fastq.gz $fastq/{}_2.fastq.gz -o $output/{}.txt -abres"
