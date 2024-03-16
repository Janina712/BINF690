from Sequence import *
from read_fasta import *
from count_fasta import *


def avg_length(filename):
    read_file = read(filename)
    count = count2(filename)
    length = 0
    for k in range(0, count):
        id = list(read_file[k].keys())[0]
        seq = read_file[k][id]['seq']
        length = length + Sequence.get_Seq_length(seq)
    length_avg = length / count
    print("The average sequence length is: ", length_avg)


avg_length("small_sample_mix_format.fasta")
