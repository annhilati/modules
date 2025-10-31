from ametrine.library.rational import rational

def gregorys_series(x: rational, i: int) -> rational:
    x = 0
    for k in range(0, i):
        x += (rational(-1) ** k) * ((x ** 2) * k + rational(1)) / (2 * k + 1)
    return 4 * x