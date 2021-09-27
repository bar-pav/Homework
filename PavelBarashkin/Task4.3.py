# ### Task 4.3
# Implement a function which works the same as `str.split` method
# (without using `str.split` itself, ofcourse).

def split_imitate(string, separator=None, maxsplit=-1):
    result = []
    start_index = 0
    if separator is None:
        count = 0
        for index, char in enumerate(string):
            if maxsplit >= 0 and len(result) == (maxsplit + 1):
                return result
            if char.isspace():
                start_index = index + 1
                if count != 0:
                    result.append(string[index - count:index])
                count = 0
            else:
                count += 1
        if start_index < len(string):
            result.append(string[start_index:])

    elif len(separator) == 1:
        for index, char in enumerate(string):
            if maxsplit >= 0 and len(result) == (maxsplit + 1):
                return result
            if char == separator:
                result.append(string[start_index:index])
                start_index = index + 1
        if start_index < len(string):
            result.append(string[start_index:])

    else:
        for index, char in enumerate(string):
            if maxsplit >= 0 and len(result) == (maxsplit + 1):
                return result
            if string[index:index + len(separator)] == separator:
                result.append(string[start_index:index])
                start_index = index + len(separator)
        if start_index < len(string):
            result.append(string[start_index:])
    return result


print(split_imitate(" \t     12,  2    \n  33  ,     234,33     "))
print(split_imitate("        12,  2        33  ,     234,33     ", maxsplit=1))
print(split_imitate("        12,  2        33  ,     234,33     ", maxsplit=10))
print(split_imitate(""))

print(split_imitate(",1,2,3,4,,5  ,6,6,,", ","))
print(split_imitate("", ","))

print(split_imitate("><>1<>2<<.><>3<>4<>5<>6<>", '<>'))
print(split_imitate("><>1<>2<<.><>3<>4<>5<>6<.>", '<.>'))
print(split_imitate("", '<>'))
