import re
from Sequence import *


def read(filename):
    # outside of recursion
    f = open(filename, 'r')                                                 # read in file
    file = f.read()
    f.close()

    header = re.compile(r">.+")                                             # find id lines
    h_pattern = header.findall(file)
    #print(len(h_pattern))

    sequence = re.compile(r"[\n][AGCTN\s].+[\n]")                           # find sequence lines
    s_pattern = sequence.findall(file)
    #print(len(s_pattern))

    read_list = []

    # inside of recursion
    def read_rec(h_pattern, s_pattern):
        if not h_pattern:  # stop criterion                                 # unless end of file, keep going
            return read_list
        else:
            current = Sequence.organize_Seq(h_pattern[0], s_pattern[0])    # process using sequence function
            read_list.append(current)
            return read_rec(h_pattern[1:], s_pattern[1:])

    result = read_rec(h_pattern, s_pattern)
    return result


read_file = read("small_sample_mix_format.fasta")
#print(read_file)