# ### Task 4.6
# Implement a function `get_shortest_word(s: str) -> str` which returns the
# longest word in the given string. The word can contain any symbols except
# whitespaces (` `, `\n`, `\t` and so on). If there are multiple longest words in
# the string with a same length return the word that occures first.

# A character is whitespace if in the Unicode character database (see unicodedata),
# either its general category is Zs (“Separator, space”), or its bidirectional class is one of WS, B, or S.

import unicodedata


def get_longest_word(string):
    longest_word = ""
    word = ""
    string += " "
    for char in string:
        if unicodedata.category(char) == "Zs" or (unicodedata.bidirectional(char) in {"WB", "B", "S"}):
            if len(longest_word) < len(word):
                longest_word = word
            word = ""
            continue
        word += char

    return longest_word


print(get_longest_word('Python is simple and effective!'))
print(get_longest_word('Any pythonista like namespaces a lot.'))
