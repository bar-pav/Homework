# ### Task 4.1
# Implement a function which receives a string and replaces all `"` symbols
# with `'` and vise versa.


def reverse_quotes(string):
    reversed_quotes = {"'": '"', '"': "'"}
    return "".join(reversed_quotes[char] if char in reversed_quotes.keys() else char for char in string)


print(reverse_quotes("aaa''ddd''ddd\"'\"aaa''ddd''ddd\"'\""))
