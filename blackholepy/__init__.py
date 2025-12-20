#       DEVELOPER NOTES
#   Ideas
#       - Make formulas for metrics universal -> any formula can be set -> automate properties from metrics' formulas 
#
#
#

from blackholepy.blackhole import BlackHole

_symbols = [BlackHole]
_constants = []

__all__ = [obj.__name__ for obj in _symbols].extend(_constants)

# ╭───────────────────────────────────────────────────────────────────────────────╮
# │                                     Config                                    │ 
# ╰───────────────────────────────────────────────────────────────────────────────╯

import warnings as _warnings
def warning(message, category, filename, lineno, file=None, line=None):
    print(
        f"\n\033[38;2;220;150;80mBlackHolePy Warning\n"
        f"╰─×\033[0m {message}\n"
    )

_warnings.showwarning = warning