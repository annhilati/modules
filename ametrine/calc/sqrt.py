from math import isqrt, gcd

def simplify_sqrt_div(n, denom):
        """Vereinfacht sqrt(n)/denom zu k*sqrt(r)/d"""
        k = 1
        for i in range(2, isqrt(n)+1):
            while n % (i*i) == 0:
                n //= i*i
                k *= i
        g = gcd(k, denom)
        k //= g
        denom //= g
        return k, n, denom