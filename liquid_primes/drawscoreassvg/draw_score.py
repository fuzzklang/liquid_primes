import drawsvg as draw

from .model import Score
from .config import Config


def _draw_score(score: Score, filepath: str, config: Config, with_voice_spread: int = 0, with_labels: bool = False, label_offset: int = 20):
    d = draw.Drawing(config.score_view.width, config.score_view.height, config.score_view.origin)

    for n, voice in enumerate(score.voices):
        y_axis_visual_offset = n * with_voice_spread
        if with_labels:
            minimum_gap_from_line = 5
            label_y_pos = voice.line_segments[0].points[0].y + y_axis_visual_offset + minimum_gap_from_line
            d.append(draw.Text(text=voice.name,
                               font_size=4,
                               x=-min(config.score_view.margin, label_offset),
                               y=label_y_pos))
        for event in voice.line_segments:
            d.append(_draw_line(event.points, y_axis_visual_offset))

    d.set_pixel_scale(1)  # Set number of pixels per geometry unit
    d.save_svg(filepath)


def _draw_line(positions, y_axis_visual_offset):
    if len(positions) < 2:
        raise ValueError("Two or more positions required to draw line")
    if len(positions) == 2:
        (sx, sy), (ex, ey) = positions[0], positions[1]
        return draw.Line(sx, sy+y_axis_visual_offset, ex, ey+y_axis_visual_offset,
                stroke='black', stroke_width=0.25, fill='none')
    else:
        p = draw.Path(stroke='black', stroke_width=0.25, fill='none')
        (x,y) = positions[0]
        p = p.M(x,y+y_axis_visual_offset)
        for (x,y) in positions[1:]:
            p = p.L(x,y+y_axis_visual_offset)
        return p