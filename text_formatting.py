import re

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def strip_ansi(text: str) -> str:
    return ansi_escape.sub('', text)

def visible_length(text: str) -> int:
    return len(strip_ansi(text))
	
from ui import Alignment
def format_length(text: str, length: int, alignment: str = Alignment.CENTER) -> str:
	
    """function for formating text with ANSI escape sequences"""
    
    return f"{text:{alignment}{length + (len(text)-visible_length(text))}}"
