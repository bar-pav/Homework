# ### Task 4.9
# Implement a bunch of functions which receive a changeable number of strings and return next parameters:
#
# 1) characters that appear in all strings
#
# 2) characters that appear in at least one string
#
# 3) characters that appear at least in two strings
#
# 4) characters of alphabet, that were not used in any string
#
# Note: use `string.ascii_lowercase` for list of alphabet letters

import itertools


def test_string(list_of_string):

    unique_chars_in_strings = []
    for string in list_of_string:
        unique_chars_in_strings.append({char.lower() for char in string})

    def test_1_1(lst):
        result = unique_chars_in_strings[0]
        for chars in unique_chars_in_strings[1:]:
            result = result.intersection(chars)
        return sorted(result)

    def test_1_2(lst):
        result = set()
        for string in lst:
            result.update(string.lower())
        return sorted(result)

    def test_1_3(lst):
        result = set()
        combinations = [*itertools.combinations(unique_chars_in_strings, 2)]
        for comb in combinations:
            result.update(comb[0] & comb[1])
        return sorted(result)

    def test_1_4(lst):
        alphabet = {chr(i) for i in range(ord('a'), ord('z') + 1)}
        for string in unique_chars_in_strings:
            alphabet = alphabet.difference(string)
        return sorted(alphabet)

    tests = [test_1_1, test_1_2, test_1_3, test_1_4]
    for test in tests:
        print(test(list_of_string))


test_string(["hello", "world", "python", ])
