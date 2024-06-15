import argparse
import logging


from liquid_primes.pitches import generate_pitch_palette, get_max_range_n, quantize_pitches
from liquid_primes.export import export_to_musicxml, filename, show_score, play_score, write_to_stdout
from liquid_primes.primes import primes, scale_with_ratio
from liquid_primes.score import to_part, to_pitches, to_score, to_voice, with_duration
from liquid_primes.utils import read_nums_from_stdin

ottava_ranges = {
    range(21, 42): -2,
    range(43, 54): -1,
    range(55, 82): 0,
    range(83, 94): 1,
    range(95, 108): 2,
}

PITCH_RANGE_MIDI = (21, 108)
CENTRAL_A_MIDI = 69

TMP_DIR = "./tmp"

def main():
    args = handle_args()
    init_logger(args.log_level)
    logging.debug(f"{args}")

    # Setup
    max_pitch = PITCH_RANGE_MIDI[1]
    min_pitch = PITCH_RANGE_MIDI[0]
    reference_pitch = CENTRAL_A_MIDI
    scale_ratio = args.scale_ratio
    tempo: int = args.tempo

    if args.read_palette_from_stdin:
        palette = read_nums_from_stdin()
        xml_file_path = f"{TMP_DIR}/custom-{filename(palette[0], palette[-1], reference_pitch)}.musicxml"
    else:
        xml_file_path = f"{TMP_DIR}/{filename(min_pitch, max_pitch, reference_pitch)}.musicxml"
        # Get rows
        intervals = scale_with_ratio(
            intervals=(read_nums_from_stdin()
                    if args.read_intervals_from_stdin
                    else primes(get_max_range_n(reference_pitch, min_pitch, max_pitch, scale_ratio))),
            ratio=scale_ratio
        )

        logging.debug(f"{intervals=}")

        palette = quantize_pitches(generate_pitch_palette(
            reference_pitch, intervals, min_pitch, max_pitch
        ), scale_ratio)
        logging.debug(f"Generated palette: {palette}")

    if args.output_row_to_stdout:
        write_to_stdout(palette)

    # Create score
    notes = with_duration(pitches=to_pitches(palette), quarter_length=4)
    part = to_part(to_voice(notes), quarter_tempo=tempo)
    score = to_score(part)
    logging.debug(f"Generated score: {score}")

    if args.exportmusicxml:
        export_to_musicxml(score, xml_file_path)

    if args.show_score:
        show_score(score, fmt='text')

    if args.playback:
        play_score(score)


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Creates a collection of pitches, can export the score as PDF and play the score.')
    parser.add_argument('-p', metavar='--play', dest="playback", type=bool, action=argparse.BooleanOptionalAction,
                        help='play the score as midi')
    parser.add_argument('-x', metavar='--exportmusicxml', dest="exportmusicxml", type=bool, action=argparse.BooleanOptionalAction,
                        help='save file as music xml to tmp folder')
    parser.add_argument('-s', metavar="--show", dest='show_score', type=bool, action=argparse.BooleanOptionalAction,
                        help='show the score as PDF')
    parser.add_argument('-t', metavar="--tempo", dest='tempo', type=int, nargs="?", default=800,
                        help='tempo (int) for score and playback')
    parser.add_argument('-r', metavar="--ratio", dest='scale_ratio', type=float, nargs="?", default=1,
                        help='ratio for scaling step. 0.5 yields quarter tones; 2 doubles step')
    parser.add_argument('--intervals', dest='read_intervals_from_stdin', type=bool, action=argparse.BooleanOptionalAction, default=False,
                        help='read input intervals piped from stdin')
    parser.add_argument('-i', metavar="--pipe-palette", dest='read_palette_from_stdin', type=bool, action=argparse.BooleanOptionalAction, default=False,
                        help='read input palette piped from stdin')
    parser.add_argument('-o', metavar="--output-row", dest='output_row_to_stdout', type=bool, action=argparse.BooleanOptionalAction, default=False,
                        help='write generated row to stdout')
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
    if level.upper() not in valid_levels.keys():
        raise SystemExit(f"Unknown log level: {level}. Should be one of {valid_levels.keys}")
    logging.basicConfig(encoding="utf-8", level=level.upper())


if __name__ == "__main__":
    main()