import re
from Sequence import *

# outside of recursion
f = open("small_sample.fastq", 'r')  # read in file
file = f.read()
f.close()

header = re.compile(r"@.+")  # find id lines
h_pattern = header.findall(file)
print(len(h_pattern))

sequence = re.compile(r"((?<=[\n])[ATGCN]+[\s])")  # find sequence lines
s_pattern = sequence.findall(file)
print(len(s_pattern))

info = re.compile(r"[+]")  # find info lines
i_pattern = info.findall(file)
print(len(i_pattern))

quality = re.compile(r"((?<=[+\n])[\w\d#$<>,:;.=@()'%&*/]+)[\n]")  # find quality lines  #just put special characters explicitly
q_pattern = quality.findall(file)                                  # does not work, finds seq instead
print(len(q_pattern))
print(q_pattern)

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

    result = read_rec(h_pattern, s_pattern)
    return result

result = read_rec(h_pattern, s_pattern, i_pattern, q_pattern)
print(result)