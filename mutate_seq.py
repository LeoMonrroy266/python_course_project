import sys
from Bio import SeqIO
from Bio.Seq import Seq


def mutate(file, pos, res):
    seq = SeqIO.read(file, "fasta")
    new_seq = [i for i in str(seq.seq)]
    new_seq[pos] = res
    new_seq = ''.join(new_seq)
    seq.seq = Seq(new_seq)
    SeqIO.write(seq, f'{file}_{seq[pos]}{pos}{res}.fasta'.replace('.fasta', ''), "fasta")
