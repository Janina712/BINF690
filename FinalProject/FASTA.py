import re
from Sequence import *


class FASTA(Sequence):
    """
    Module that handles everything related to fasta files.
    """
    def __init__(self, filename):       # file is required to evoke fasta module
        self.filename = filename

    def read(filename):
        # outside of recursion
        f = open(filename, 'r')                                                 # read in file
        file = f.read()
        f.close()

        header = re.compile(r">.+")                                             # find id lines
        h_pattern = header.findall(file)

        f = open(filename, 'r')                                                 # find sequence in between id lines
        lines = f.readlines()
        read_list = []
        done = []
        sequence = ''
        n = 0
        for m in range(len(lines)):
            if n == len(h_pattern)-1:
                break
            else:
                if lines[m].strip() == h_pattern[n] and lines[m].strip() not in done:  # check for duplicates
                    done.append(h_pattern[n])
                    pass
                elif lines[m].strip() == h_pattern[n+1]:
                    read_list.append(sequence)
                    sequence = ''
                    n = n + 1
                elif lines[m].strip() != h_pattern[n+1]:
                    sequence = sequence + lines[m].strip()

        # ensure that each sequence has one header
        #print(len(read_list))
        #h_pattern = [*set(h_pattern)]
        #print(len(h_pattern))

        def read_rec(h_pattern, read_list):
            if not h_pattern:  # stop criterion                                 # unless end of file, keep going
                return read_list
            else:
                current = Sequence.organize_Seq(h_pattern[0], read_list[0])  # process using sequence function
                read_list.append(current)
                return read_rec(h_pattern[1:], read_list[1:])

        result = read_rec(h_pattern, read_list)
        return result

    def write(filename, write_filename=None):
        read_file = FASTA.read(filename)
        if not write_filename:
            print(read_file)
        else:
            f = open(write_filename, "w")
            f.write(str(read_file))
            f.close()

    def count(filename):
        read_file = FASTA.read(filename)
        count = len(read_file)
        # print("The total number of sequences in the file is: ", count)
        return count

    def avg_length(filename):
        length_avg = 0
        read_file = FASTA.read(filename)
        count = FASTA.count(filename)
        lengths = Sequence.get_Seq_length(read_file)
        length_avg = sum(lengths) / count
        return length_avg
