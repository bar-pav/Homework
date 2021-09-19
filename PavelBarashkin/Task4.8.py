# ### Task 4.8
# Implement a function `get_pairs(lst: List) -> List[Tuple]` which returns a list
# of tuples containing pairs of elements. Pairs should be formed as in the
# example. If there is only one element in the list return `None` instead.


def get_pairs(lst):
    if len(lst) < 2:
        return None
    else:
        return [tuple(lst[i:i + 2]) for i in range(len(lst)) if len(lst[i:i + 2]) == 2]


print(get_pairs([1, 2, 3, 8, 9]))
print(get_pairs(['need', 'to', 'sleep', 'more']))
print(get_pairs([1]))
