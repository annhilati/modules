from blackholepy.blackhole import BlackHole
import blackholepy.config as config

_symbols = [BlackHole, config]
_constants = []

__all__ = [obj.__name__ for obj in _symbols].extend(_constants)

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                     Config                                    │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

import warnings as _warnings
def warning(message, category, filename, lineno, file=None, line=None):
    print(f"{filename}\n  BlackHolePy: {message}")

_warnings.showwarning = warning