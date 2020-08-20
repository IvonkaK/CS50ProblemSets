# Import
from cs50 import SQL
from sys import argv, exit

# Db connect
db = SQL("sqlite:///students.db")

# Check cla
if len(argv) != 2:
    print("Usage: python roster.py Gryffindor")
    exit(1)

# Select all students from provided house (in argv[1])
students = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", argv[1])

# Print out each student in the house
for student in students:
    if student['middle'] != None:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")
    else:
        print(f"{student['first']} {student['last']}, born {student['birth']}")
