from typing import List

from sympy.ntheory.generate import prime, primerange


def to_nth_prime(n: int) -> List[int]:
    """Return a list of primes from 2 to the nth prime"""
    return list(primerange(prime(n) + 1))


def primes(n: int):
    """Return a list of the primes up to n"""
    return list(primerange(n))
