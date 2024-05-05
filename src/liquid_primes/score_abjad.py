import logging
from typing import Dict, List
import abjad
from abjad import Ottava, NamedPitch, Staff, Voice, Score, Block

from liquid_primes.pitches import get_partition_indices_and_ottava_n


def make_staff(voice: Voice, tempo: int|None = None, staff_name: str = "Default staff") -> Staff:
    staff = Staff([voice], name=staff_name)
    if tempo is not None and tempo > 0:
        mark = abjad.MetronomeMark(abjad.Duration(1, 4), tempo)
        logging.debug(f"Attaching tempo: {tempo}")
        abjad.attach(mark, voice[0])
    return staff

def make_score(staff: Staff, score_name: str = "Default score") -> Score:
    return Score([staff], name=score_name)

def create_blocks(score: Score, with_midi: bool = False) -> Block:
    items: List[Score | Block] = [score]
    if with_midi:
        items.append(Block("midi"))
    return Block("score", items)

def make_voice(
    pitches: List[int|float],
    durations: List[int] | None = None,
    voice_name: str = "Default voice",
    ranges: Dict[range, int] | None = None,
) -> Voice:
    if durations is None:
        durations = [1]
    voice = Voice(
        make_note_string(transform_to_named_pitches(pitches), durations),
        name=voice_name,
    )
    if ranges:
        attach_ottavas_mutating(voice, pitches, ranges)
    return voice


def make_note_string(notes: List[NamedPitch], durations: List[int]) -> str:
    assert len(durations) == 1
    duration_str = f"{str(durations[0])}"

    voice_string = notes[0].name + duration_str
    voice_string += " ".join([n.name for n in notes[1:]]) + duration_str
    return voice_string


def attach_ottavas_mutating(
    voice: Voice, pitches: List[int|float], ranges: Dict[range, int]
) -> None:
    for idx, n in get_partition_indices_and_ottava_n(pitches, ranges):
        abjad.attach(Ottava(n=n, site="before"), voice[idx])


def transform_to_named_pitches(pitches: List[int|float]) -> List[NamedPitch]:
    return [NamedPitch(n) for n in pitches]