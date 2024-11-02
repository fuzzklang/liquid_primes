from dataclasses import asdict
import json

from liquid_primes.score.model import Section, Voice
from liquid_primes.score.create_score import get_sum_of_voices, create_score_from_sections
from liquid_primes.score.mapping_to_sc_json import map_to_sc_json
from liquid_primes.palette.primes import prime_gen
from liquid_primes.score.mapping_to_drawable import map_to_drawable_score
from liquid_primes.drawscoreassvg import Config as DrawConfig, ScoreView as DrawScoreView, export_score_as_svg


N_PRIMES = 50
CONST_PITCH = 94
CONST_DUR = 11
PITCH_BEND = 0.33
DIST_TO_TRIGGER_GLISS = 3

VOICES = [
    Voice(name="a", type="typeA", events=list()),
    Voice(name="b", type="typeB", events=list()),
    Voice(name="c", type="typeC", events=list()),
    Voice(name="d", type="typeD", events=list()),
    Voice(name="e", type="typeE", events=list()),
    Voice(name="f", type="typeF", events=list()),
    Voice(name="g", type="typeG", events=list()),
]

sections = [
    Section(
        num_events=11,
        reference_pitch=60,
        base_duration=11,
        pitch_bend=0.25,
        distance_to_trigger_gliss=5,
        dynamic_range=(0.2, 0.4),
    ),
    Section(
        num_events=13,
        reference_pitch=61,
        base_duration=7,
        pitch_bend=0.25,
        distance_to_trigger_gliss=5,
        dynamic_range=(0.3, 0.5),
    ),
    Section(
        num_events=17,
        reference_pitch=62,
        base_duration=5,
        pitch_bend=0.25,
        distance_to_trigger_gliss=5,
        dynamic_range=(0.4, 0.8),
    ),
]


def main():
    # Prime generator for onsets
    onset_gen = prime_gen(0)

    # Create score from sections
    score = create_score_from_sections(sections, VOICES, onset_gen)

    # Write JSON score (for SuperCollider)
    score_as_json = json.dumps(asdict(map_to_sc_json(score)), indent=2)
    with open("./output/testing_sections.json", "w") as f:
        f.write(score_as_json)

    # Write SVG (for Inkscape)
    voices = score.voices
    voices.append(get_sum_of_voices(voices))
    # Convert to drawable and create SVG score
    drawable_score = map_to_drawable_score(voices, min_bend=PITCH_BEND)
    config = DrawConfig(DrawScoreView(width=1500, height=1000, center_line=-800, margin=20, grid_base=10))
    export_score_as_svg(
        drawable_score,
        filepath="output/testing_sections.svg",
        with_voice_spread=10,
        config=config,
        with_labels=True,
        label_offset=15,
    )


if __name__ == "__main__":
    main()
