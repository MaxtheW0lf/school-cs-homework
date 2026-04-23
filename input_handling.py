import sys

# Detect platform
WINDOWS = sys.platform.startswith("win")

if WINDOWS:
    import msvcrt
else:
    import termios
    import tty


def get_key() -> str:
    if WINDOWS:
        key = msvcrt.getch()

        # Special keys (arrows, etc.)
        if key == b'\xe0':
            key2 = msvcrt.getch()
            combo = key + key2

            KEY_MAP = {
                b'\xe0H': 'UP',
                b'\xe0P': 'DOWN',
                b'\xe0K': 'LEFT',
                b'\xe0M': 'RIGHT',
            }

            return KEY_MAP.get(combo, 'SPECIAL')

        return key.decode(errors='ignore')

    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch1 = sys.stdin.read(1)

            if ch1 == "\x1b":
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)

                combo = ch1 + ch2 + ch3

                KEY_MAP = {
                    '\x1b[A': 'UP',
                    '\x1b[B': 'DOWN',
                    '\x1b[D': 'LEFT',
                    '\x1b[C': 'RIGHT',
                }

                return KEY_MAP.get(combo, 'SPECIAL')

            return ch1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)