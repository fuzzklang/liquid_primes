import abjad

from liquid_primes.score_abjad import make_voice, show_score


test_palette = [
    -39,
    -29,
    -25,
    -16,
    -14,
    -10,
    -5,
    0,
    1,
    2,
    3,
    -39,
    4,
    5,
    6,
    7,
    8,
    9,
    12,
    19,
    23,
    24,
    40,
    48,
]

ottava_ranges = {
    range(-39, -17): -2,
    range(-17, -5): -1,
    range(-5, 23): 0,
    range(23, 35): 1,
    range(35, 48): 2,
}


def test_create_voice():
    voice = make_voice(test_palette)
    show_score(abjad.Score([voice], name="Default staff"))


def test_create_voice_with_ottava():
    voice = make_voice(test_palette, ranges=ottava_ranges)
    show_score(abjad.Score([voice], name="Default staff"))
