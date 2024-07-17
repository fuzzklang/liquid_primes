from .model import Score, Voice


def _create_score(voices: list[Voice] = []):
    return Score(voices=voices)
