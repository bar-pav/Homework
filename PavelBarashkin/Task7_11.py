# ### Task 7.11
# Implement a generator which will geterate
# [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number)
# endlessly.

from time import sleep


def endless_fib_generator():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b
        sleep(0.5)


gen = endless_fib_generator()

while True:
    print(next(gen))
