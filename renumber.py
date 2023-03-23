import os
import argparse
from Bio import Align

parser = argparse.ArgumentParser('PDB renumbering according to fasta')
parser.add_argument('--pdb_file', help='input path for pdb file')
parser.add_argument('--fasta_file', help='input path for fasta file')
parser.add_argument('--out_file', help='output path for renumbered pdb file')
args = parser.parse_args()
print(args)

def remap_resnum_for_line(pdb_file, mapping):
    newlines = []
    last_resstr = ""
    resi = 0

    with open(pdb_file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if not line.startswith('ATOM '):
                continue
        left = line[:22]
        right = line[27:]
        resstr = line[22:27]
        if resstr == last_resstr:
            newstr = "%4d " % mapping[resi]
        else:
            last_resstr = resstr
            if resi != len(mapping):
                resi += 1
            if resi == len(mapping):
                resi = resi
            newstr = "%4d " % mapping[resi]
        #print("|"+resstr+"|"+newstr+"|")
        newlines.append(left+newstr+right)
    return newlines

def main():
    # pdb_file = './pdb/7XNO_A.pdb'
    # pdb_id = os.path.basename(pdb_file).split('.pdb')[0]
    # fasta_file = f'./fasta/{pdb_id}.fasta'
    pdb_file = args.pdb_file
    fasta_file = args.fasta_file
    out_file = args.out_file

    pdb_seqls = os.popen(f'pdb_tofasta {pdb_file}').readlines()[1:]
    pdb_seq = ''.join([i.strip() for i in pdb_seqls]).replace('X', '')
    print(f'pdb_seq: {pdb_seq}')
    with open(fasta_file, 'r') as f:
        fasta_seq = f.readlines()[1].strip()
    print(f'fasta_seq: {fasta_seq}')

    aligner = Align.PairwiseAligner()
    alignment = aligner.align(fasta_seq, pdb_seq)[0]
    print(alignment)
    assert len(alignment[0]) == len(fasta_seq)


    p_pdb = 0
    p_fst = 0
    mapping = {}
    for i in alignment[1]:
        p_fst += 1
        if i != '-':
            p_pdb += 1
            mapping[p_pdb] = p_fst
    # print(mapping)

    new_lines = remap_resnum_for_line(pdb_file, mapping)
    with open(out_file, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    main()


