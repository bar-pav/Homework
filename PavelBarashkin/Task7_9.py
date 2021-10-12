# ### Task 7.9
# Implement an iterator class EvenRange, which accepts start and end of the interval
# as an init arguments and gives only even numbers during iteration.
# If user tries to iterate after it gave all possible numbers `Out of numbers!`
# should be printed.
# _Note: Do not use function `range()` at all_


class EvenRange:
    def __init__(self, start, end):
        self.start = start if start % 2 == 0 else (start - 1)
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 2
        if self.start > self.end:
            return "Out of numbers!"
        return self.start


er1 = EvenRange(7, 12)
print(next(er1))
print(next(er1))
print(next(er1))
print(next(er1))
er2 = EvenRange(3, 14)
for number in er2:
    print(number)







