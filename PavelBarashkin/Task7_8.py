# ### Task 7.8
# Implement your custom iterator class called MySquareIterator which gives squares
# of elements of collection it iterates through.


class MySquareIterator:
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.collection):
            self.index = 0
            raise StopIteration
        next_element = self.collection[self.index] ** 2
        self.index += 1
        return next_element


m = MySquareIterator([1, 2, 3, 4, 5])

for i in m:
    print(i)

for i in m:
    print(i)
