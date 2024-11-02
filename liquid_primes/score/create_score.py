import copy
from itertools import cycle
import math
from typing import Generator
from liquid_primes.score.model import Event, GlissEvent, GlissPoint, Voice, Score, Section


def create_score_from_sections(
    sections: list[Section],
    voices: list[Voice],
    onset_gen: Generator[int, None, None],
    distribution=None,
) -> Score:
    gliss_events = [event for section in sections for event in _section_to_events(onset_gen, section)]
    return create_score_from_gliss_events(gliss_events, voices, onset_gen)


def create_score_from_gliss_events(
    events: list[GlissEvent],
    voices: list[Voice],
    distribution=None,
) -> Score:
    score = Score(voices=_distribute_events_over_voices_mut(events, _get_copy_of_voices(voices)))
    return validate_score(score)


def _get_onsets(onset_gen: Generator[int, None, None], n: int):
    return [next(onset_gen) for _ in range(n)]


def _get_copy_of_voices(voices: list[Voice]):
    return copy.deepcopy(voices)


def _section_to_events(onset_gen: Generator[int, None, None], section: Section):
    onsets = _get_onsets(onset_gen, section.num_events)
    events = [
        Event(
            onset=onset,
            duration=section.base_duration,
            pitch=section.reference_pitch,
            dynamic_range=section.dynamic_range,
        )
        for onset in onsets
    ]
    gliss_events = _map_to_gliss_events(
        events=events,
        distance_to_trigger_gliss=section.distance_to_trigger_gliss,
        split_point_normalized=0.5,
        pitch_bend=section.pitch_bend,
    )
    return gliss_events


def _map_to_gliss_events(
    events: list[Event], distance_to_trigger_gliss: int | float, split_point_normalized: float = 0.5, pitch_bend=0
) -> list[GlissEvent]:
    """Converts a selection of the events to gliss events based on the criteria 'distance_to_trigger_gliss'."""

    def map_to_gliss_event(event: Event) -> GlissEvent:
        """Assumes 1 is smallest interval, gives unexpected results.
        TODO: Should handle floats"""
        gliss: list[GlissPoint] = [
            GlissPoint(
                end_pitch=event.pitch + pitch_bend,
                duration=math.ceil(event.duration * split_point_normalized),
            ),
            GlissPoint(
                end_pitch=event.pitch,
                duration=math.floor(event.duration * (1.0 - split_point_normalized)),
            ),
        ]
        return GlissEvent(
            onset=event.onset,
            start_pitch=event.pitch,
            gliss=gliss,
            dynamic_range=event.dynamic_range,
        )

    if not events:
        return []

    gliss_events: list[GlissEvent] = [map_to_gliss_event(events[0])]
    for e in events[1:]:
        if e.onset - gliss_events[-1].onset >= distance_to_trigger_gliss:
            gliss_events.append(map_to_gliss_event(e))
        else:
            gliss_events.append(
                GlissEvent(
                    onset=e.onset,
                    start_pitch=e.pitch,
                    gliss=[GlissPoint(end_pitch=e.pitch, duration=e.duration)],
                    dynamic_range=e.dynamic_range,
                )
            )

    return gliss_events


def _distribute_events_over_voices_mut(events: list[GlissEvent], voices: list[Voice]) -> list[Voice]:
    for event, voice in zip(events, cycle(voices)):
        voice.events.append(event)
    return voices


def get_sum_of_voices(voices: list[Voice]) -> Voice:
    return Voice("sum", "sum_type", [event for voice in voices for event in voice.events])


def validate_score(score: Score) -> Score:
    """TODO: implement"""
    return score
