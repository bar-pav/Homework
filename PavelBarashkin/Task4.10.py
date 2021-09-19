# ### Task 4.10
# Implement a function that takes a number as an argument and returns a dictionary, where the key is a number and the
# value is the square of that number.


def generate_squares(number):
    return {num: num ** 2 for num in range(1, number + 1)}


print(generate_squares(5))
