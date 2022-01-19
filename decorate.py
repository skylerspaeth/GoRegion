class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    #COLOR REFERENCE:
    #cyan is for setup/anything before the process of blocking addresses, blue is for anything after, and green is final success.

    @classmethod
    def write(cls, color, text):
        return getattr(cls, color.upper()) + text + cls.ENDC
