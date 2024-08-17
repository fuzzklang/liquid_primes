from dataclasses import asdict
import json
from liquid_primes.scripts.utils import _distribute_events_over_voices_mut
from liquid_primes.score.model import Event, Score, Voice
from liquid_primes.score.create_score_with_gliss import map_to_gliss_events
from liquid_primes.score.mapping_to_sc_json import map_to_sc_json

VOICES = [
    Voice(name="a", type="type_a", events=list()),
    Voice(name="b", type="type_b", events=list()),
]


def test_json_export():
    onsets = [1, 2, 4, 5]
    durations = [2, 3, 2, 3]
    pitches = [60, 61, 62, 63]
    events = [Event(onset, duration, pitch) for (onset, duration, pitch) in zip(onsets, durations, pitches)]
    print(events)
    gliss_events = map_to_gliss_events(
        events=events,
        distance_to_trigger_gliss=2,
        split_point_normalized=0.5,
        pitch_bend=1,
    )
    score = map_to_sc_json(Score(voices=_distribute_events_over_voices_mut(gliss_events, VOICES)))
    print("Score:\n", score)
    score_as_json = json.dumps(asdict(score), indent=2)
    expected = json.loads(score_as_json)
    with open("./tests/test_data_expected_score.json", "r") as f:
        assert json.loads(f.read()) == expected
