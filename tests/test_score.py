from liquid_primes.score.create_score import _map_to_gliss_events, get_sum_of_voices
from liquid_primes.score.mapping_to_drawable import map_to_drawable_score
from liquid_primes.score.model import Voice, GlissEvent, GlissPoint, Event
from liquid_primes.drawscoreassvg import Point
from liquid_primes.drawscoreassvg import LineSegment as DrawLineSegment
from liquid_primes.drawscoreassvg import Score as DrawScore
from liquid_primes.drawscoreassvg import Voice as DrawVoice


def test_gliss_events_correctly_created():
    input_events = [
        Event(onset=1, pitch=60, duration=2, dynamic_range=(0.25, 0.5)),
        Event(onset=5, pitch=61, duration=2, dynamic_range=(0.3, 0.4)),
    ]
    result = _map_to_gliss_events(
        events=input_events, distance_to_trigger_gliss=0, split_point_normalized=0.5, pitch_bend=1
    )
    expected = [
        GlissEvent(
            onset=1,
            start_pitch=60,
            gliss=[GlissPoint(61, duration=1.0), GlissPoint(end_pitch=60, duration=1.0)],
            dynamic_range=(0.25, 0.5),
        ),
        GlissEvent(
            onset=5,
            start_pitch=61,
            gliss=[GlissPoint(62, duration=1.0), GlissPoint(end_pitch=61, duration=1.0)],
            dynamic_range=(0.3, 0.4),
        ),
    ]
    assert result == expected


def test_gliss_events_trigger_distance_correct():
    input_events = [
        Event(onset=1, pitch=60, duration=2, dynamic_range=(0.25, 0.5)),
        Event(onset=2, pitch=60, duration=2, dynamic_range=(0.25, 0.5)),
        Event(onset=4, pitch=60, duration=2, dynamic_range=(0.25, 0.5)),
    ]
    result = _map_to_gliss_events(
        events=input_events, distance_to_trigger_gliss=2, split_point_normalized=0.5, pitch_bend=1
    )
    expected = [
        GlissEvent(
            onset=1,
            start_pitch=60,
            gliss=[GlissPoint(61, duration=1.0), GlissPoint(end_pitch=60, duration=1.0)],
            dynamic_range=(0.25, 0.5),
        ),
        GlissEvent(
            onset=2,
            start_pitch=60,
            gliss=[GlissPoint(end_pitch=60, duration=2.0)],
            dynamic_range=(0.25, 0.5),
        ),
        GlissEvent(
            onset=4,
            start_pitch=60,
            gliss=[GlissPoint(61, duration=1.0), GlissPoint(end_pitch=60, duration=1.0)],
            dynamic_range=(0.25, 0.5),
        ),
    ]
    assert result == expected


def test_get_sum_of_voices():
    events_a = [
        GlissEvent(
            onset=1,
            start_pitch=1,
            gliss=[GlissPoint(1, 1)],
            dynamic_range=(0.25, 0.5),
        )
    ]
    events_b = [
        GlissEvent(
            onset=3,
            start_pitch=1,
            gliss=[GlissPoint(1, 1)],
            dynamic_range=(0.25, 0.5),
        )
    ]
    voices: list[Voice] = [
        Voice(name="a", type="type_a", events=events_a),
        Voice(name="b", type="type_b", events=events_b),
    ]
    result = get_sum_of_voices(voices)
    expected = Voice(name="sum", type="sum_type", events=events_a + events_b)
    assert expected == result


def test_get_sum_of_voices_no_events():
    voices: list[Voice] = [Voice(name="a", type="type_a", events=[]), Voice(name="b", type="type_b", events=[])]
    result = get_sum_of_voices(voices)
    expected = Voice(name="sum", type="sum_type", events=[])
    assert expected == result


def test_map_to_drawable_score():
    voices = [
        Voice(
            "a",
            "type_a",
            events=[
                GlissEvent(
                    1,
                    60,
                    [GlissPoint(60, 1)],
                    (0.25, 0.5),
                )
            ],
        ),
        Voice(
            "b",
            "type_b",
            events=[
                GlissEvent(
                    1,
                    60,
                    [GlissPoint(60, 1)],
                    (0.25, 0.5),
                ),
                GlissEvent(
                    1,
                    60,
                    [
                        GlissPoint(61, 1),
                        GlissPoint(60, 1),
                    ],
                    (0.25, 0.5),
                ),
            ],
        ),
    ]
    result: DrawScore = map_to_drawable_score(voices)
    expected = DrawScore(
        voices=[
            DrawVoice(
                name="a",
                type="type_a",
                line_segments=[DrawLineSegment([Point(1, -60), Point(2, -60)])],
            ),
            DrawVoice(
                name="b",
                type="type_b",
                line_segments=[
                    DrawLineSegment([Point(1, -60), Point(2, -60)]),
                    DrawLineSegment([Point(1, -60), Point(2, -61), Point(3, -60)]),
                ],
            ),
        ]
    )
    assert result == expected
