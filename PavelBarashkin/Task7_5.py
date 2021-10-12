# ### Task 7.5
# Implement function for check that number is even, at least 3.
# Throw different exceptions for this errors.
# Custom exceptions must be derived from custom base exception
# (not Base Exception class).


class EvenCheckBaseException(Exception):
    pass


class ToSmallNumber(EvenCheckBaseException):
    pass


class NumberIsNotEven(EvenCheckBaseException):
    pass


def is_even(number):
    if number < 3:
        raise ToSmallNumber("Number must be greater than or equal to 3.")
    elif number % 2 != 0:
        raise NumberIsNotEven(f"Number {number} is not even.")
    else:
        return True


if __name__ == "__main__":
    print(is_even(5))
