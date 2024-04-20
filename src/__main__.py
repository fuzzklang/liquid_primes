from liquid_primes.pitches import generate_pitch_palette
from liquid_primes.primes import primes
from liquid_primes.score import (
    make_staff,
    make_voice,
    show_score,
)

ottava_ranges = {
    range(-39, -17): -2,
    range(-17, -5): -1,
    range(-5, 23): 0,
    range(23, 35): 1,
    range(35, 48): 2,
}

MIDI_PITCH_RANGE = (-39, 48)  # Piano range in Adjab terms
CENTRAL_A = 7  # in abjad, midi-pitch 69


def main():
    max_pitch = MIDI_PITCH_RANGE[1]
    min_pitch = MIDI_PITCH_RANGE[0]
    reference_pitch = CENTRAL_A

    upto_prime_n = max(
        max_pitch - reference_pitch, reference_pitch - min_pitch
    )
    prime_intervals = primes(upto_prime_n)
    palette = generate_pitch_palette(
        reference_pitch, prime_intervals, min_pitch, max_pitch
    )

    staff = make_staff(make_voice(palette, ranges=ottava_ranges))

    show_score(staff)


if __name__ == "__main__":
    main()
