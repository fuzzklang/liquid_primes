import math
from liquid_primes.score.model import Event, GlissEvent, GlissPoint, Voice


def map_to_gliss_events(
    events: list[Event], distance_to_trigger_gliss: int | float, split_point_normalized: float = 0.5, pitch_bend=0
) -> list[GlissEvent]:
    """Converts a selection of the events to gliss events based on the criteria 'distance_to_trigger_gliss'."""

    def map_to_gliss_event(event: Event) -> GlissEvent:
        """Assumes 1 is smalles interval, gives unexpected results.
        TODO: Should handle floats"""
        gliss: list[GlissPoint] = [
            GlissPoint(end_pitch=event.pitch + pitch_bend, duration=math.ceil(event.duration * split_point_normalized)),
            GlissPoint(end_pitch=event.pitch, duration=math.floor(event.duration * (1.0 - split_point_normalized))),
        ]
        return GlissEvent(onset=event.onset, start_pitch=event.pitch, gliss=gliss)

    if not events:
        return []

    gliss_events: list[GlissEvent] = [map_to_gliss_event(events[0])]
    for e in events[1:]:
        if e.onset - gliss_events[-1].onset >= distance_to_trigger_gliss:
            gliss_events.append(map_to_gliss_event(e))
        else:
            gliss_events.append(
                GlissEvent(
                    onset=e.onset, start_pitch=e.pitch, gliss=[GlissPoint(end_pitch=e.pitch, duration=e.duration)]
                )
            )

    return gliss_events


def get_sum_of_voices(voices: list[Voice]) -> Voice:
    return Voice("sum", "sum_type", [event for voice in voices for event in voice.events])
