import sys

# Detect platform
WINDOWS = sys.platform.startswith("win")

if WINDOWS:
    import msvcrt
else:
    import termios
    import tty


def get_key():
    if WINDOWS:
        key = msvcrt.getch()

        # Arrow / special keys (two bytes)
        if key == b'\xe0':
            key += msvcrt.getch()

        try:
            return key.decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            return ""

    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch1 = sys.stdin.read(1)

            if ch1 == "\x1b":
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
                return ch1 + ch2 + ch3

            return ch1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)