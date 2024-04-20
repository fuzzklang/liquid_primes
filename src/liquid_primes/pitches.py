from typing import Dict, List, Tuple


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


def partition_notes_to_ranges(notes: List[int], ranges: Dict[range, int]):
    def previous_is_in_same_range(
        partition: List[Tuple[int, List[int]]], n: int
    ) -> bool:
        if not partition or not partition[-1]:
            return False
        return partition[-1][0] == n

    partition: List[Tuple[int, List[int]]] = []
    for n in notes:
        for r in ranges:
            if n in r:
                if previous_is_in_same_range(partition, ranges[r]):
                    partition[-1][1].append(n)
                else:
                    partition.append((ranges[r], [n]))
                continue
    return partition


def get_partition_indices_and_ottava_n(
    pitches: List[int], ranges=Dict[range, int]
):
    indices_and_ottava_n: List[Tuple[int, int]] = []
    idx = 0
    partitions = partition_notes_to_ranges(pitches, ranges)
    for n, notes in partitions:
        indices_and_ottava_n.append((idx, n))
        idx += len(notes)
    return indices_and_ottava_n
