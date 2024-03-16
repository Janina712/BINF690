#! usr/bin/env python

import math as math
import numpy as np

a = 6
b = 14
c = 22
d = 37
S = "CGCAGTTGTATTGCTTCCCACATTTATTAGACCACCTATTAAAAATGGATTTCTTCCCATTTCAAGCTGCCCACAAATCTCGCTCCTGATACGTTCTTCACTTCAAGCCGT" \
    "AGCATCCCAATATCAGAAGCGGCGCCGGACTTGTTTTCAAAATATCCACGTATCCCTTCTTTCTCTTTCAATAGAAAACACCCATTGGTTCCGAAATAACGCATCTTATAC" \
    "TGTGGCTTATTGGCGTTACCC"

# 1. Assume right angle triangle with base = b and height = a return length of hypotenuse
HT_length = math.sqrt(a**2 + b**2)
print("The hypotenuse of a right triangle with base = {a:2.0f} and height = {b:2.0f} is {HT_length:7.5f}."
      .format(a=a, b=b, HT_length=HT_length))

# 2.Assume a rectangle of length = c and width = d.
# 2.1 Return area of rectangle
RA_area = c * d
print("The area of a rectangle with length = {c:2.0f} and width = {d:2.0f} is {RA_area:3.0f}."
      .format(c=c, d=d, RA_area=RA_area))

# 2.2 Return perimeter of the rectangle
RA_peri = 2 * (c + d)
print("The perimeter of a rectangle with length = {c:2.0f} and width = {d:2.0f} is {RA_peri:3.0f}."
      .format(c=c, d=d, RA_peri=RA_peri))

# 3. Assume a circle where radius=a
# 3.1 Return area of circle
C_area = math.pi * a**2
print("The area of a circle with radius = {a:2.0f} is {C_area:7.5f}."
      .format(a=a, C_area=C_area))

# 3.2 Return circumference of the circle.
C_peri = 2 * math.pi * a
print("The circumference of a circle with radius = {a:2.0f} is {C_peri:7.5f}."
      .format(a=a, C_peri=C_peri))

# 4. Given a string S of any length and four integers a, b, c and d set above
# 4.1 Slice the string S from indices a through b and c through d (with space in between), inclusively
sliced_S = S[a:b+1] + S[c:d+1]
print("The new substring of S is {sliced_S}."
      .format(sliced_S=sliced_S))

# 4.2 Generate the reverse of string S
S_reverse = ''.join(reversed(S))
print("The reverse of string S is: {S_reverse})"
      .format(S_reverse=S_reverse))

# 5.1 Find first and last location of stop codon TAG and report its starting locations
first = S.find("TAG")
last = S.rfind("TAG")
print(f"The first instance of the substring 'TAG' begins at index {first}, "
      f"while the last 'TAG' begins at position {last}.")

# 5.2 Split the DNA string by stop codon TAG and report each fragment and their respective lengths
fragments = S.split("TAG")
number_frags = len(fragments)
print(f"There are {number_frags} DNA fragments.")

frag1_length = len(fragments[0])
frag2_length = len(fragments[1])
frag3_length = len(fragments[2])
frag4_length = len(fragments[3])
print(f"The lengths of the fragments are {frag1_length}, {frag2_length}, {frag3_length}, and {frag4_length}.")

# 5.3 Report percent GC of original DNA string S
number_G = S.count("G")
number_C = S.count("C")
total = len(S)
percent_GC = (number_G + number_C)/(total/100)
print(f"The percentage of G and C in the DNA string is {percent_GC:7.5f}%")

# 5.4 Report number of A, C, T and G's
number_A = S.count("A")
number_T = S.count("T")
print(f"A, C, T, and G occur {number_A}, {number_C}, {number_T}, and {number_G} times, respectively.")

# 6. Lists
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# 6.1 Return a list of all unique elements
unique_items_a = list(np.unique(a))
unique_items_b = list(np.unique(b))
unique_items = np.unique(a+b)
print(f"Unique numbers from both lists combined are:")
print(*unique_items)

# 6.2 Return a list of all common elements
elements = []
for i in range(0, len(unique_items_a)):
    if unique_items_b.count(unique_items_a[i]) > 0:
        elements.append(unique_items_a[i])
print(f"The elements that are represented in both lists are:")
print(*elements)

# 6.3 Return a list of all elements
print("All elements (duplicates included) from both lists combined are:")
print(*a+b)
