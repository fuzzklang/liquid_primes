import json
from dataclasses import asdict

from liquid_primes.palette.primes import primes
from liquid_primes.score.model import Event, Score, Voice

from liquid_primes.scripts.utils import _distribute_events_over_voices_mut
# from liquid_primes.score.mapping_to_drawable import map_to_events_with_glissandi

CONST_PITCH = 440
CONST_DUR = 4
PITCH_BEND = 1

OUTPUT_FILE = "./output/score.json"

VOICES = [
    Voice(name="A", type="", events=list()),
    Voice(name="B", type="", events=list()),
    Voice(name="C", type="", events=list()),
]


def main():
    onsets = primes(50)  # Generate prime seq
    events = [_get_event(onset=onset) for onset in onsets]
    # events_with_gliss = map_to_events_with_glissandi(
    #     events=events,
    #     distance_to_trigger_gliss=5,
    #     split_point_normalized=0.5,
    #     pitch_bend=PITCH_BEND,
    # )
    score = Score(voices=_distribute_events_over_voices_mut(events, VOICES))  # Distribute over voices
    score_as_json = json.dumps(asdict(score), indent=2)
    with open(OUTPUT_FILE, "w") as f:
        f.write(score_as_json)


def _get_event(onset, duration=CONST_DUR, pitch=CONST_PITCH):
    return Event(onset=onset, duration=duration, pitch=pitch)


if __name__ == "__main__":
    main()
