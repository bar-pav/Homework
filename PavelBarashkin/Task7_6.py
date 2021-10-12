# ### Task 7.6
# Create console program for proving Goldbach's conjecture.
# Program accepts number for input and print result.
# For pressing 'q' program successfully close.
# Use function from Task 5.5 for validating input,
# handle all exceptions and print user friendly output.

import Task7_5 as iseven


def is_prime(p):
    for n in range(2, p):
        if p % n == 0:
            return False
    return True


def prove_goldbach_conjecture(n):
    for i in range(n - 1, n // 2 - 1, -1):
        if is_prime(i):
            for j in range(2, n):
                prime_sum = i + j
                if is_prime(j) and prime_sum == n:
                    print(f"Number {n} is prove goldbach's conjecture: {n} = {j} + {i}")
                    return
        else:
            continue
    print(f"Number {n} is disprove goldbach's conjecture. 80")


while True:
    input_str = input("Enter even number greater than 2 or 'q' for exit: ")
    if input_str.lower() == 'q':
        break
    try:
        number = int(input_str)
        iseven.is_even(number)
    except ValueError:
        print("Input must be integer")
    except Exception as e:
        print(e)
    else:
        prove_goldbach_conjecture(number)
