# Import
from cs50 import SQL
from sys import argv, exit
import csv

# Db connect
db = SQL("sqlite:///students.db")

# Check cla
if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)

# Open csv file
with open("students.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == "name":
            continue

        # Split name into 3 parts: first, middle and last
        name = row[0].split()
        if len(name) < 3:
            # Insert each student into the db student table if name has only 2 elements: first and last name
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], None, name[1], row[1], row[2])

        else:
            # Insert each student into the db student table if name has 3 elements
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       name[0], name[1], name[2], row[1], row[2])



