from liquid_primes.pitches import generate_pitch_palette
from liquid_primes.primes import primes
from liquid_primes.score import partition_notes_to_ranges, show_score

MIDI_PITCH_RANGE = (-39, 48)  # Piano range in Adjab terms
CENTRAL_A = 7  # in abjad, midi-pitch 69

ranges = {
    range(-39, -27): "15vb",
    range(-27, -15): "8vb",
    range(-15, 23): "ord",
    range(23, 49): "8va",
}


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

    partition = partition_notes_to_ranges(
        [
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
        ],
        ranges,
    )
    print(partition)
    print(palette)
    show_score(palette)


if __name__ == "__main__":
    main()
