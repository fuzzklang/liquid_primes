import math
from dataclasses import dataclass
from itertools import cycle

from liquid_primes.drawscoreassvg import Config, Point, create_score, export_score_as_svg
from liquid_primes.drawscoreassvg import LineSegment as DrawLineSegment
from liquid_primes.drawscoreassvg import Score as DrawScore
from liquid_primes.drawscoreassvg import ScoreView as DrawScoreView
from liquid_primes.drawscoreassvg import Voice as DrawVoice
from liquid_primes.primes import primes


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
PITCH_BEND = 1

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
    events_with_gliss = _map_to_events_with_glissandi(
        events=events,
        distance_to_trigger_gliss=3,
        split_point_normalized=0.5,
        pitch_bend=PITCH_BEND,
    )
    voices = _distribute_events_over_voices_mut(events_with_gliss, VOICES)  # Distribute over voices
    # for voice in voices:
    #     print(f"==== {voice.name} {voice.type} ====")
    #     for e in voice.events:
    #         print(f" {e}")

    # Convert to event/domain objects
    drawable_score = _map_to_drawable_score(voices)
    # [print(x) for x in drawable_score.voices]

    # Create SVG score
    config = Config(DrawScoreView(width=150, height=1000, center_line=-800, margin=20, grid_base=10))
    export_score_as_svg(
        drawable_score,
        filepath="output/example_output.svg",
        with_voice_spread=10,
        config=config,
        with_labels=True,
        label_offset=15,
    )


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
            segment.points.append(Point(x=e.onset, y=-e.pitch))
            prev_onset = e.onset
            for gliss in e.gliss:
                prev_onset += gliss.duration
                segment.points.append(Point(x=prev_onset, y=-gliss.end_pitch))
        else:
            if e.duration is None:
                raise ValueError("Duration is None")
            segment.points.append(Point(x=e.onset, y=-e.pitch))
            segment.points.append(Point(x=e.onset + e.duration, y=-e.pitch))
        line_segments.append(segment)
    return line_segments


def _map_to_drawable_score(voices: list[Voice]) -> DrawScore:
    draw_voices: list[DrawVoice] = []
    for v in voices:
        draw_voices.append(DrawVoice(name=v.name, type=v.type, line_segments=_map_to_line_segments(v.events)))
    return create_score(voices=draw_voices)


def _map_to_events_with_glissandi(
    events: list[Event], distance_to_trigger_gliss: int | float, split_point_normalized: float = 0.5, pitch_bend=0
) -> list[Event]:
    """Converts a selection of the events to gliss events based on the criteria 'distance_to_trigger_gliss'."""

    def map_to_gliss_event(event: Event) -> Event:
        if event.duration is None:
            raise ValueError("Duration is None")
        gliss: list[GlissPoint] = [
            GlissPoint(end_pitch=event.pitch + pitch_bend, duration=math.ceil(event.duration * split_point_normalized)),
            GlissPoint(end_pitch=event.pitch, duration=math.floor(event.duration * split_point_normalized)),
        ]
        return Event(onset=event.onset, duration=None, pitch=event.pitch, gliss=gliss)

    if not events:
        return []

    events_with_glissandi: list[Event] = [events[0]]
    for e in events[1:]:
        if e.onset - events_with_glissandi[-1].onset <= distance_to_trigger_gliss:
            events_with_glissandi.append(map_to_gliss_event(e))
        else:
            events_with_glissandi.append(e)

    return events_with_glissandi


if __name__ == "__main__":
    main()
