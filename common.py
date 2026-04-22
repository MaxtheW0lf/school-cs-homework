def reset():
    print("\x1B[H", end="") # Move cursor to top-left

def clear():
    print("\033[2J\033[H", end="")

def cleanup():
    print("\033[0m", end="")  # reset styles
    print("\033[?1049l", end="") # restore main buffer
    print("\033[?25h", end="")  # show cursor again

def start():
    print("\033[?1049h" , end="") # switch to alternate buffer
    print("\033[?25l", end="") # hides cursor

BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
END = "\033[0m"

# 48 BG 38 text

def color(red: int = 0, green: int = 0, blue: int = 0, background: bool = False) -> str:
    return f"\x1b[{48 if background else 38};2;{red};{green};{blue}m"