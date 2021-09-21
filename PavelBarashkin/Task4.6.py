# ### Task 4.6
# Implement a function `get_shortest_word(s: str) -> str` which returns the
# longest word in the given string. The word can contain any symbols except
# whitespaces (` `, `\n`, `\t` and so on). If there are multiple longest words in
# the string with a same length return the word that occures first.


def get_longest_word(string):
    words = []
    word = ''
    for char in string:
        if not char.isspace():
            word += char
        elif word:
            words.append(word)
            word = ''
    if word:
        words.append(word)
    return max(words, key=len)


print(get_longest_word('Python is simple and effective!'))
print(get_longest_word('Any pythonista like namespaces a lot.'))
