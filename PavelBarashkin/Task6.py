# Task 1.5
# Write a Python program to print all unique values of all dictionaries in a list.

def unique_values_from_dicts(list_of_dict):
    unique_values = set()
    for dct in list_of_dict:
        for val in dct.values():
            unique_values.add(val)
    print(unique_values)


lst = [{"V": "S001"}, {"V": "S002"}, {"VI": "S001"}, {"VI": "S005"}, {"VII": "S005"}, {"V": "S009"}, {"VIII": "S007"}]
unique_values_from_dicts(lst)