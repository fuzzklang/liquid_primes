from .config import Config
from .create_score import _create_score
from .draw_score import _draw_score


def main():
    _draw_score(
        score=_create_score(),
        filepath="example.svg",
        config=Config(),
        with_visual_offset=20,
        with_labels=True,
    )


if __name__ == "__main__":
    main()
