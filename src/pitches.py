from typing import List


def generate_pitch_palette(
    central_tone: int,
    intervals: List[int],
    cutoff_bot: float = float("-inf"),
    cutoff_top: float = float("inf"),
) -> List[int]:
    """
    Return a list of pitches.
    Constructed from the central tone and list of intervals (ints)
    """

    def in_range(i: int):
        return cutoff_bot <= i and i <= cutoff_top

    positive_and_negative_intervals = (
        [i * -1 for i in intervals[::-1]] + [0] + intervals
    )
    pitches = [i + central_tone for i in positive_and_negative_intervals]
    return [i for i in pitches if in_range(i)]
