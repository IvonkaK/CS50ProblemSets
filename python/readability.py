from cs50 import get_string
import re


def gradeCount():
    text = get_string("Text: ")

    charCount = letterCounter(text)
    wordCount = wordCounter(text)
    sentenceCount = sentenceCounter(text)

    # average number of letters per 100 words
    L = charCount * 100 / wordCount

    # average number of sentences per 100 words
    S = sentenceCount * 100 / wordCount

    # C-L index
    grade = round(0.0588 * L - 0.296 * S - 15.8)

    # Print correct grade
    if (grade < 1):
        print("Before Grade 1")
    elif (grade >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {grade}")



# count total letters in text
def letterCounter(text):
    counter = 0
    for letter in text:
        if letter.isalpha():
            counter += 1
    return counter

# count total words in text
def wordCounter(text):
    result = text.split(" ")
    return len(result)

# count total sentences in text
def sentenceCounter(text):
    result = re.split(r'[.!?]+', text)
    result = result[:-1]
    return len(result)

gradeCount()