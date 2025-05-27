import enum
from types import MappingProxyType

# Fast membership test for the obvious immutable built-ins
_IMMUTABLE_PRIMITIVES = (
    int, float, complex, bool, str, bytes,
    tuple, frozenset, range, type(None),  # NoneType
    enum.Enum,                            # every Enum subclass instance is immutable
)

def is_mutable(obj) -> bool:
    """
    # Chat made
    # not important thing, just a helper——tries to check to see if something is mutable
    # to prevent the user from misusing Item() comparisons (errs on the side of mutable)
    Best-effort heuristic that returns True if *obj* is *probably* mutable.

    The function never mutates *obj*; it only inspects its public interface
    and class metadata.
    """
    # 1. Cheap positives – primitives & enums
    if isinstance(obj, _IMMUTABLE_PRIMITIVES):
        return False

    # NamedTuple subclasses behave like tuples (immutable)
    if isinstance(obj, tuple) and getattr(obj.__class__, "_fields", None):
        return False

    # MappingProxyType is an immutable dict wrapper
    if isinstance(obj, MappingProxyType):
        return False

    # 2. Supports item assignment?  That’s a strong signal of mutability
    if hasattr(obj, "__setitem__"):
        return True

    # 3. A class that *explicitly* blocks new attributes via empty __slots__
    if getattr(obj.__class__, "__slots__", None) == ():
        return False

    # 4. Fallback – we assume mutability to stay on the safe side
    return True


# Everything above (including imports) is for isMutable, for userComparable (not even very important, just a possibly helpful check)
# These are some dumb constants I made for userComparable:

CONFIRMATIONS = {'y', 'yes', 'yeah', 'ye', 'yah', 'yay', 'yep', 'yup', 'yeh',
                 'affirmative', 'totally', 'sure', 'you know it', 'you bet',
                 'for sure', 'you betcha', 'aye', 'roger', 'absolutely', 'mhm'
                 'definitely', 'of course', 'si', 'sí', 'sì', 'oui', 'ja', 'da',
                 'sim', 'hai', 'shi', '👍', '👌', '✅', 'i think overdid it...'}
TO_STRIP = ' \t\n\r\x0b\x0c.!?-_–—–()[]{}\\|/`~"\':;,<>#$%^&*@'  # might as well

# Below is for also for the user input stuff, like the constants:


def getch():
    """
    Read a single keypress from stdin, without waiting for Enter.
    Works on Windows and POSIX (Linux/macOS).
    Returns:
        A one-character string.
    """
    try:
        # Windows
        import msvcrt
        ch = msvcrt.getch()
        if ch == b'\x03':            # Ctrl-C
            raise KeyboardInterrupt
        # msvcrt.getch() returns a bytes object; decode to string
        return ch.decode('utf-8', errors='ignore')
    except ImportError:
        # POSIX (Linux / macOS)
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)   # read exactly one character
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        if ch == '\x1b':
            print(end="\ngetching thrice to try to avoid arrow key messing everything up,"
            "\n(hopefully only next input will count, but could be 2nd or 3rd if something is weird)\ntry again: ", flush=True)
            getch()
            getch()
            return getch()
        return ch


if __name__ == "__main__":
    print("Press y or n: ", end="", flush=True)
    c = getch()
    print([c])  # prints the character immediately, without needing Enter
