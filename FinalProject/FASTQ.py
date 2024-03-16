import re
from Sequence import *


class FASTQ(Sequence):
    """
    Module that handles everything related to fastq files.
    """
    def __init__(self, filename):       # file is required to evoke fastq module
        self.filename = filename

    def read(filename):
        f = open("small_sample.fastq", 'r')  # read in file
        file = f.read()
        f.close()

        header = re.compile(r"@.+")  # find id lines
        h_pattern = header.findall(file)

        f = open(filename, 'r')  # find sequence in between id lines
        lines = f.readlines()
        s_pattern = []
        i_pattern = []
        q_pattern = []
        n = 0
        for m in range(len(lines)):
            if n == len(h_pattern):
                break
            else:
                if lines[m].strip() == h_pattern[n]:  # check for duplicates
                    s_pattern.append(lines[m+1].strip())
                    i_pattern.append(lines[m + 2].strip())
                    q_pattern.append(lines[m + 3].strip())
                    n = n + 1
                else:
                    pass

        read_list = []

        # inside of recursion
        def read_rec(h_pattern, s_pattern, i_pattern, q_pattern):
            if not h_pattern:  # stop criterion                                 # unless end of file, keep going
                return read_list
            else:
                current = Sequence.organize_Seq(h_pattern[0], s_pattern[0], i_pattern[0],
                                                q_pattern[0])  # process using sequence function
                read_list.append(current)
                return read_rec(h_pattern[1:], s_pattern[1:], i_pattern[1:], q_pattern[1:])
        result = read_rec(h_pattern, s_pattern, i_pattern, q_pattern)
        return result

    def write(filename, write_filename=None):
        read_file = FASTQ.read(filename)
        if not write_filename:
            print(read_file)
        else:
            f = open(write_filename, "w")
            f.write(str(read_file))
            f.close()

    def count(filename):
        read_file = FASTQ.read(filename)
        count = len(read_file)
        return count

    def avg_length(filename):
        read_file = FASTQ.read(filename)
        count = FASTQ.count(filename)
        lengths = Sequence.get_Seq_length(read_file)
        length_avg = sum(lengths) / count
        return length_avg
    
