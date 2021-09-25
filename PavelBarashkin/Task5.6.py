# ### Task 4.6
# Implement a decorator `call_once` which runs a function or method once and caches the result.
# All consecutive calls to this function should return cached result no matter the arguments.

def call_once(func):
    cached_value = None

    def wrapper(a, b):
        nonlocal cached_value
        if cached_value:
            return cached_value
        cached_value = func(a, b)
        return cached_value

    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b


@call_once
def sum_of_numbers2(a, b):
    return a + b


print(sum_of_numbers(13, 42))
print(sum_of_numbers(999, 100))
print(sum_of_numbers(134, 412))
print(sum_of_numbers2(134, 412))
print(sum_of_numbers(856, 232))
print(sum_of_numbers2(13, 42))
