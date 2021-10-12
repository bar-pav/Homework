# ### Task 7.4
# Implement decorator for supressing exceptions.
# If exception not occure write log to console.

import io
import sys


def suppressing_exceptions(func):
    def wrapper(*args, **kwargs):
        stdout = sys.stdout
        buffer_out = io.StringIO()
        sys.stdout = buffer_out
        try:
            func(*args, **kwargs)
        except Exception:
            pass
        else:
            sys.stdout = stdout
            print(f"Function '{func.__name__}' completed without exceptions.")
            print("Function log: ")
            print(buffer_out.getvalue())
        finally:
            sys.stdout = stdout
    return wrapper


@suppressing_exceptions
def func_with_exception():
    print(2**10)
    print("Ended")
    raise AttributeError


@suppressing_exceptions
def func_without_exception():
    print(2**10)
    print("Ended")


func_with_exception()
func_without_exception()
