from typing import Callable, Dict, List, Tuple
import abjad


def show_score(pitches: List[int]) -> None:
    notes = [abjad.NamedPitch(n) for n in pitches]
    if not notes:
        return
    note_string = notes[0].name + "1"
    note_string += " ".join([n.name for n in notes[1:]]) + "1"
    # string = "c'16 f' g' a' d' g' a' b' e' a' b' c'' f' b' c'' d''16"
    voice_1 = abjad.Voice(note_string, name="Voice_1")
    staff_1 = abjad.Staff([voice_1], name="Staff_1")
    abjad.show(staff_1)


def in_range_cmp(a: int, b: int) -> Callable[[int], bool]:
    def f(x: int):
        return a <= x and x < b

    return f


def previous_is_in_same_range(
    partition: List[Tuple[str, List[str]]], key: str
) -> bool:
    if not partition:
        return False
    return partition[-1][0] == key


def partition_notes_to_ranges(
    notes: List[int], ranges: Dict[range, str]
) -> List[Tuple[str, List[str]]]:
    partition: List[Tuple[str, List[str]]] = []
    for n in notes:
        for r in ranges:
            if n in r:
                if previous_is_in_same_range(partition, ranges[r]):
                    partition[-1][1].append(str(n))
                else:
                    partition.append((ranges[r], [str(n)]))
                continue
    return partition
