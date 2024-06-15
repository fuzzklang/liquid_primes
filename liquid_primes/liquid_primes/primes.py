from typing import List
from sympy.ntheory.generate import primerange, prime


def to_nth_prime(n: int) -> List[int]:
    """Return a list of primes from 2 to the nth prime"""
    return list(primerange(prime(n) + 1))


def primes(n: int):
    """Return a list of the primes up to n"""
    return list(primerange(n))


def scale_with_ratio(intervals: list[int], ratio: float) -> list[float]:
    return [n * ratio for n in intervals]