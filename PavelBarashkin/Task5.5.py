# ## Task 4.5
# Implement a decorator `remember_result` which remembers last result of function it decorates
# and prints it before next call.


def remember_result(func):
    last_result = None

    def wrapper(*args):
        nonlocal last_result
        print(f"Last result = '{last_result}'")
        last_result = func(*args)
    return wrapper


@remember_result
def sum_list(*args):
    if not len(args):
        print(f"Current result = 'None'")
        return None
    result = args[0]
    for item in args[1:]:
        result += item
    print(f"Current result = '{result}'")
    return result


sum_list('1', '2')
sum_list('a', 'b')
sum_list(1, 2, 3)
sum_list(2)
sum_list('a')
sum_list()
sum_list('abc', 'def')

