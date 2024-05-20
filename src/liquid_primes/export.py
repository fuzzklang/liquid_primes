from random import randint
from typing import Any

from music21.stream import Score
from music21.midi.realtime import StreamPlayer


def show_score(score: Score, fmt: str = 'text') -> None:
    score.show(fmt)


def play_score(score: Any) -> None:
    StreamPlayer(score).play()


def export_to_musicxml(score: Score, filepath:str) -> None:
    score.write("musicxml", fp=filepath)


def filename(min_pitch: int, max_pitch:int, reference_pitch) -> str:
    # trunk-ignore(bandit/B311)
    return f"/min_{min_pitch}_max{max_pitch}_ref{reference_pitch}_{randint(100,999)}"