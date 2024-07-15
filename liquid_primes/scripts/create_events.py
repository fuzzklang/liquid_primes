from dataclasses import dataclass
from itertools import cycle

from liquid_primes.primes import primes
from liquid_primes.drawscoreassvg import Voice as DrawVoice, Score as DrawScore, LineSegment as DrawLineSegment, Point
from liquid_primes.drawscoreassvg import Config, create_score, export_score_as_svg, ScoreView as DrawScoreView

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


CONST_PITCH = 440
CONST_DUR = 11
VOICES = [
    Voice(name="A", type="", events=list()),
    Voice(name="B", type="", events=list()),
    Voice(name="C", type="", events=list()),
    Voice(name="D", type="", events=list()),
    Voice(name="E", type="", events=list()),
    Voice(name="F", type="", events=list()),
    Voice(name="G", type="", events=list()),
    Voice(name="H", type="", events=list()),
    Voice(name="I", type="", events=list()),
]


def main():
    onsets = primes(100)  # Generate prime seq
    events = [get_event(onset=onset) for onset in onsets]
    voices = _distribute_events_over_voices_mut(events, VOICES)  # Distribute over voices
    # for voice in voices:
    #     print(f"==== {voice.name} {voice.type} ====")
    #     for e in voice.events:
    #         print(f" {e}")

    # Convert to event/domain objects
    drawable_score = map_to_drawable_score(voices)
    # [print(x) for x in drawable_score.voices]

    # Create SVG score
    config = Config(DrawScoreView(width=150, height=600, center_line=0, margin=20, grid_base=10))
    export_score_as_svg(drawable_score, filepath="output/example_output.svg", config=config, with_labels=True, label_offset=0)



def get_event(onset, duration=CONST_DUR, pitch=CONST_PITCH):
    return Event(onset=onset, duration=duration, pitch=pitch)


def _distribute_events_over_voices_mut(events: list[Event], voices: list[Voice]) -> list[Voice]:
    for event, voice in zip(events, cycle(voices)):
        voice.events.append(event)
    return voices


def _map_to_line_segments(events: list[Event]) -> list[DrawLineSegment]:
    line_segments: list[DrawLineSegment] = []
    for e in events:
        segment = DrawLineSegment(points=list())
        if e.gliss:
            segment.points.append(Point(x=e.onset, y=e.pitch))
            prev_onset = e.onset
            for gliss in e.gliss:
                prev_onset += gliss.duration
                segment.points.append(Point(x=prev_onset, y=gliss.end_pitch))
        else:
            if e.duration is None:
                raise ValueError("Duration is None")
            segment.points.append(Point(x=e.onset, y=e.pitch))
            segment.points.append(Point(x=e.onset+e.duration, y=e.pitch))
        line_segments.append(segment)
    return line_segments


def map_to_drawable_score(voices: list[Voice]) -> DrawScore:
    draw_voices: list[DrawVoice] = []
    for v in voices:
        draw_voices.append(DrawVoice(name=v.name, type=v.type, line_segments=_map_to_line_segments(v.events)))
    return create_score(voices=draw_voices)


if __name__ == '__main__':
    main()