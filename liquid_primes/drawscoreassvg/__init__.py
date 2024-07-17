from .config import Config, ScoreView
from .create_score import _create_score
from .draw_score import _draw_score
from .model import LineSegment, Point, Score, Voice


def create_score(voices: list[Voice]) -> Score:
    return _create_score(voices=voices)


def export_score_as_svg(
    score: Score, filepath: str, config=Config(), with_voice_spread=0, with_labels=False, label_offset=0
) -> None:
    _draw_score(score, filepath, config, with_voice_spread, with_labels, label_offset)


def create_and_export_as_svg(
    voices: list[Voice], filepath: str, config=Config(), with_voice_spread=0, with_labels=False, label_offset=0
):
    _draw_score(_create_score(voices), filepath, config, with_voice_spread, with_labels, label_offset)


__all__ = [
    create_score.__name__,
    export_score_as_svg.__name__,
    Point.__name__,
    Score.__name__,
    Voice.__name__,
    LineSegment.__name__,
    Config.__name__,
    ScoreView.__name__,
]
