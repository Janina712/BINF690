#! usr/bin/env python

# Script with my solutions for assignment 3. Topics include loops and regular expressions.

import re
import random

# Exercise 1
string_a = "GGGCCGTTGGT"
string_b = "GGACCGTTGAC"
HD = 0

for i in range(len(string_a)):
    if string_a[i] != string_b[i]:
        sub = re.subn(string_a[i], string_b[i], string_a[i], count=0)
        HD += 1

print("The Hamming Distance between strings a and b is: ", HD)

# Exercise 2
# Read in FASTA file
F = open('contigs.fasta', 'r')
seq = F.read()
F.close()

# identify headers of nucleotide sequence as pattern
header = re.compile(r">.+")
h_pattern = header.findall(seq)

# print header with corresponding 80 nucleotide sequence
nuc = ""
for i in range(len(h_pattern)):
    print("")
    print(h_pattern[i])
    for line in seq:
        if (line == "A") | (line == "C") | (line == "G") | (line == "T"):
            nuc = nuc + line
            if len(nuc) == 80:
                print(nuc)
                nuc = ""
print("")
print("FASTA file pretty printed.")

# Exercise 3
# Read in FASTQ file
FQ = open('example.fastq', 'r')
seq_Q = FQ.read()
FQ.close()

# find header and sequence
both_Q = re.compile(r"@.+[\n][NATCG]{151}")
both_pattern = both_Q.findall(seq_Q)

# replace @ with >
for i in range(len(both_pattern)):
    sub = re.subn("@", ">", both_pattern[i], count=0)
    both_pattern[i] = sub[0]

# print in FASTA format
for i in range(len(both_pattern)):
    print(both_pattern[i])
    print("")

# save file
Seq_Q_A = open("example.fasta", "w")
Seq_Q_A.write(str(both_pattern))
Seq_Q_A.close()

# Exercise 4
# create dictionary to store ASCII to quality score mapping
A_Q = {'!': 0, '"': 1, '#': 2, '$': 3, "%": 4, "&": 5, "'": 6, "(": 7, ")": 8, "*": 9, "+": 10,
       ",": 11, "-": 12, ".": 13, "/": 14, "0": 15, "1": 16, "2": 17, "3": 18, "4": 19, "5": 20, "6": 21,
       "7": 22, "8": 23, "9": 24, ":": 25, ";": 26, "<": 27, "=": 28, ">": 29, "?": 30, "@": 31, "A": 32,
       "B": 33, "C": 34, "D": 35, "E": 36, "F": 37, "G": 38, "H": 39, "I": 40, "J": 41, "K": 42}

# Define q threshold value and minimum number of bases kept
# (No clear theoretical motivation for the chosen values. More domain knowledge needed.)
thresh = 35
min_n = 100

# convert quality line to q scores
eval_Q = re.compile(r"[+][\n].+")
eval_pattern = eval_Q.findall(seq_Q)
print("That many evals: ", len(eval_pattern))

print("Begin loop: Convert ASCII to Quality Score")
eval_converted = []
for i in range(len(eval_pattern)):
    new = []
    for j in range(len(eval_pattern[i])):
        if (eval_pattern[i][j] == '+') | (eval_pattern[i][j] == '\n'):
            continue
        else:
            new.append(A_Q[eval_pattern[i][j]])
    eval_converted.append(new)

print("end loop: Convert ASCII to Quality Score")

# find the first value that's above threshold from left
# cut left edge
print("begin loop: Cut Edges")
for k in range(len(eval_converted)):
    for i in range(len(eval_converted[k])):
        if int(eval_converted[k][i]) >= thresh:
            eval_converted[k] = eval_converted[k][i:]
            break

# find the first value that's above threshold from right
# cut right edge
for k in range(len(eval_converted)):
    for j in range(len(eval_converted[k])-2, -1, -1):
        if int(eval_converted[k][j]) >= thresh:
            eval_converted[k] = eval_converted[k][:j]
            break
print("end loop: Cut Edges")

# print only sequences that are longer than n
for k in range(len(eval_converted)):
    if int(len(eval_converted[k])) >= thresh:
        print(eval_converted[k])

# Exercise 5a: Print all sequences where average read quality is below the threshold
print("Sequences with average read quality below threshold:")
for k in range(len(eval_converted)):
    if len(eval_converted[k]) == 0:
        continue
    q_avg = sum(eval_converted[k])/len(eval_converted[k])
    if q_avg < thresh:
        print(k, ":", eval_converted[k])

# Exercise 5b: Print all sequences where average read quality is above or the same as the threshold
print("Sequences with average read quality at or above threshold:")
for k in range(len(eval_converted)):
    if len(eval_converted[k]) == 0:
        continue
    q_avg = sum(eval_converted[k])/len(eval_converted[k])
    if q_avg >= thresh:
        print(k, ":", eval_converted[k])

# Exercise 6: Find the longest repeat in the sequence
S = "TGTCAGCTACCTTGATGGATTGAGTTTGTTTCGGTCGATGCTCCATCGGGAGAGAGTCTG\
    CGTCCTGGTCCGAGCAAGTCCCACCAAGTGGCACTTGGCGGCGCCATGTCCTATCTAGTG\
    CCACCATGTCCGAGGACTTTGATGGCACATGGTGGCACTTGATTTGCCCAAGTCCCACCT\
    GCTCCGACGTGGACCGACTTCGTGGCACATCGCTATCACCCACTCTACCGTTGAAAAGCC\
    GAAGTCAAGCGCCGAAAGCTGATCGATTTGCGGTGTGATACGTTGCCAGTGATTCGTTCC\
    GTGGTTTATGCTTGGCGCACCTACCGCGTCCCCGACGCATCGACTCCGCCGCCATTGCGC\
    GGCACAAAACGGCCTTCGATCCTTCCGTACGGAGGGGTACTGCAGGGCTCACTGTTCATG\
    CCGGAAATTGCACCGGCTTTTTTTTCAATCAAATCAAGTGGACCGTGTCGGATAGTGAGG\
    ACACCGGACACCGCGATACCAAGCCGATTGGCGGTCTGTTTGTGAAAATAGACCGTAGTG\
    CGGACAATTCCGAAGCCGGACACCGGACAGGTGCTCTGTGGAAATTCCGCGTATGCCCGA\
    CACCCTTACAGCCGCGTGGCTGGGTGCGGATCACGAAGCCCAAAACACTGCGGCGGGGAT\
    GATCTGACTTTGGGGTGGGGAGCTGCTTTGCGTGCCGAATGACGGCGAACGCAGGCTTCT\
    GAGCAAATATCGATCCGGGGGGCGCCACCGGTACCAGAACGGCGCAACAGGTAATCACCC\
    ATCACGGCAAGGGCCGCAGGCGTGTGGACGCAATCCACGCGAAGGCAGGCTCGCATCCAG\
    AGATGCACCGGATAGGGTGGCCGCGCAAGCGGTGCGTGAGGCGAGAGCCTTGCATGTTCG\
    CGAAGCGGACGGTCACGACGCATTGCTTCCATGCTCAGGGCCGATCGGTTTGGCATCGCT\
    AAAGGACCGGAAGAGTGGTTGTAGGACCGGCAGGGTGGGCCGGCAAGCTGGGGGTGGTAC\
    CCCGGTGCACCAAGCGGGCAGGGCCAATTCGGGGTTGGCGCCGCCGAGAATTGGGTTGCG\
    CAGATTTGCGCGGCCGGCGGGATGCGCTTAGCGCGAATAGGAATCCGTC"

# Attempted to compare each possible substring with each possible substring
# Stopped it after 2 hours
# Realized that the computational complexity of this approach is O(n * m2)
'''
longest_repeat = [""]
for i in range(len(S)):                              # starting position
    print("starting position:", i)
    for k in range(len(S)):                          # sequence length
        print("number of elements in the pattern:", k)
        for j in range(i + 1, len(S)):               # comparison position
            print("Compared to:", S[j:k])
            if S[i:(i+k)] == S[j:(i+k)]:
                repeat = S[i:(i+k)]
                if repeat >= longest_repeat[0]:
                    longest_repeat.append(repeat)
print(longest_repeat)
'''

# this exercise is a common computer science program and can be solved with dynamic programming
# use the longest common substring algorithm to reduce computational load to O(m*n)
# solved the exercise using this link: https://www.bogotobogo.com/python/python_solutions.php#longest_substring
substring = []
longest = 0
for i in range(len(S)):                    # take each element of string as starting point subsequently
    c_set = set()                          # we create a set to store the identified pattern
    for j in range(i, len(S)):             # compare to remaining string (after i) adding one element at a time
        c_set.add(S[j])                    # and store as set
        if len(c_set) > 2:                 # must be one
            break
        if j+1-i == longest:               # if the counter and the 'longest' are the same length,
            substring.append(S[i:j+1])     # we don't want to update but still store the pattern
        if j+1-i > longest:                # if the current counter is larger than previously stored ones
            longest = j+1-i                # we update the counter to the current value
            substring = []                 # remove what we previously stored as the longest pattern
            substring.append(S[i:j+1])     # and store the new pattern

print("The longest repeating pattern in the string S is: ", substring)
print("With a length of ", len(substring[0]), "characters.")

# Exercise 7
string = str(input("Enter a string."))

for i in range(len(string)):
    if string[i] == string[len(string) - i - 1]:
        if i < len(string) - 1:
            continue
        else:
            print("This string is a palindrome!")
    else:
        print("This string is not a palindrome.")
        break

# Exercise 8
target = random.randrange(1, 10)
guess = int(input("Guess a number between 1 and 9."))

if guess == target:
    print("You're exactly right!")
elif guess > target:
    print("Your guess is too high.")
else:
    print("Your guess is too low.")

# Exercise 9
F_rna = open('rna.fasta', 'r')
seq = F_rna.read()
F_rna.close()

# create dictionary of RNA to protein codes
R_P = {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L', 'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S', 'UAU': 'Y',
       'UAC': 'Y', 'UAA': '*', 'UAG': '*', 'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W', 'CUU': 'L', 'CUC': 'L',
       'CUA': 'L', 'CUG': 'L', 'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'CAU': 'H', 'CAC': 'H', 'CAA': 'Q',
       'CAG': 'Q', 'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
       'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'AGU': 'S',
       'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V', 'GCU': 'A', 'GCC': 'A',
       'GCA': 'A', 'GCG': 'A', 'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'GGU': 'G', 'GGC': 'G', 'GGA': 'G',
       'GGG': 'G'}

# identify sequence pattern
rna_seq = re.compile(r"\b[A-Z]+")
rna_seq_pattern = rna_seq.findall(seq)

# take triples and find corresponding protein in dictionary
print("This is the RNA sequences translated into sequences of proteins:")
protein_seq = []
for k in range(len(rna_seq_pattern)):
    protein = []
    for i in range(3, len(rna_seq_pattern[k]), 3):
        start = i - 3
        triplet = rna_seq_pattern[k][start:i]
        protein.append(R_P[triplet])
    protein_seq.append(protein)
    print(''.join(protein_seq[k]))
