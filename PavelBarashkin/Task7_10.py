# ### Task 7.10
# Implement a generator which will generate odd numbers endlessly.

from time import sleep


def endless_odd_generator():
    start = 1
    while True:
        yield start
        start += 2
        sleep(0.5)


gen = endless_odd_generator()

while True:
    print(next(gen))
