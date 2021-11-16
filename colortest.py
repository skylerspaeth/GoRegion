class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def write(cls, color, text):
        return getattr(cls, color.upper(), getattr(cls, "WARNING")) + text + cls.ENDC

print(colors.write("green", "Green text here"))
