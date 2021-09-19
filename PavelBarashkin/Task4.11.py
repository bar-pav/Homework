# ### Task 4.11
# Implement a function, that receives changeable number of dictionaries (keys - letters, values - numbers) and combines
# them into one dictionary. Dict values ​​should be summarized in case of identical keys

def combine_dicts(*args):
    combined_dict = {}
    for dict in args:
        for key, value in dict.items():
            combined_dict[key] = combined_dict.get(key, 0) + value
    return combined_dict


dict_1 = {'a': 100, 'b': 200}
dict_2 = {'a': 200, 'c': 300}
dict_3 = {'a': 300, 'd': 100}

print(combine_dicts(dict_1, dict_3, dict_2))
