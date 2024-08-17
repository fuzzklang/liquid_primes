from dataclasses import dataclass


@dataclass
class Voice:
    name: str
    type: str
    events: list["GlissEvent"]


@dataclass
class GlissPoint:
    end_pitch: int | float
    duration: int | float


@dataclass
class Event:
    onset: int | float
    duration: int | float
    pitch: int | float


@dataclass
class GlissEvent:
    onset: int | float
    start_pitch: int | float
    gliss: list[GlissPoint]


@dataclass
class Score:
    voices: list[Voice]


@dataclass
class SCScore:
    voices: list["SCVoice"]


@dataclass
class SCVoice:
    name: str
    type: str
    events: list["SCEvent"]


@dataclass
class SCEvent:
    onset: int | float
    durations: list[int | float]
    pitches: list[int | float]
