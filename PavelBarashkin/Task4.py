# Task 1.3
# Create a program that asks the user for a number and then prints out a list of all the [divisors]
# (https://en.wikipedia.org/wiki/Divisor) of that number.

def find_divisors(number):
    divisors = []
    for i in range(1, number // 2 + 1):
        if number % i == 0:
            divisors.append(i)
    divisors.append(number)
    print(divisors)


find_divisors(60)
