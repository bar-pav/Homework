# ### Task 4.4
# Implement a function `split_by_index(s: str, indexes: List[int]) -> List[str]`
# which splits the `s` string by indexes specified in `indexes`. Wrong indexes
# must be ignored.


def split_by_index(string, indexes):
    result = []
    start_index = 0
    for index in indexes:
        if index > len(string):
            continue
        result.append(string[start_index:index])
        start_index = index
    if start_index < len(string) or not result:
        result.append(string[start_index:len(string)])
    return result


print(split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18]))
print(split_by_index("pythoniscool,isn'tit?", [21, 42, 100]))
print(split_by_index("no luck", [42]))
print(split_by_index("no luck", [2, 42]))

