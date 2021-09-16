# Task 1.1
# Write a Python program to calculate the length of a string without using the `len` function.

def string_length(string):
    length = 0
    for _ in string:
        length += 1
    print("length of: \"" + string + "\" = " + str(length))


string_length('Some string')
