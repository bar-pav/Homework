# ### Task 4.5
# Implement a function `get_digits(num: int) -> Tuple[int]` which returns a tuple
# of a given integer's digits.


def get_digits(num):
    result = []
    while num:
        result.append(num % 10)
        num //= 10
    return result[::-1]


print(get_digits(12345))
print(get_digits(87178291199))
