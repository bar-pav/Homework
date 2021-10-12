# ### Task 7.7
# Implement your custom collection called MyNumberCollection.
# It should be able to contain only numbers. It should NOT inherit
# any other collections.
# If user tries to add a string or any non numerical object there,
# exception `TypeError` should be raised. Method init sholud be able
# to take either
# `start,end,step` arguments, where `start` - first number of
# collection, `end` - last number of collection or some ordered
# iterable
# collection (see the example).
# Implement following functionality:
# * appending new element to the end of collection
# * concatenating collections together using `+`
# * when element is addressed by index(using `[]`), user should get
# square of the addressed element.
# * when iterated using cycle `for`, elements should be given
# normally
# * user should be able to print whole collection as if it was list.

from collections.abc import Iterable


def instance(obj):
    return isinstance(obj, (int, float))


class MyNumberCollection:
    def __init__(self, start=None, end=None, step=1):
        if isinstance(start, Iterable):
            if isinstance(start, str):
                raise TypeError("'string' - object is not a number!")
            if all([*map(instance, start)]):
                self.col = [*start]
            else:
                raise TypeError("MyNumberCollection supports only numbers!")
        elif isinstance(start, (int, float)):
            if end:
                self.col = [*range(start, end + 1, step)]
            else:
                self.col = [start]
        else:
            self.col = []

    def append(self, num):
        if isinstance(num, (int, float)):
            self.col.append(num)
        else:
            raise TypeError(f"'{num}' object is not a number!")

    def __repr__(self):
        return str(self.col)

    def __add__(self, other):
        if isinstance(other, MyNumberCollection):
            return MyNumberCollection(self.col + other.col)
        else:
            raise TypeError(f"'{other}' object must be instance of MyNumberCollection")

    def __getitem__(self, item):
        return self.col[item] ** 2

    def __iter__(self):
        return iter(self.col)


col1 = MyNumberCollection(0, 5, 2)
print(col1)
col2 = MyNumberCollection((1, 2, 3, 4, 5))
print(col2)
# col3 = MyNumberCollection((1, 2, 3, "4", 5))
col1.append(7)
print(col1)
# col2.append("string")
print(col1 + col2)
print(col1)
print(col2)
print(col2[4])
for i in col1:
    print(i)
