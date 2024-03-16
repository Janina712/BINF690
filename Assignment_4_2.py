#! usr/bin/env python

# Assignment 4: Regular expressions and functions.

import re

# exercise 1
def test_email(email_to_test):
    """
    Function to test if email address is valid. Prints response in console.
    :param email_to_test: Email address entered by user to test
    """
    global address
    name = re.compile(r"^[\w.]+[^@]")
    name_pattern = name.findall(email_to_test)

    domain = re.compile(r"(?<=@)[^@][\w.].+(?=.com|.org|.net|.edu|.co.)")
    domain_pattern = domain.findall(email_to_test)

    extension = re.compile(r".com$|.org$|.net$|.edu$|.co.\w{2}$")
    extension_pattern = extension.findall(email_to_test)

    if len(name_pattern) == 0:
        print("Email address not valid.")
    elif len(domain_pattern) == 0:
        print("Email address not valid.")
    elif len(extension_pattern) == 0:
        print("Email address not valid.")
    else:
        print("Email address valid.")
        address = name_pattern + domain_pattern + extension_pattern
        print(address)


email_to_test = str(input("Enter your email address."))
test_email(email_to_test)

# exercise 2
def complement(S):
    """
    Function turns a DNA string into its complementary string.
    :param S: DNA string provided by the user.
    :return: A string that contains the complement of the provided DNA sequence.
    """
    dict = {"A": "T", "T": "A", "G": "C", "C": "G"}
    for idx, item in enumerate(S):
        S = list(S)
        S[idx] = dict[item]
    S = "".join(S)
    return S


dna_string = "TGTCAGCTACCTTGATGGATTGAGTTTGTTTCGGTCGATGCTCCATCGGGAGAGAGTCTGCGTCCTGGTCCGAGCAAGTCCCACCAAGTG"
comp_dna_string = complement(dna_string)
print("This is the original DNA string: ", dna_string)
print("This is the reversed DNA string: ", comp_dna_string)

# exercise 3

def get_elements(input):
    """
    This function counts the number of times a chemical element occurs in a formula
    :param input: it requires the user to input a formula in valid format
    :return: print statement that displays the results for each element on the screen
    """
    # get the patterns
    # word patterns
    element = re.compile(r"[A-Z][a-z]?")
    word_pattern = element.findall(input)

    # get word indices
    starts = []
    ends = []
    for loc_idx in re.finditer(r"[A-Z][a-z]?", input):
        starts.append(loc_idx.start())
        ends.append(loc_idx.end())

    # get directly following number
    all_nums = []
    for i in range(len(word_pattern)):
        current = word_pattern[i]
        number = re.compile(rf"(?<={current})[\d]+")
        number_pattern = number.findall(input)
        all_nums.append(number_pattern)

    # put one for each element not directly followed by a number
    for i in range(len(all_nums)):
        if not all_nums[i]:
            all_nums[i] = ['1']

    # get multipliers
    mult = re.compile(rf"(?<=\))[\d]+")
    mult_pattern = mult.findall(input)

    # get multiplication bracket starting index
    starts_m = []
    for loc_idx in re.finditer(r"\(", input):
        starts_m.append(loc_idx.start())

    # get multiplication bracket ending index
    ends_m = []
    for loc_idx in re.finditer(r"\)", input):
        ends_m.append(loc_idx.end())


    def mult_func(mult_pattern, word_pattern, all_nums, starts_m, ends_m, result_output):
        """
        This function performs multiplication of elements inside a bracket
        :param mult_pattern: A list of lists. Each list contains a single value by which the bracket is multiplied.
        :param word_pattern: A list of all the patterns that represent elements
        :param all_nums: A list of values that represents the count of elements before multiplication
        :param starts_m: A list of values that represent the starting point of a multiplication bracket.
        :param ends_m: A list of values that represent the ending point of a multiplication bracket.
        :param result_output: empty dictionary to store results
        :return: Function returns dictionary with elements as keys and their #occurences as values
        """
        if not mult_pattern:            # stop criterion
            return result_output
        else:
            previous = []
            for j in range(len(starts)):
                if (starts[j] > starts_m[0]) and (starts[j] < ends_m[0]):      # if there are elements within the m-bracket
                    if word_pattern[j] in result_output.keys():                # check if element is already assigned a value
                        counter = previous.count(word_pattern[j])              # count how many times element has already occurred up to this point
                        result_output[word_pattern[j]] = result_output.get(word_pattern[j]) + (int(all_nums[j][counter-1]) * int(mult_pattern[0])) # if yes, add, don't update
                        previous.append(word_pattern[j])
                    else:
                        result_output[word_pattern[j]] = int(all_nums[j][0]) * int(mult_pattern[0]) # or create new key with value
                        previous.append(word_pattern[j])
            return mult_func(mult_pattern[1:], word_pattern, all_nums, starts_m[1:], ends_m[1:], result_output)

    result_output = {}
    result = mult_func(mult_pattern, word_pattern, all_nums, starts_m, ends_m, result_output)

    # now add elements that are not inside a multiplication bracket
    for k in range(len(word_pattern)):
        if not word_pattern[k] in result.keys():
            result[word_pattern[k]] = int(all_nums[k][0])

    print("Result:")
    for i in result:
        print(i, ": ", result[i])
    return result


user_input = str(input("Please enter a chemical formula."))
get_elements(user_input)

# exercise 4
def get_p_words(S):
    """
    Function to get all words that start with p or P.
    :param S: A sentence provided by the user
    :return: A list of strings, each corresponding to a word that starts with p or P
    """
    name = re.compile(r"\b[\w.+].+?\b")
    word_pattern = name.findall(sentence_to_test)
    p_words = []
    for i in range(len(word_pattern)):
        if (word_pattern[i][0] == "P")|(word_pattern[i][0] == "p"):
            p_words.append(word_pattern[i])
    return p_words


sentence_to_test = str(input("Please enter a sentence."))
user_output = get_p_words(sentence_to_test)
print(user_output)

# exercise 5
P = "CTTAAAAGCG"
C = "CGCTTTTAAGACTTAAAAGCGTTTGCTATGGACCTTAAAAGCGATCCACTTAAAAGCGTCTTAAAAGCGAACTTAAAAGCGGCGATTTGTCCTGCCTGAGTGCGGAAT\
     CAGAGGTTGATGTGTTGATGGACTCGAGTCATACAAGCGGAACTAGATACGGGGGGACTTCACCTGCGTTCTCAACTGCAGATCTAGAAGTGTTGATGTAGCTAGCAC\
     TCCAGAACGACTGTTTAACTTGGAGACCTCTCGTACAACATTTCGTTTCCGACACCCGTGTATAGGCGTCAAGAACGGAACCCGTATCTTAGAGGGGGATTCTCTTTT\
     CTTACTCAAATTTGTGGCGGAATAACCGCGAATGAATCAACTGTATGCGGCTCTACTATGTGTAGATCATTTCGCATCAGCACCCAGAGCGCCCAGTGCAATACTGGT\
     TGCCAGTTGCGCTGTATCCTTGACCCAGATGATAGTCCTAGGATCTAGGCCCGCGCAAACACCCTAACAACTAGTTATCCCAACATTCGCCGCCAAAAGGGTCAACAA\
     GAGCGGGGCTGGAACTTCATCGCTTTTGCTATGAGGTTAAAACATCGGTACAGAGAACCCCCGGTGCAGGGAGGGGATGGGTATTGGGAACAAGATATACGAGCCGGA\
     GCAAAGCGTCATTACCCATGTGTAGGAACACGGGGTTCAAAGTAGTCCACAATCCACGATCGATTCCCATGAACCTGGCCATATGAGCCAAGTCGTACTATAAGAAGC\
     CTCTCCGCGCCTACGCCGCACGTTTTAAGGCCGTTTATCTTCCGTGATACTGGGTCGGTGTGC"

# get complement of P
P_complement = complement(P)

# reverse complement of P
P_reversed = P_complement[::-1]

# find starting location of P_reversed in C
loc_idx = re.search(P_reversed, C)
print("The reverse complement of P starts at position ", loc_idx.span()[0])

# find starting locations of all P occurrences in C
starts = []
for loc_idx in re.finditer(P, C):
    starts.append(loc_idx.start())
print("The number of occurrences of P in C is ", len(starts))
print("The respective starting locations are ", starts)
