#! usr/bin/env python

# Project 1: Exclude and trim sequences in a fasta file.

import re

# Part 1
# Read in input FASTA file
F = open('Scaffolds.fasta', 'r')
seq = F.read()
F.close()

# Remove sequences as listed in exclude file
# Read in exclude file
F = open('exclude_list.tab', 'r')
exclude = F.read()
F.close()

# identify individual entries in seq file
entry = re.compile(r">([^>]*)")
entry_pattern = entry.findall(seq)
print("There are this many entries in the FASTA file: ", len(entry_pattern))

# identify headers in seq file
header = re.compile(r">.*")
h_pattern = header.findall(seq)
print("Sanity check: There are this many headers in the FASTA file: ", len(h_pattern))
print(h_pattern)

# remove > in pattern
# and add tab at the end
for i in range(len(h_pattern)):
    sub = re.subn(">", "", h_pattern[i], count=0)
    h_pattern[i] = sub[0]
    h_pattern[i] = h_pattern[i] + "\t"

# search for pattern in exclude file
count = -1
to_be_removed = []
for i in range(len(h_pattern)):
    match = exclude.find(h_pattern[i])
    if match != -1:                         # if the ID is found on the exclude file
        print("Exclude:", h_pattern[i])     # exclude that entry
        to_be_removed.append(entry_pattern[i])
    else:
        continue

# add > and
# remove line breaks
for i in range(len(to_be_removed)):
    to_be_removed[i] = ">" + to_be_removed[i]
    to_be_removed[i].replace('\n', '')

# delete in seq
for i in range(len(to_be_removed)):
    match = seq.find(to_be_removed[i])
    if match != -1:
        end = match + len(to_be_removed[i])
        substring = seq[match:end]
        str_list = seq.split(substring)
        seq = "".join(str_list)
    else:
        continue

# save FASTA file with sequences removed (output 1)
new_scaffolds = open("Scaffolds_removed.fasta", "w")
new_scaffolds.write(str(seq))
new_scaffolds.close()

# Part 2
# Read in input FASTA file without exclude sequences
F = open('Scaffolds_removed.fasta', 'r')
seq = F.read()
F.close()

# Read in trim file
# read in line by line
F = open('trim_list.tab', 'r')
entries = F.readlines()
F.close()

# remove entries marked 'mitochondrion-not_cleaned'
to_be_removed = []  # marked rows
remove = 0
entries_short = []  # unmarked rows
keep = 0
for i in range(len(entries)):
    match = entries[i].find('mitochondrion-not_cleaned')
    if match != -1:  # if marking is to be marked
        to_be_removed.append(entries[i])  # store to remove
        remove = remove + 1
    else:
        entries_short.append(entries[i])  # keep not marked records in a separate list
        keep = keep + 1

# get IDs in unmarked_trim (entries on trim_tab file that are not marked mitochondrion-not_cleaned)
entries_short = ''.join(entries_short)
ID_unm_trim = re.compile(r"scaffold\d+")
ID_unm_pattern = ID_unm_trim.findall(entries_short)

print(to_be_removed)
# get ID patterns in to_be_removed (entries on trim_tab file that are marked mitochondrion-not_cleaned)
to_be_removed = ''.join(to_be_removed)
ID = re.compile(r"scaffold\d+")
ID_pattern = ID.findall(to_be_removed)
print("There are this many IDs: ", len(ID_pattern))

# get length in to_be_removed
length = re.compile(r"[\t]\d+[\t]")
length_pattern = length.findall(to_be_removed)
print("There are this many lengths: ", len(length_pattern))

for i in range(len(ID_pattern)):
    match = seq.find(ID_pattern[i])
    if match != -1:
        end = match + int(length_pattern[i])
        substring = seq[match:end]
        str_list = seq.split(substring)
        seq = "".join(str_list)
    else:
        continue
#######################################################################################################################
# save sub-results
unmarked_seq_list = open("trim_unmarked.fasta", "w")
unmarked_seq_list.write(str(seq))
unmarked_seq_list.close()

# save sub-results
unmarked_trim_list = open("trim_list_unmarked.tab", "w")
unmarked_trim_list.write(str(entries_short))
unmarked_trim_list.close()
#######################################################################################################################
#######################################################################################################################
# import entries short
F = open('trim_list_unmarked.tab', 'r')
entries_short = F.readlines()
F.close()
#######################################################################################################################
# We work with the IDs that are not marked in the trim file
# the seq file contains unmarked sequences that need to be trimmed, and sequences that don't need trimming
entries_short = ''.join(entries_short)

# IDs of sequences that need to be trimmed
ID_unm_trim = re.compile(r"scaffold\d+")
ID_unm_pattern = ID_unm_trim.findall(entries_short)

# starts of trimmed spans
starts = re.compile(r"[\t|,]\d+[.]")
starts_pattern = starts.findall(entries_short)                                      #

# strip extra characters of start point edges
for i in range(len(starts_pattern)):
    starts_pattern[i] = starts_pattern[i].replace('.', '')
    starts_pattern[i] = starts_pattern[i].replace('\t', '')

# ends of trimmed spans
ends = re.compile(r"[.]\d+[\t|,]")  # get length pattern: [\t]\d+.
ends_pattern = ends.findall(entries_short)

# strip extra characters of end point edges
for i in range(len(starts_pattern)):
    ends_pattern[i] = ends_pattern[i].replace('.', '')
    ends_pattern[i] = ends_pattern[i].replace('\t', '')

# dictionary with starting positions
starts_dict = {}
current = 0
for i in range(len(ID_unm_pattern)):
    starts_dict[ID_unm_pattern[i]] = [starts_pattern[current]]
    current = current + 1
    if current == len(starts_pattern):
        break
    while (',' in ends_pattern[current-1]) | (',' in starts_pattern[current]):
        starts_dict[ID_unm_pattern[i]].append(starts_pattern[current])
        current = current + 1
        if current == len(starts_pattern):
            break
    else:
        if current == len(starts_pattern):
            break
        continue

# get length of span(s) to be trimmed
length = re.compile(r"[\t]\d+[\t]")
length_pattern = length.findall(entries_short)

# dictionary with ending positions
ends_dict = {}
current = 0
for i in range(len(ID_unm_pattern)):
    ends_dict[ID_unm_pattern[i]] = [ends_pattern[current]]
    current = current + 1
    if current == len(ends_pattern):
        break
    while (',' in ends_pattern[current-1]) | (',' in starts_pattern[current]):
        ends_dict[ID_unm_pattern[i]].append(ends_pattern[current])
        current = current + 1
        if current == len(ends_pattern):
            break
    else:
        if current == len(ends_pattern):
            break
        continue

# remove any commas
for i in starts_dict:
    for j in range(len(starts_dict[i])):
        starts_dict[i][j] = starts_dict[i][j].strip(',')
for i in ends_dict:
    for j in range(len(ends_dict[i])):
        ends_dict[i][j] = ends_dict[i][j].strip(',')

print("starting position: ", starts_dict)
print("ending position: ", ends_dict)

#######################################################################################################################
# read in fasta sequence
F = open('trim_unmarked.fasta', 'r')
seq_unmarked = F.read()
F.close()
#######################################################################################################################
# get fasta IDs
seq_string = "".join(seq_unmarked)
header = re.compile(r">scaffold.*")
h_pattern = header.findall(seq_string)
print("That many headers: ", len(h_pattern))

# strip extra characters of end point edges
for i in range(len(h_pattern)):
    h_pattern[i] = h_pattern[i].replace('>', '')
    h_pattern[i] = h_pattern[i].replace('\t', '')

# get fasta sequences
seqs = re.compile(r"[^>]([\n][\w].*)")
seqs_pattern = seqs.findall(seq_string)
print("That many sequences: ", len(seqs_pattern))

# strip extra characters of end point edges
for i in range(len(seqs_pattern)):
    seqs_pattern[i] = seqs_pattern[i].strip()

# if dictionary key matches one of the IDs, do trimming
for ID in starts_dict:
    for i in range(len(h_pattern)):
        if ID == h_pattern[i]:
            diff = 0
            pre = len(seqs_pattern[i])
            for j in range(len(starts_dict[ID])):
                trim_string = seqs_pattern[i][(int(starts_dict[ID][j])-diff):(int(ends_dict[ID][j])-diff)]
                str_list = seqs_pattern[i].split(trim_string)
                str_list[0] = str_list[0].strip("N")
                str_list[1] = str_list[1].strip("N")
                seqs_pattern[i] = "".join(str_list)
                post = len(seqs_pattern[i])
                diff = pre - post

# ensure minimum length of sequence
thresh = 250  # assignment suggests 200 as the threshold, will use 250 because no sequence is shorter than 200
k = 0
for i in range(len(seqs_pattern)):
    if len(seqs_pattern[i-k]) < thresh:
        seqs_pattern.remove(seqs_pattern[i-k])
        h_pattern.remove(h_pattern[i-k])
        k = k + 1
print("The number of sequences removed is", k)

# convert back into fasta format
# add >
for i in range(len(h_pattern)):
    h_pattern[i] = ">" + h_pattern[i]
# add IDs back in
zipped = zip(h_pattern, seqs_pattern)
fasta_zipped = str(list(zipped))
# replace commas with line breaks and get rid of other characters
fasta_zipped = fasta_zipped.replace(',', '\n')
fasta_zipped = fasta_zipped.replace(')', '')
fasta_zipped = fasta_zipped.replace('(', '')
fasta_zipped = fasta_zipped.replace("'", '')

# save output 2
new = open("trimmed(unmarked_output2).fasta", "w")
new.write(fasta_zipped)
new.close()

# Part 3
#######################################################################################################################
# import trim_list
F = open('trim_list.tab', 'r')
entries = F.readlines()
F.close()
#######################################################################################################################
# the seq file contains unmarked and marked sequences that need to be trimmed, and sequences that don't need trimming
entries = ''.join(entries)

# IDs of sequences that need to be trimmed
ID_trim = re.compile(r"scaffold\d+")
ID_trim_pattern = ID_trim.findall(entries)

# starts of trimmed spans
starts = re.compile(r"[\t|,]\d+[.]")
starts_pattern = starts.findall(entries)                                      #

# strip extra characters of start point edges
for i in range(len(starts_pattern)):
    starts_pattern[i] = starts_pattern[i].replace('.', '')
    starts_pattern[i] = starts_pattern[i].replace('\t', '')

# ends of trimmed spans
ends = re.compile(r"[.]\d+[\t|,]")  # get length pattern: [\t]\d+.
ends_pattern = ends.findall(entries)

# strip extra characters of end point edges
for i in range(len(starts_pattern)):
    ends_pattern[i] = ends_pattern[i].replace('.', '')
    ends_pattern[i] = ends_pattern[i].replace('\t', '')

# dictionary with starting positions
starts_dict = {}
current = 0
for i in range(len(ID_trim_pattern)):
    starts_dict[ID_trim_pattern[i]] = [starts_pattern[current]]
    current = current + 1
    if current == len(starts_pattern):
        break
    while (',' in ends_pattern[current-1]) | (',' in starts_pattern[current]):
        starts_dict[ID_trim_pattern[i]].append(starts_pattern[current])
        current = current + 1
        if current == len(starts_pattern):
            break
    else:
        if current == len(starts_pattern):
            break
        continue

# get length of span(s) to be trimmed
length = re.compile(r"[\t]\d+[\t]")
length_pattern = length.findall(entries)
print("There are this many lengths: ", len(entries))

# dictionary with ending positions
ends_dict = {}
current = 0
for i in range(len(ID_trim_pattern)):
    ends_dict[ID_trim_pattern[i]] = [ends_pattern[current]]
    current = current + 1
    if current == len(ends_pattern):
        break
    while (',' in ends_pattern[current-1]) | (',' in starts_pattern[current]):
        ends_dict[ID_trim_pattern[i]].append(ends_pattern[current])
        current = current + 1
        if current == len(ends_pattern):
            break
    else:
        if current == len(ends_pattern):
            break
        continue

# remove any commas
for i in starts_dict:
    for j in range(len(starts_dict[i])):
        starts_dict[i][j] = starts_dict[i][j].strip(',')
for i in ends_dict:
    for j in range(len(ends_dict[i])):
        ends_dict[i][j] = ends_dict[i][j].strip(',')

print("starting position: ", starts_dict)
print("ending position: ", ends_dict)
#######################################################################################################################
# read in fasta sequence
F = open('Scaffolds_removed.fasta', 'r')
seq = F.readlines()
F.close()
#######################################################################################################################
# get fasta IDs
seq_string = "".join(seq)
header = re.compile(r">scaffold.*")
h_pattern = header.findall(seq_string)
print("That many headers: ", len(h_pattern))

# strip extra characters of end point edges
for i in range(len(h_pattern)):
    h_pattern[i] = h_pattern[i].replace('>', '')
    h_pattern[i] = h_pattern[i].replace('\t', '')

# get fasta sequences
seqs = re.compile(r"[^>]([\n][\w].*[\n])")
seqs_pattern = seqs.findall(seq_string)
print("That many sequences: ", len(seqs_pattern))

# strip extra characters of end point edges
for i in range(len(seqs_pattern)):
    seqs_pattern[i] = seqs_pattern[i].strip()

# if dictionary key matches one of the IDs, do trimming
for ID in starts_dict:
    for i in range(len(h_pattern)):
        if ID == h_pattern[i]:
            diff = 0
            pre = len(seqs_pattern[i])
            for j in range(len(starts_dict[ID])):
                trim_string = seqs_pattern[i][(int(starts_dict[ID][j])-diff):(int(ends_dict[ID][j])-diff)]
                str_list = seqs_pattern[i].split(trim_string)
                str_list[0] = str_list[0].strip("N")
                str_list[1] = str_list[1].strip("N")
                seqs_pattern[i] = "".join(str_list)
                post = len(seqs_pattern[i])
                diff = pre - post

# ensure minimum length of sequence
thresh = 200  # assignment suggests 200 as the threshold, will use 250 because no sequence is shorter than 200
k = 0
for i in range(len(seqs_pattern)):
    if len(seqs_pattern[i-k]) < thresh:
        seqs_pattern.remove(seqs_pattern[i-k])
        h_pattern.remove(h_pattern[i-k])
        k = k + 1
print("The number of sequences removed is", k)

# convert back into fasta format
# add >
for i in range(len(h_pattern)):
    h_pattern[i] = ">" + h_pattern[i]
# add IDs back in
zipped = zip(h_pattern, seqs_pattern)
fasta_zipped = str(list(zipped))
# replace commas with line breaks and get rid of other characters
fasta_zipped = fasta_zipped.replace(',', '\n')
fasta_zipped = fasta_zipped.replace(')', '')
fasta_zipped = fasta_zipped.replace('(', '')
fasta_zipped = fasta_zipped.replace("'", '')

# save output 3
new = open("trimmed(unmarked_marked_output3).fasta", "w")
new.write(fasta_zipped)
new.close()
