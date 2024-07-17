from itertools import cycle

from liquid_primes.score.model import Event, Voice


def _distribute_events_over_voices_mut(events: list[Event], voices: list[Voice]) -> list[Voice]:
    for event, voice in zip(events, cycle(voices)):
        voice.events.append(event)
    return voices
