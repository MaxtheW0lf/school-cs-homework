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
