# ### Task 7.2
# Implement context manager for opening and working with file,
# including handling exceptions with @contextmanager decorator.

from contextlib import contextmanager


@contextmanager
def file_context(filename, mode):
    file = None
    try:
        file = open(filename, mode)
    except (FileNotFoundError, ValueError) as e:
        print("Exception occurred while open file: ", e)
        try:
            yield e
        except (AttributeError, Exception):
            pass
    else:
        print(f"File '{filename}' open for work ...")
        try:
            yield file
        except (AttributeError, TypeError, Exception) as e:
            print("Exception occurred while working with file: ", e)
    if file:
        file.close()
        print("File closed")


with file_context("Task7.2_output.txt", 'w') as f:
    f.write("file_context test string")
    raise Exception("Some exception")
