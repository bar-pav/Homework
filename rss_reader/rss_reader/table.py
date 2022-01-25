import textwrap

columns = 2
table_max_width = 98
col_separator = ' | '
col1_width = 0
col2_width = 0
colored = False


def get_max_column_width(col=None):
    global col1_width, col2_width
    col1_width = max(len(cell) for cell in col)
    col2_width = table_max_width - col1_width - len(col_separator)


def get_number_of_lines(text):
    return len(text) // col2_width + 1


def print_horizontal_row_separator():
    print(" " * col1_width, end=col_separator)
    print('-' * (table_max_width - col1_width - len(col_separator)), end=col_separator + '\n')


def print_horizontal_border():
    print('-' * table_max_width)


def style(text, colored=False):
    return "\033[32m" + text + "\033[0m" if colored else text


def print_header(text):
    print(' ' + '-' * (table_max_width - 2) + ' ')
    print('|' + ('\033[1;38;46m' if colored else '') + f'{text:^{table_max_width}}' + ('\033[0m' if colored else '') + '|')
    print(' ' + '-' * (table_max_width - 2) + ' ')


def print_row(col1, col2):
    col2_lines = col2.split('\n')
    lines = []
    for line in col2_lines:
        if line.isspace():
            continue
        if len(line) > col2_width:
            line = textwrap.wrap(line, col2_width)
            lines.extend(line)
        else:
            lines.append(line)
    col2 = lines
    for line, txt in enumerate(col2):
        col1_line = col1[line * col1_width: line * col1_width + col1_width]
        print(style(col1_line.ljust(col1_width, " "), colored), end=col_separator)
        print(txt.ljust(col2_width, " "), end=col_separator + "\n")
