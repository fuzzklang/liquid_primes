from liquid_primes.score import to_voice, to_part, to_score
from liquid_primes.export import show_score


test_palette = [
    21,
    31,
    35,
    44,
    46,
    50,
    55,
    60,
    61,
    62,
    63,
    21,
    64,
    65,
    66,
    67,
    68,
    69,
    72,
    79,
    83,
    84,
    100,
    108,
]

ottava_ranges = {
    range(21, 42): -2,
    range(43, 54): -1,
    range(55, 82): 0,
    range(83, 94): 1,
    range(95, 108): 2,
}

def test_create_voice():
    voice = to_voice(test_palette)
    score = to_score(to_part(voice))
    show_score(score)