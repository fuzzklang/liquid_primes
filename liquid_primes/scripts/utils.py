from itertools import cycle

from liquid_primes.score.model import GlissEvent, Voice


def _distribute_events_over_voices_mut(events: list[GlissEvent], voices: list[Voice]) -> list[Voice]:
    for event, voice in zip(events, cycle(voices)):
        voice.events.append(event)
    return voices
