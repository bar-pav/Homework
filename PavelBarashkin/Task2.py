# Task 1.2
# Write a Python program to count the number of characters (character frequency) in a string (ignore case of letters).

def number_of_chars(s):
    char_frequency = dict()
    for char in s.lower():
        if char in char_frequency.keys():
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1
    print(char_frequency)


number_of_chars("Your string could be here")
