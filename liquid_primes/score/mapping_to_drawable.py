import math

from liquid_primes.drawscoreassvg import Point, create_score
from liquid_primes.drawscoreassvg import LineSegment as DrawLineSegment
from liquid_primes.drawscoreassvg import Score as DrawScore
from liquid_primes.drawscoreassvg import Voice as DrawVoice
from liquid_primes.score.model import Event, GlissPoint, Voice


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


def map_to_drawable_score(voices: list[Voice]) -> DrawScore:
    draw_voices: list[DrawVoice] = []
    for v in voices:
        draw_voices.append(DrawVoice(name=v.name, type=v.type, line_segments=_map_to_line_segments(v.events)))
    return create_score(voices=draw_voices)


def map_to_events_with_glissandi(
    events: list[Event], distance_to_trigger_gliss: int | float, split_point_normalized: float = 0.5, pitch_bend=0
) -> list[Event]:
    """Converts a selection of the events to gliss events based on the criteria 'distance_to_trigger_gliss'."""

    def map_to_gliss_event(event: Event) -> Event:
        if event.duration is None:
            raise ValueError("Duration is None")
        gliss: list[GlissPoint] = [
            GlissPoint(end_pitch=event.pitch + pitch_bend, duration=math.ceil(event.duration * split_point_normalized)),
            GlissPoint(end_pitch=event.pitch, duration=math.floor(event.duration * (1.0 - split_point_normalized))),
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


def get_sum_of_voices(voices: list[Voice]) -> Voice:
    return Voice("Sum", "", [event for voice in voices for event in voice.events])
