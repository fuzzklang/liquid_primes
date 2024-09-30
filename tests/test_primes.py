from liquid_primes.palette.primes import primes, to_nth_prime, prime_gen


def test_primes_returns_primes():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    result = primes(30)
    assert result == expected


def test_to_nth_prime_generator():
    expected = [2, 3, 5, 7, 11, 13, 17, 19]
    result = to_nth_prime(8)
    assert result == expected


def test_prime_generator():
    gen = prime_gen(0)
    first_prime = next(gen)
    expected = 2
    assert first_prime == expected
    second_prime = 3
    assert next(gen) == second_prime
    third_prime = 5
    assert next(gen) == third_prime


def test_prime_generator_larger_range():
    gen = prime_gen(10)
    next_prime = next(gen)
    expected = 11
    assert next_prime == expected
    next_prime = 13
    assert next(gen) == next_prime
    next_prime = 17
    assert next(gen) == next_prime
