# Task 1.6
# Write a Python program to convert a given tuple of positive integers into an integer.

def tuple_to_int(tpl):
    str_of_int = ''.join(str(i) for i in tpl)
    return int(str_of_int)


print(tuple_to_int((0, 2, 3, 4)))
