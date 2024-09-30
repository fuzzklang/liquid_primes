from typing import Generator
import sympy

from sympy.ntheory.generate import nextprime


def to_nth_prime(n: int) -> list[int]:
    """Return a list of primes from 2 to the nth prime"""
    return list(sympy.primerange(sympy.prime(n) + 1))


def primes(n: int) -> list[int]:
    """Return a list of the primes up to n"""
    return list(sympy.sieve.primerange(n))


def prime_gen(start: int = 0) -> Generator[int, None, None]:
    next_prime = start
    while next_prime := nextprime(n=next_prime, ith=1):
        yield next_prime
