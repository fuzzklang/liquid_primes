import logging
from decimal import Decimal
from typing import Dict, List, Tuple


def _get_max_range_n(reference_pitch, min_pitch, max_pitch, scale_ratio=1.0) -> int:
    return int(max((max_pitch - reference_pitch) / scale_ratio, (reference_pitch - min_pitch) / scale_ratio))


def generate_pitch_palette(
    central_tone: int,
    intervals: List[int | float],
    cutoff_bot: float = float("-inf"),
    cutoff_top: float = float("inf"),
) -> List[int | float]:
    """
    Return a list of pitches.
    Constructed from the central tone and list of intervals (ints)
    """

    def _in_range(i: int | float):
        return cutoff_bot <= i and i <= cutoff_top

    positive_and_negative_intervals = [i * -1 for i in intervals[::-1]] + [0] + intervals
    logging.debug(f"{positive_and_negative_intervals=}")
    pitches = [i + central_tone for i in positive_and_negative_intervals]
    return [i for i in pitches if _in_range(i)]


def quantize_pitches(pitches: list[int | float], scale_ratio: float) -> list[float]:
    scale_ratio_decimal = Decimal(scale_ratio).quantize(Decimal("0.01"))
    return [float(Decimal(n).quantize(scale_ratio_decimal)) for n in pitches]


def _partition_notes_to_ranges(notes: List[int | float], ranges: Dict[range, int]):
    def previous_is_in_same_range(partition: List[Tuple[int, List[int | float]]], n: int | float) -> bool:
        if not partition or not partition[-1]:
            return False
        return partition[-1][0] == n

    partition: List[Tuple[int, List[int | float]]] = []
    for n in notes:
        for r in ranges:
            if int(n) in r:
                if previous_is_in_same_range(partition, ranges[r]):
                    partition[-1][1].append(n)
                else:
                    partition.append((ranges[r], [n]))
                continue
    return partition


def _get_partition_indices_and_ottava_n(pitches: List[int | float], ranges=Dict[range, int | float]):
    indices_and_ottava_n: List[Tuple[int, int]] = []
    idx = 0
    partitions = _partition_notes_to_ranges(pitches, ranges)
    for n, notes in partitions:
        indices_and_ottava_n.append((idx, n))
        idx += len(notes)
    return indices_and_ottava_n


def scale_with_ratio(intervals: list[int], ratio: float) -> list[float]:
    return [n * ratio for n in intervals]
