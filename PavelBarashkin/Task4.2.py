# ### Task 4.2
# Write a function that check whether a string is a palindrome or not. Usage of
# any reversing functions is prohibited. To check your implementation you can use
# strings from [here](https://en.wikipedia.org/wiki/Palindrome#Famous_palindromes).


def is_palindrome(string):
    alpha_string = "".join(char.lower() for char in string if (char.isalpha() or char.isdigit()))
    if len(alpha_string) <= 1:
        print("False")
        return
    for ind in range(len(alpha_string) // 2 + 1):
        if alpha_string[ind] != alpha_string[-ind - 1]:
            print("False")
            return
    print("True")


is_palindrome("Satire: Veritas")
is_palindrome("Dammit I'm Mad")
is_palindrome("ΝΙΨΟΝ ΑΝΟΜΗΜΑΤΑ ΜΗ ΜΟΝΑΝ ΟΨΙΝ")
is_palindrome("a")
is_palindrome("123 45543 2   1")
