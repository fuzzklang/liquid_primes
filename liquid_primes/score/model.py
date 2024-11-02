from dataclasses import dataclass


@dataclass
class Section:
    num_events: int
    reference_pitch: int | float
    base_duration: int | float
    pitch_bend: int | float
    distance_to_trigger_gliss: int | float
    dynamic_range: tuple[float, ...]


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
    dynamic_range: tuple[float, ...]


@dataclass
class GlissEvent:
    onset: int | float
    start_pitch: int | float
    gliss: list[GlissPoint]
    dynamic_range: tuple[float, ...]


dynamics: dict[str, float] = {
    "ppp": 0.12,
    "pp": 0.25,
    "p": 0.37,
    "mp": 0.5,
    "mf": 0.6,
    "f": 0.73,
    "ff": 0.88,
    "fff": 1,
}


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
    dynamic_range: tuple[float, ...]
