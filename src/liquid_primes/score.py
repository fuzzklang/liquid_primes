from typing import Dict, List, Tuple
import abjad


def show_score(staff: abjad.Staff) -> None:
    abjad.show(staff)


ranges = {
    range(-39, -17): -2,
    range(-17, -5): -1,
    range(-5, 23): 0,
    range(23, 35): 1,
    range(35, 48): 2,
}


def previous_is_in_same_range(
    partition: List[Tuple[int, List[int]]], key: int
) -> bool:
    if not partition:
        return False
    return partition[-1][0] == key


def partition_notes_to_ranges(
    notes: List[int], ranges: Dict[range, int]
) -> List[Tuple[int, List[int]]]:
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


def create_voice_in_staff(
    pitches: List[int],
    voice_name: str = "Default voice",
    staff_name: str = "Default staff",
    durations: List[int] | None = None,
) -> abjad.Staff:
    if not pitches:
        return abjad.Staff([], name=staff_name)
    if durations is None:
        durations = [1]
    duration_str = f"{str(durations[0])}"
    notes = [abjad.NamedPitch(n) for n in pitches]
    voice_str = make_voice_string(notes, duration_str)
    voice = abjad.Voice(voice_str, name=voice_name)
    staff = abjad.Staff([voice], name=staff_name)
    return staff


def make_voice_string(notes: List[abjad.NamedPitch], duration_str: str) -> str:
    voice_string = notes[0].name + duration_str
    voice_string += " ".join([n.name for n in notes[1:]]) + duration_str
    return voice_string


def create_voice_with_ottava(
    pitches: List[int],
    voice_name: str = "Default voice",
    durations: List[int] | None = None,
) -> abjad.Voice:
    if durations is None:
        durations = [1]
    duration_str = f"{str(durations[0])}"
    notes = [abjad.NamedPitch(n) for n in pitches]
    voice_string = notes[0].name + duration_str
    voice_string += " ".join([n.name for n in notes[1:]]) + duration_str
    voice = abjad.Voice(voice_string, name=voice_name)

    for idx, n in get_partition_indices_and_ottava_n(pitches):
        abjad.attach(abjad.Ottava(n=n, site="before"), voice[idx])

    return voice


def get_partition_indices_and_ottava_n(
    pitches: List[int],
) -> List[Tuple[int, int]]:
    indices_and_ottava_n = []
    idx = 0
    partitions = partition_notes_to_ranges(pitches, ranges)
    for n, notes in partitions:
        indices_and_ottava_n.append((idx, n))
        idx += len(notes)
    return indices_and_ottava_n
