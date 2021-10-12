# ### Task 7.3
# Implement decorator with context manager support for
# writing execution time to log-file. See contextlib module.


from time import time, sleep


class ContextExecLogger:
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        self.start = time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exec_time = time() - self.start
        file = open("Task7.3_log.log", "a")
        file.write("{}: {:0.7f}".format(self.func.__name__, self.exec_time) + " sec" + "\n")
        file.close()


def context_exec_logger(func):
    def wrapper(*args, **kwargs):
        with ContextExecLogger(func):
            func(*args, **kwargs)
    return wrapper


@context_exec_logger
def sleep_function():
    sleep(1)


@context_exec_logger
def pow_function():
    print(2**10000)


sleep_function()
pow_function()
