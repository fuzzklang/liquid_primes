from liquid_primes.drawscoreassvg import Config, export_score_as_svg
from liquid_primes.drawscoreassvg import ScoreView as DrawScoreView
from liquid_primes.palette.primes import primes
from liquid_primes.score.mapping_to_drawable import (
    get_sum_of_voices,
    map_to_drawable_score,
    map_to_events_with_glissandi,
)
from liquid_primes.score.model import Event, Voice

from liquid_primes.scripts.utils import _distribute_events_over_voices_mut

CONST_PITCH = 440
CONST_DUR = 11
PITCH_BEND = 1

VOICES = [
    Voice(name="A", type="", events=list()),
    Voice(name="B", type="", events=list()),
    Voice(name="C", type="", events=list()),
    Voice(name="D", type="", events=list()),
    Voice(name="E", type="", events=list()),
    Voice(name="F", type="", events=list()),
    Voice(name="G", type="", events=list()),
    Voice(name="H", type="", events=list()),
    Voice(name="I", type="", events=list()),
]


def main():
    onsets = primes(100)  # Generate prime seq
    events = [_get_event(onset=onset) for onset in onsets]
    events_with_gliss = map_to_events_with_glissandi(
        events=events,
        distance_to_trigger_gliss=5,
        split_point_normalized=0.5,
        pitch_bend=PITCH_BEND,
    )
    voices = _distribute_events_over_voices_mut(events_with_gliss, VOICES)  # Distribute over voices
    voices.append(get_sum_of_voices(voices))

    # Convert to drawable and create SVG score
    drawable_score = map_to_drawable_score(voices)
    config = Config(DrawScoreView(width=1500, height=1000, center_line=-800, margin=20, grid_base=10))
    export_score_as_svg(
        drawable_score,
        filepath="output/example_output.svg",
        with_voice_spread=10,
        config=config,
        with_labels=True,
        label_offset=15,
    )


def _get_event(onset, duration=CONST_DUR, pitch=CONST_PITCH):
    return Event(onset=onset, duration=duration, pitch=pitch)


if __name__ == "__main__":
    main()