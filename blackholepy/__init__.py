from blackholepy.blackhole import BlackHole

_symbols = [BlackHole]
_constants = []

__all__ = [obj.__name__ for obj in _symbols].extend(_constants)

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                     Config                                    │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

import warnings as _warnings
def warning(message, category, filename, lineno, file=None, line=None):
    print(f"{filename}\n  BlackHolePy: {message}")

_warnings.showwarning = warning