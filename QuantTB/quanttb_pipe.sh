
mixed_samples='/mnt/storage7/lwang/trial_tb_philippines/data/insilico_mix_mix'
output='/mnt/storage7/lwang/Projects/Philipine_tb_report/gmm'


cd $mixed_samples

ls | grep -E '_1.fastq.gz' | cut -f 1 -d "_" > $output/sample_name.txt

cd $output
cat $output/sample_name.txt | parallel -j 1 "quanttb quant -f $mixed_samples/{}_1.fastq.gz $mixed_samples/{}_2.fastq.gz -o {}.txt -op $output -abres"
