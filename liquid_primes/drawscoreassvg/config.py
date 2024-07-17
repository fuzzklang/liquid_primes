from dataclasses import dataclass

A3_VIEWBOX_SIZE = (420, 297)


class ScoreView:
    def __init__(self, width=200, height=100, center_line=0, grid_base=1, margin=0):
        self.width: int = width
        self.height: int = height
        self.center_line: int = center_line
        self.grid_base: int = grid_base
        self.margin: int = margin
        self.rounded_center_line: int = grid_base * round(center_line / grid_base)
        self.origin = (-margin, self.rounded_center_line)


@dataclass
class Config:
    score_view: ScoreView = ScoreView(
        width=A3_VIEWBOX_SIZE[0],
        height=A3_VIEWBOX_SIZE[1],
        center_line=-int(A3_VIEWBOX_SIZE[1] / 2),
        grid_base=5,
        margin=20,
    )
