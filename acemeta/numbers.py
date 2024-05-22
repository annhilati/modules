def isPrime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def factorial(n: int) -> int:
    out: int = 1
    for i in range(1, n + 1):
        out *= i
    return out