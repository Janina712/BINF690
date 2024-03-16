from Sequence import *
from read_fasta import *


# option 1
def count1(filename):
    with open(filename) as ip_f:
        count = 0
        for line in ip_f:
            if '>' in line:
                count += 1
            else:
                pass
        #print("The total number of sequences in the file is: ", count)


# option 2
def count2(filename):
    read_file = read(filename)
    count = len(read_file)
   # print("The total number of sequences in the file is: ", count)
    return count


count1("small_sample_mix_format.fasta")
count2("small_sample_mix_format.fasta")