from liquid_primes.drawscoreassvg import Point, create_score
from liquid_primes.drawscoreassvg import LineSegment as DrawLineSegment
from liquid_primes.drawscoreassvg import Score as DrawScore
from liquid_primes.drawscoreassvg import Voice as DrawVoice
from liquid_primes.score.model import GlissEvent, Voice


def _map_to_line_segments(events: list[GlissEvent], min_interval: int | float) -> list[DrawLineSegment]:
    line_segments: list[DrawLineSegment] = []
    for e in events:
        segment = DrawLineSegment(points=list())
        segment.points.append(Point(x=e.onset, y=-e.start_pitch / min_interval))
        prev_onset = e.onset
        for gliss in e.gliss:
            prev_onset += gliss.duration
            segment.points.append(Point(x=prev_onset, y=-gliss.end_pitch / min_interval))
        line_segments.append(segment)
    return line_segments


def map_to_drawable_score(voices: list[Voice], min_bend: int | float = 1) -> DrawScore:
    draw_voices: list[DrawVoice] = []
    for v in voices:
        draw_voices.append(
            DrawVoice(name=v.name, type=v.type, line_segments=_map_to_line_segments(v.events, min_interval=min_bend))
        )
    return create_score(voices=draw_voices)
