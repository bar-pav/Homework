# ### Task 4.2
# Implement a function which search for most common words in the file.
# Use `data/lorem_ipsum.txt` file as a example.
# > NOTE: Remember about dots, commas, capital letters etc.


def most_common_words(filepath, number_of_words=3):
    file = open(filepath, 'r')
    word_frequency = {}
    for line in file:
        if not line.isspace():
            for word in line.split():
                if word[-1].isalpha():
                    word_frequency[word.lower()] = word_frequency.get(word.lower(), 0) + 1
                else:
                    word_frequency[word[:-1].lower()] = word_frequency.get(word.lower(), 0) + 1
    print([word_count[0] for word_count in sorted(word_frequency.items(), key=lambda items: (-items[1], items[0]))][:number_of_words])


most_common_words("../data/lorem_ipsum.txt")
