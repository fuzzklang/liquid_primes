from dataclasses import asdict
import json

from liquid_primes.scripts.utils import _distribute_events_over_voices_mut
from liquid_primes.score.model import Event, Score, Voice
from liquid_primes.score.create_score_with_gliss import get_sum_of_voices, map_to_gliss_events
from liquid_primes.score.mapping_to_sc_json import map_to_sc_json
from liquid_primes.palette.primes import primes
from liquid_primes.score.mapping_to_drawable import map_to_drawable_score
from liquid_primes.drawscoreassvg import Config as DrawConfig, ScoreView as DrawScoreView, export_score_as_svg


CONST_PITCH = 94
CONST_DUR = 11
PITCH_BEND = 0.33
N_PRIMES = 50
DIST_TO_TRIGGER_GLISS = 3

VOICES = [
    Voice(name="a", type="typeA", events=list()),
    Voice(name="b", type="typeB", events=list()),
    Voice(name="c", type="typeC", events=list()),
    Voice(name="d", type="typeD", events=list()),
    Voice(name="e", type="typeE", events=list()),
]


def main():
    onsets = primes(N_PRIMES)  # Generate prime seq
    events = [_get_event(onset=onset, duration=CONST_DUR, pitch=CONST_PITCH) for onset in onsets]
    gliss_events = map_to_gliss_events(
        events=events,
        distance_to_trigger_gliss=DIST_TO_TRIGGER_GLISS,
        split_point_normalized=0.5,
        pitch_bend=PITCH_BEND,
    )
    # Distribute over voices
    score = Score(voices=_distribute_events_over_voices_mut(gliss_events, VOICES))

    # Write JSON score (for SuperCollider)
    score_as_json = json.dumps(asdict(map_to_sc_json(score)), indent=2)
    with open("./output/demo.json", "w") as f:
        f.write(score_as_json)

    # Write SVG (for Inkscape)
    voices = score.voices
    voices.append(get_sum_of_voices(voices))
    # Convert to drawable and create SVG score
    drawable_score = map_to_drawable_score(voices, min_bend=PITCH_BEND)
    config = DrawConfig(DrawScoreView(width=1500, height=1000, center_line=-800, margin=20, grid_base=10))
    export_score_as_svg(
        drawable_score,
        filepath="output/demo.svg",
        with_voice_spread=10,
        config=config,
        with_labels=True,
        label_offset=15,
    )


def _get_event(onset, duration=CONST_DUR, pitch=CONST_PITCH):
    return Event(onset=onset, duration=duration, pitch=pitch)


if __name__ == "__main__":
    main()
