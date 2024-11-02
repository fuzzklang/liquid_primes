from dataclasses import asdict
import json
from liquid_primes.score.model import Event, Voice
from liquid_primes.score.create_score import _map_to_gliss_events, create_score_from_gliss_events
from liquid_primes.score.mapping_to_sc_json import map_to_sc_json

VOICES = [
    Voice(name="a", type="type_a", events=list()),
    Voice(name="b", type="type_b", events=list()),
]


def test_json_export():
    onsets = [1, 2, 4, 5]
    durations = [2, 3, 2, 3]
    pitches = [60, 61, 62, 63]
    dynamic_ranges = (
        (0.1, 0.2),
        (0.2, 0.3),
        (0.3, 0.4),
        (0.4, 0.5),
    )
    events = [
        Event(onset, duration, pitch, dynamic_range)
        for (onset, duration, pitch, dynamic_range) in zip(onsets, durations, pitches, dynamic_ranges)
    ]
    gliss_events = _map_to_gliss_events(
        events=events,
        distance_to_trigger_gliss=2,
        split_point_normalized=0.5,
        pitch_bend=1,
    )
    score = create_score_from_gliss_events(gliss_events, voices=VOICES)
    sc_score = map_to_sc_json(score)
    score_as_json = json.dumps(asdict(sc_score), indent=2)
    expected = json.loads(score_as_json)
    with open("./tests/test_data_expected_score.json", "r") as f:
        assert json.loads(f.read()) == expected
