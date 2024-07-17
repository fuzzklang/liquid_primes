from music21.duration import Duration
from music21.note import Note
from music21.pitch import Pitch
from music21.stream import Part, Score, Voice
from music21.tempo import MetronomeMark


def to_pitches(pitches: list[int | float]) -> list[Pitch]:
    return [Pitch(ps=p) for p in pitches]


def with_duration(pitches: list[Pitch], quarter_length=float) -> list[Note]:
    return [Note(p, duration=Duration(quarterLength=quarter_length)) for p in pitches]


def to_voice(notes=list[Note]) -> Voice:
    return Voice(notes)


def to_part(voice: Voice, quarter_tempo: int = 60) -> Part:
    part = Part(voice)
    part.insert(0, MetronomeMark(number=quarter_tempo, referent=Note(type="quarter")))
    return part


def to_score(part: Part) -> Score:
    score = Score(part)
    return score
