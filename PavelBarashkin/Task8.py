# Task 1.6
# Write a program which makes a pretty print of a part of the multiplication table.

def multiplication_table(a=1, b=9, c=1, d=9):
    width = len(str(b * d)) + 5
    template = "{: >" + str(width) + "}"
    print("", "".join([template.format(i) for i in range(c, d + 1)]))
    for row in range(a, b + 1):
        print(str(row) + "".join([template.format(row * col) for col in range(c, d + 1)]))


multiplication_table(222, 229, 3122, 3130)
