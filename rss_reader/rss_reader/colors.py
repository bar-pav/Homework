class Colors:
    DEFAULT = "\033[0m"
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    WHITE = '\033[38m'
    BG_BLUE = '\033[44m'
    WARNING = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\33[92m'
    FAIL = '\033[91m'


def print_exceptions(exception):
    print(f"{Colors.FAIL}{exception}{Colors.DEFAULT}")


def print_success(message):
    print(f"{Colors.GREEN}{message}{Colors.DEFAULT}")


def print_info(message):
    print(f"{Colors.BLUE}{message}{Colors.DEFAULT}")



