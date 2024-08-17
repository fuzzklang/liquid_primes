from dataclasses import astuple, dataclass


@dataclass
class Point:
    x: int | float
    y: int | float

    def __iter__(self):
        return iter(astuple(self))

    def __getitem__(self, keys):
        return iter(getattr(self, k) for k in keys)


@dataclass
class LineSegment:
    points: list[Point]


@dataclass
class Voice:
    name: str
    type: str  # instrument/type
    line_segments: list[LineSegment]


@dataclass
class Score:
    voices: list[Voice]
