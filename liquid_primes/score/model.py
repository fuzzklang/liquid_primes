from dataclasses import dataclass


@dataclass
class Voice:
    name: str
    type: str
    events: list["Event"]


@dataclass
class GlissPoint:
    end_pitch: int | float
    duration: int | float


@dataclass
class Event:
    onset: int | float
    duration: int | float | None
    pitch: int | float
    gliss: list[GlissPoint] | None = None


@dataclass
class Score:
    voices: list[Voice]
