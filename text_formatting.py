import re

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

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


def strip_ansi(text: str) -> str:
    return ansi_escape.sub('', text)

def visible_length(text: str) -> int:
    return len(strip_ansi(text))

from ui import Alignment
def format_length(text: str, length: int, alignment: str = Alignment.CENTER) -> str:
    """function for formating text with ANSI escape sequences"""
    
    return f"{text:{alignment}{length + (len(text)-visible_length(text))}}"
