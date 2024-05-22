def isPrime(num: int) -> bool:
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def factorial(n: int) -> int:
    out: int = 1
    for i in range(1, n + 1):
        out *= i
    return out