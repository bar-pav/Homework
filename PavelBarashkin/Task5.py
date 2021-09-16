# Task 1.4
# Write a Python program to sort a dictionary by key.

def sort_dict(dct):
    print(dict(sorted(dct.items(), key=lambda x: x[0])))


sort_dict({"z": 2, "1": 90, "a": [], "5": "5", "m": "m"})
