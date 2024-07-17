import datetime
from typing import Any

from music21.midi.realtime import StreamPlayer
from music21.stream import Score


def show_score(score: Score, fmt: str = "text") -> None:
    score.show(fmt)


def play_score(score: Any) -> None:
    StreamPlayer(score).play()


def export_to_musicxml(score: Score, filepath: str) -> None:
    score.write("musicxml", fp=filepath)


def filename(min_pitch: int, max_pitch: int, reference_pitch) -> str:
    # trunk-ignore(bandit/B311)
    return f"min_{min_pitch}_max{max_pitch}_ref{reference_pitch}_{datetime.datetime.now().isoformat()}"


def write_to_stdout(palette: list[float | int]):
    output_string = " ".join([str(note) for note in palette])
    print(output_string)
