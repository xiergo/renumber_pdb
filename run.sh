#!/usr/bin/bash

#SBATCH -p gpu31
#SBATCH --gres=gpu:1
#SBATCH -c 64

echo Start: $(date)

pdb_dir=./pdb
fasta_dir=./fasta
out_dir=./pdb_renum

find ${pdb_dir} -name '*.pdb' -type f | \
    parallel -kj64 "python renumber.py \
        --pdb_file {} \
        --fasta_file ${fasta_dir}/{/.}.fasta \
        --out_file ${out_dir}/{/.}_renum.pdb"

echo Finished! $(date)