# ### Task 7.1
# Implement class-based context manager for opening and working with file,
# including handling exceptions. Do not use 'with open()'.
# Pass filename and mode via constructor.

class FileContext:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = None
        try:
            self.file = open(self.filename, self.mode)
        except (FileNotFoundError, ValueError) as e:
            print("Exception occurred while open file: ", e)
        else:
            print(f"File '{self.filename}' open for work ...")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            if exc_type:
                print("Exception occurred while working with file: ", exc_val)
            else:
                print("No exceptions while working with file.")
            self.file.close()
            print("File closed")
        return True


with FileContext("Task7.1_output.txt", 'w') as f:
    f.write("FileContext test string")
    raise Exception("Some error in context")
