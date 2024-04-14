from pitches import generate_pitch_palette
from primes import primes

MIDI_PITCH_RANGE = (21, 108)  # Piano range
CENTRAL_A = 69


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


if __name__ == "__main__":
    main()
