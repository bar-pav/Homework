# ## Task 4.7
# Implement a function `foo(List[int]) -> List[int]` which, given a list of
# integers, return a new list such that each element at index `i` of the new list
# is the product of all the numbers in the original array except the one at `i`.


def foo(lst):
    result = []
    for list_ in map(lambda ind: [num for index, num in enumerate(lst) if index != ind], range(len(lst))):
        prod = 1
        for number in list_:
            prod *= number
        result.append(prod)
    return result


print(foo([1, 2, 3, 4, 5]))
print(foo([3, 2, 1]))
print(foo([1, 6, 3, 0, 2]))
