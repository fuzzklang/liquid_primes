import abjad
from liquid_primes.pitches import generate_pitch_palette
from liquid_primes.primes import primes
from liquid_primes.score import (
    create_voice_with_ottava,
    show_score,
)

MIDI_PITCH_RANGE = (-39, 48)  # Piano range in Adjab terms
CENTRAL_A = 7  # in abjad, midi-pitch 69


test_palette = (
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
)


def test():
    string = "d'8 f' a' d'' f'' gs'4 r8 e' gs' b' e'' gs'' a'4"
    voice = abjad.Voice(string, name="RH_Voice")
    staff = abjad.Staff([voice], name="RH_Staff")
    score = abjad.Score([staff], name="Score")

    key_signature = abjad.KeySignature(
        abjad.NamedPitchClass("g"), abjad.Mode("major")
    )
    abjad.attach(key_signature, voice[0])

    time_signature = abjad.TimeSignature((2, 4), partial=abjad.Duration(1, 8))
    abjad.attach(time_signature, voice[0])

    ottava = abjad.Ottava(n=-2, site="after")
    abjad.attach(ottava, voice[1])

    ottava = abjad.Ottava(n=0, site="after")
    abjad.attach(ottava, voice[5])

    ottava = abjad.Ottava(n=1, site="after")
    abjad.attach(ottava, voice[8])

    articulation = abjad.Articulation("turn")
    abjad.attach(articulation, voice[5])

    abjad.show(score)


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
    # staff = create_voice_in_staff(palette)

    print(f"{palette}")
    voice = create_voice_with_ottava(palette)

    show_score(abjad.Staff([voice], name="default_staff"))

    # test()


if __name__ == "__main__":
    main()
