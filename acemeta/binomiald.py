from acemeta.numbers import factorial

def binominalC(n: int, k: int) -> float:
    return factorial(n) / (factorial(k) * factorial(n - k))
def binominalD(n: int, k: int, p: float) -> float:
    return binominalC(n, k) * (p ** k) * ((1-p) ** (n - k))

def binomialDF(n: int, k: int, p: float, mode: str) -> float:

    def bdf_max(n: int, k_max: int, p: float) -> float:
        out: float = 0
        for i in range(0, k_max + 1):
            out = out + binominalD(n, i, p)
        return out
    
    match mode:
        case "exact":
            return binominalD(n, k, p)
        case "max":
            out: float = 0
            for i in range(0, k + 1):
                out = out + binominalD(n, i, p)
            return out
        case "min":
            return 1 - bdf_max(n, k - 1, p)
        case "morethen":
            return 1 - bdf_max(n, k, p)
        case "lessthen":
            return bdf_max(n, k - 1, p)
        case _:
            raise ValueError("mode must be one of \"exact\", \"max\", \"min\", \"morethen\" or \"lessthen\"") 