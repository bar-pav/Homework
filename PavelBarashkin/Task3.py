# Task 1.3
# Write a Python program that accepts a comma separated sequence of words as input and prints the unique words in sorted
# form.

def sorted_words(words):
    unique_words = list(set(words))
    unique_words.sort()
    print(unique_words)


sorted_words([w.strip() for w in input().split(',')])
