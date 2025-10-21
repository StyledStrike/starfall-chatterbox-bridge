from datetime import datetime
from colorama import Fore, Back, Style, just_fix_windows_console

just_fix_windows_console()

def padNumber(n):
    if (n > 9):
        return str(n)
    
    return "0" + str(n)

def getCurrentTimestamp(dateSep = "/", timeSep = ":"):
    dt = datetime.now()

    d = [
        padNumber(dt.day),
        padNumber(dt.month),
        padNumber(dt.year)
    ]

    t = [
        padNumber(dt.hour),
        padNumber(dt.minute),
        padNumber(dt.second)
    ]

    return dateSep.join(d) + " @ " + timeSep.join(t)

def debug(*values: object):
    print(Fore.CYAN + "[" + getCurrentTimestamp() + "]" + Style.RESET_ALL, *values)

def info(*values: object):
    print(Fore.LIGHTBLACK_EX + "[" + getCurrentTimestamp() + "]" + Style.RESET_ALL, *values)

def warn(*values: object):
    print(Fore.YELLOW + "[" + getCurrentTimestamp() + "]" + Style.RESET_ALL, *values)

def success(*values: object):
    print(Fore.GREEN + "[" + getCurrentTimestamp() + "]" + Style.RESET_ALL, *values)

def error(*values: object):
    print(Fore.RED + "[" + getCurrentTimestamp() + "]" + Style.RESET_ALL, *values)

def highlight(text: str):
    return Fore.GREEN + text + Style.RESET_ALL
