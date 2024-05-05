import argparse
from decimal import Decimal
import logging

from liquid_primes.pitches import generate_pitch_palette, get_max_range_n
from liquid_primes.export import filename, show_score_abjad, play_score_abjad_blocking
from liquid_primes.primes import primes, scale_with_ratio
from liquid_primes.score_abjad import create_blocks, make_staff, make_voice, make_score

ottava_ranges_abjad = {
    range(-39, -17): -2,
    range(-17, -5): -1,
    range(-5, 23): 0,
    range(23, 35): 1,
    range(35, 48): 2,
}

MIDI_PITCH_RANGE = (-39, 48)  # Piano range in Adjab terms
CENTRAL_A_ABJAD = 7  # in abjad, midi-pitch 69

TMP_DIR = "./tmp"

def main():
    args = handle_args()
    init_logger(args.log_level)
    logging.debug(f"{args}")

    # Setup
    max_pitch = MIDI_PITCH_RANGE[1]
    min_pitch = MIDI_PITCH_RANGE[0]
    reference_pitch = CENTRAL_A_ABJAD
    tempo: int = args.tempo
    scale_ratio_decimal = Decimal(args.scale_ratio).quantize(Decimal("0.01"))

    export_file_name = filename(min_pitch, max_pitch, reference_pitch)
    midi_file_path = f"{TMP_DIR}/{export_file_name}.midi"

    # Create rows
    prime_intervals = scale_with_ratio(
        primes(get_max_range_n(reference_pitch, min_pitch, max_pitch, scale_ratio_decimal)),
        scale_ratio_decimal
    )
    palette = generate_pitch_palette(
        reference_pitch, prime_intervals, min_pitch, max_pitch
    )
    logging.debug(f"Generated palette: {palette}")

    quantized = [round(Decimal(n).quantize(scale_ratio_decimal), 2) for n in palette]
    logging.debug(f"{quantized}")

    # Create score
    score = make_score(
        make_staff(
            make_voice(palette, ranges=ottava_ranges_abjad),
            tempo=tempo
        )
    )

    # Show score
    if args.show_score:
        show_score_abjad(score)

    # Playback
    if args.playback:
        play_score_abjad_blocking(create_blocks(score, with_midi=True), midi_file_path)


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Creates a collection of pitches, can export the score as PDF and play the score.')
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
