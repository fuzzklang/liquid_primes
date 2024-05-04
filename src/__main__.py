from liquid_primes.pitches import generate_pitch_palette
from liquid_primes.export import export_midi, filename, init_mixer, play_midi, show_score
from liquid_primes.primes import primes
from liquid_primes.score import create_blocks, make_staff, make_voice, make_score

ottava_ranges = {
    range(-39, -17): -2,
    range(-17, -5): -1,
    range(-5, 23): 0,
    range(23, 35): 1,
    range(35, 48): 2,
}

MIDI_PITCH_RANGE = (-39, 48)  # Piano range in Adjab terms
CENTRAL_A = 7  # in abjad, midi-pitch 69

TMP_DIR = "./tmp"


def main():
    max_pitch = MIDI_PITCH_RANGE[1]
    min_pitch = MIDI_PITCH_RANGE[0]
    reference_pitch = CENTRAL_A

    export_file_name = filename(min_pitch, max_pitch, reference_pitch)
    midi_file_path = f"{TMP_DIR}/{export_file_name}.midi"

    upto_prime_n = max(max_pitch - reference_pitch, reference_pitch - min_pitch)
    prime_intervals = primes(upto_prime_n)
    palette = generate_pitch_palette(
        reference_pitch, prime_intervals, min_pitch, max_pitch
    )
    voice = make_voice(palette, ranges=ottava_ranges)
    staff = make_staff(voice)
    score = make_score(staff)
    show_score(score)

    score_block = create_blocks(score, with_midi=True)
    is_success = export_midi(score_block, midi_file_path)
    if not is_success:
        SystemExit("Midi export failed")
    init_mixer()
    play_midi(midi_file_path)



if __name__ == "__main__":
    main()
