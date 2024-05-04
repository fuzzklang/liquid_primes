import argparse
from decimal import Decimal
import logging

from liquid_primes.pitches import generate_pitch_palette
from liquid_primes.export import export_midi, filename, init_mixer, play_midi, show_score
from liquid_primes.primes import primes, scale_with_ratio
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
    args = handle_args()
    init_logger(args.log_level)
    logging.debug(f"{args}")

    max_pitch = MIDI_PITCH_RANGE[1]
    min_pitch = MIDI_PITCH_RANGE[0]
    reference_pitch = CENTRAL_A
    tempo: int = args.tempo
    scale_ratio = args.scale_ratio
    scale_ratio_decimal = Decimal(scale_ratio).quantize(Decimal("0.01"))

    export_file_name = filename(min_pitch, max_pitch, reference_pitch)
    midi_file_path = f"{TMP_DIR}/{export_file_name}.midi"

    upto_prime_n = int(max((max_pitch - reference_pitch)/scale_ratio_decimal, (reference_pitch - min_pitch)/scale_ratio_decimal))
    prime_intervals = scale_with_ratio(primes(upto_prime_n), scale_ratio_decimal)
    palette = generate_pitch_palette(
        reference_pitch, prime_intervals, min_pitch, max_pitch
    )
    logging.debug(f"Generated palette: {palette}")

    quantized = [round(Decimal(n).quantize(scale_ratio_decimal), 2) for n in palette]
    logging.debug(f"{quantized}")

    voice = make_voice(palette, ranges=ottava_ranges)
    staff = make_staff(voice, tempo=tempo)
    score = make_score(staff)

    if args.show_score:
        show_score(score)

    if args.playback:
        score_block = create_blocks(score, with_midi=True)
        is_success = export_midi(score_block, midi_file_path)
        if not is_success:
            Exception("Midi export failed")
        init_mixer()
        play_midi(midi_file_path)


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Creates a collection of pitches, exports the score PDF and plays them')
    parser.add_argument('-p', metavar='--play', dest="playback", type=bool, action=argparse.BooleanOptionalAction,
                        help='play the score as midi')
    parser.add_argument('-s', metavar="--show", dest='show_score', type=bool, action=argparse.BooleanOptionalAction,
                        help='show the score as PDF')
    parser.add_argument('-t', metavar="--tempo", dest='tempo', type=int, nargs="?", default=800,
                        help='tempo (int) for score and playback')
    parser.add_argument('-r', metavar="--ratio", dest='scale_ratio', type=float, nargs="?", default=1,
                        help='ratio for scaling step. 0.5 yields quarter tones; 2 doubles step')
    parser.add_argument('--log-level', dest='log_level', type=str, default="INFO",
                        help='set log level')

    return parser.parse_args()


def init_logger(level: str):
    valid_levels = {
        "DEBUG":logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL}
    if level not in valid_levels.keys():
        raise SystemExit(f"Unknown log level: {level}. Should be on of {valid_levels}")
    logging.basicConfig(encoding="utf-8", level=level)


if __name__ == "__main__":
    main()
