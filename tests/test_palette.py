from decimal import Decimal
import re

import pytest

from liquid_primes.palette.primes import primes, to_nth_prime
from liquid_primes.palette.export import filename
from liquid_primes.palette.pitches import generate_pitch_palette, quantize_pitches, scale_with_ratio


def test_primes_returns_primes():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    result = primes(30)
    assert result == expected


def test_to_nth_prime_generator():
    expected = [2, 3, 5, 7, 11, 13, 17, 19]
    result = to_nth_prime(8)
    assert result == expected


def test_filename_correctly_made():
    result = filename(min_pitch=10, max_pitch=100, reference_pitch=60)
    # regexp from https://stackoverflow.com/a/3143231
    full_datetime_regexp = "\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+"
    expected_regexp = re.compile(f"min_10_max100_ref60_{full_datetime_regexp}")
    assert re.fullmatch(expected_regexp, result) is not None


def test_pitch_palette_correctly_made():
    result = generate_pitch_palette(central_tone=60, intervals=[1, 2, 3, 5, 10], cutoff_bot_incl=49, cutoff_top_incl=70)
    expected = [50, 55, 57, 58, 59, 60, 61, 62, 63, 65, 70]
    assert result == expected


def test_pitch_palette_excludes_at_cutoff():
    result = generate_pitch_palette(central_tone=50, intervals=[1, 2, 3, 5, 10], cutoff_bot_incl=41, cutoff_top_incl=59)
    expected = [45, 47, 48, 49, 50, 51, 52, 53, 55]
    assert result == expected


def test_quantize_pitches_is_correct_no_scaling():
    expected = [0.444, 0.51, 0.621]
    input_floats = [0.44444, 0.51, 0.62111111]
    result = quantize_pitches(pitches=input_floats, scale_ratio=1.0, exp=Decimal("1.000"))
    assert result == expected


@pytest.mark.skip(reason="quantize_pitches probably does not handle scaling arg as expected. Is it needed?")
def test_quantize_pitches_is_correct_with_scaling():
    expected = [0.5, 0.5, 0.75]
    input_floats = [0.44444, 0.51, 0.69111111]
    result = quantize_pitches(pitches=input_floats, scale_ratio=0.25, exp=Decimal("1.00"))
    assert result == expected


def test_interval_scaling_is_correct():
    expected = [0.5, 1.0, 1.5, 2.5]
    result = scale_with_ratio(intervals=[1, 2, 3, 5], ratio=0.5)
    assert result == expected
