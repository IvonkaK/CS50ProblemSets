from sys import argv, exit
import csv

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")

# open and read csv file containing STR sequences
with open(argv[1], "r") as csv_file:
    # read content of the csv file into memory
    dna_seq = csv.reader(csv_file)
    for line in dna_seq:
        row = line
        row.pop(0)
        break

# open and read the text file containing DNA seq
with open(argv[2], "r") as txt_file:
    # read content of a text file into memory as a single string in a list
    dna_id = txt_file.readlines()
    dna = dna_id[0]

# create dict to store the sequence to be counted/checked
seq = {}

# and copy the list to the dict (key is the gen)
for element in row:
    seq[element] = 1

# iterate the sequence, if found repetition count it
for key in seq:
    length = len(key)
    longest = 0
    temp_seq = 0
    for i in range(len(dna)):
        # skip to the end of seq after finding it
        while temp_seq > 0:
            temp_seq -= 1
            continue

        # count the segments if it's same as the key and there is a repetition
        if dna[i: i + length] == key:
            while dna[i - length: i] == dna[i: i + length]:
                temp_seq += 1
                i += length

            # compare to the longest and replace it if the new one is longer
            if temp_seq > longest:
                longest = temp_seq

    # store the longest seq in the dictionary with its key
    seq[key] += longest

# open the csv and iterate to compare each line (dict) to sequence
with open(argv[1], newline='') as csv_file:
    dna_seq = csv.DictReader(csv_file)
    for line in dna_seq:
        match = 0
        for el in seq:
            if seq[el] == int(line[el]):
                match += 1
        if match == len(seq):
            print(line['name'])
            exit()
    print("No match")