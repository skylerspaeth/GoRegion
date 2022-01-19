import string
import os
from decorate import Colors
ALLOWED_CHARS = set(string.digits + '.')

#validate address to prevent shell injection
def validate(address):
    if set(address) <= ALLOWED_CHARS:
        return True
    else:
        print(Colors.write("fail", "\n" + "*" * os.get_terminal_size().columns \
        + "WARNING: A non-digit/period character is contained in the SteamDB NetworkDatagramConfig.json file.\n" \
        + "Refusing to continue and the potentially dangerous address was never passed to a system call.\n" \
        + "*" * os.get_terminal_size().columns))
        raise Exception("Please check SteamDB's network tracking file to see if any incorrect characters are contained within the IP strings.")
