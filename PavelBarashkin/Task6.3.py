# ### Task 4.3
# Implement The Keyword encoding and decoding for latin alphabet.
# The Keyword Cipher uses a Keyword to rearrange the letters in the alphabet.
# Add the provided keyword at the begining of the alphabet.
# A keyword is used as the key, and it determines the letter matchings of the cipher alphabet to the plain alphabet.
# Repeats of letters in the word are removed, then the cipher alphabet is generated with the keyword matching to A, B, C etc. until the keyword is used up, whereupon the rest of the ciphertext letters are used in alphabetical order, excluding those already used in the key.
#
# <em> Encryption:
# Keyword is "Crypto"

class Cipher:
    def __init__(self, keyword):
        self.alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.encode_alphabet = {}
        self.unique_char_count = 0
        for char in keyword:
            try:
                self.alphabet.remove(char.upper())
            except ValueError:
                continue
            self.encode_alphabet[chr(65 + self.unique_char_count)] = char.upper()
            self.unique_char_count += 1
        for i, c in enumerate(self.alphabet):
            self.encode_alphabet[chr(65 + self.unique_char_count + i)] = c
        for key, value in self.encode_alphabet.copy().items():
            self.encode_alphabet[key.lower()] = value.lower()
        self.decode_alphabet = {value: key for key, value in self.encode_alphabet.items()}

    def encode(self, string):
        print(f"{string}: ", "".join(self.encode_alphabet.get(c, c) for c in string))

    def decode(self, string):
        print(f"{string}: ", "".join(self.decode_alphabet.get(c, c) for c in string))


cipher = Cipher('cryyppto')
cipher.encode('Hello world')
cipher.decode('Btggj vjmgp')
cipher.decode('Fjedhc dn atidsn')
cipher.decode('')
