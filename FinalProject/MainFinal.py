#! usr/bin/env python

# Final Project: Modules

import re
from random import sample
from Sequence import *
from FASTA import *
from FASTQ import *

# 1. Ask user for input
filename = str(input("Please enter the name of the file that contains your sequence(s)."))

# 2. Determine type of input file
def check_ext(filename):
    """
    Function to check file and sequence type of input. Prints response in console.
    """

    global return_type
    global letter_type
    return_type = "FASTA"
    letter_type = "Peptides"
    extension = re.compile(r".fasta$|.fastq$")
    extension_pattern = extension.findall(filename)

    if not extension_pattern:
        print("ERROR: File extension not supported.")
    else:
        if extension_pattern[0] == ".fastq":
            print("Type of input file: FASTQ")
            print("Type of sequence: Peptides")
            return_type = "FASTQ"
            return return_type, letter_type
        elif extension_pattern[0] == ".fasta":
            print("Type of input file: FASTA")
            read_file = FASTA.read(filename)
            letters_all = []
            # determine length of loop based on file size and pick randomly
            p = round(len(read_file)/10)
            selection = sample(range(0, len(read_file)), p)
            if p == 0:
                p = 1           # ensure that test will run if file contains only 10 or less sequences
            else:
                p = p
            for k in selection:
                id = list(read_file[k].keys())[0]
                letters = list(set(read_file[k][id]['seq']))
                letters_all.append(letters)
            letters_all = [item for sublist in letters_all for item in sublist]
            letters_all = list(set(letters_all))
            count_letters = len(letters_all)
            if count_letters >= 5:
                print("Type of sequence: Peptides")
                return return_type, letter_type
            else:
                print("Type of sequence: Nucleotides")
                letter_type = "Nucleotides"
                return return_type, letter_type
        else:
            print("ERROR: File extension not supported.")


return_type, letter_type = check_ext(filename)

# 3. Use module functions
if return_type == "FASTA":
    read_file = FASTA.read(filename)
    # 3.1.1 total number of sequences
    count = FASTA.count(filename)
    print("Total number of sequences in file: ", count)
    # 3.2 avg GC content of the file( if nucleotide file)
    if letter_type == "Nucleotides":
        percent_gc, percent_gc_avg = Sequence.get_GC_content(read_file)
        print("Average GC content in sequences in file: ", round(percent_gc_avg, 2))
    else:
        print("GC content not available for peptide sequence.")
elif return_type == "FASTQ":
    read_file = FASTQ.read(filename)
    # 3.1.2 total number of sequences
    count = FASTQ.count(filename)
    print("Total number of sequences in file: ", count)

# 3.3 min sequence length of the input file
lengths = Sequence.get_Seq_length(read_file)
print("Min sequence length of the input file: ", min(lengths))
# 3.4 max sequence length of the input file
print("Max sequence length of the input file: ", max(lengths))
# 3.5 average sequence length of the input file
avg_count = sum(lengths)/count
print("Average sequence length of the input file: ", round(avg_count))

# 4. Convert FASTQ to FASTA file
# create dictionary
A_Q = {'!': 0, '"': 1, '#': 2, '$': 3, "%": 4, "&": 5, "'": 6, "(": 7, ")": 8, "*": 9, "+": 10,
       ",": 11, "-": 12, ".": 13, "/": 14, "0": 15, "1": 16, "2": 17, "3": 18, "4": 19, "5": 20, "6": 21,
       "7": 22, "8": 23, "9": 24, ":": 25, ";": 26, "<": 27, "=": 28, ">": 29, "?": 30, "@": 31, "A": 32,
       "B": 33, "C": 34, "D": 35, "E": 36, "F": 37, "G": 38, "H": 39, "I": 40, "J": 41, "K": 42}

min_n = int(input("Please enter the minimum length of sequences that should be displayed.") or "0")
thresh = int(input("Please enter the minimum average quality score of sequences that should be displayed.") or "0")

if return_type == "FASTQ":
    read_file = FASTQ.read(filename)
    convert = str(input("Do you want to convert your fastq file to fasta format?") or "no")
    if convert == 'yes':
        print("FASTQ file in FASTA format:")
        for i in range(0, len(read_file)):
            id = list(read_file[i].keys())[0]
            seq_id = read_file[i][id]['seq_id']
            seq_header = read_file[i][id]['seq_header']
            seq = read_file[i][id]['seq']
            head = f">{seq_id}{seq_header}"
            if thresh in locals():
                qual = read_file[i][id]['quality']
                quality = []
                sum = 0
                for j in range(len(qual)):
                    quality = A_Q[qual[j]]
                    sum = sum + quality
                avg = sum/(len(qual))
                if min_n in locals():
                    if (len(read_file[i][id]['seq']) >= min_n) and (avg >= thresh):
                        print('\n'.join([head, seq]))
                        with open('output.fasta', 'w') as f:
                            f.write(head)
                            f.write('\n')
                            f.write(read_file[i][id]['seq'])
                            f.write('\n')

            elif min_n in locals():
                if len(read_file[i][id]['seq']) >= min_n:
                    print('\n'.join([head, seq]))
                    with open('output.fasta', 'w') as f:
                        f.write(head)
                        f.write('\n')
                        f.write(read_file[i][id]['seq'])
                        f.write('\n')

            else:
                print('\n'.join([head, seq]))
                with open('output.fasta', 'w') as f:
                    f.write(head)
                    f.write('\n')
                    f.write(read_file[i][id]['seq'])
                    f.write('\n')
    else:
        FASTQ.write(filename, "output.fastq")
        print("FASTQ format:")
        f = open(filename, 'r')
        file = f.read()
        print(file)
else:
    read_file = FASTA.read(filename)
    print("FASTA format:")
    for i in range(0, len(read_file)):
        id = list(read_file[i].keys())[0]
        seq_id = read_file[i][id]['seq_id']
        seq_header = read_file[i][id]['seq_header']
        head = f">{seq_id}{seq_header}"
        if len(read_file[i][id]['seq']) >= min_n:
            print(head)
            print(read_file[i][id]['seq'])
            with open('output.fasta', 'w') as f:
                f.write(head)
                f.write('\n')
                f.write(read_file[i][id]['seq'])
                f.write('\n')
        else:
            pass
