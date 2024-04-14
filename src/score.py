from typing import List
import abjad


def show_score(notes: List[int]) -> None:
    notes = [abjad.NamedPitch(n) for n in notes]
    if not notes:
        return
    note_string = notes[0].name + "1"
    note_string += " ".join([n.name for n in notes[1:]]) + "1"
    # string = "c'16 f' g' a' d' g' a' b' e' a' b' c'' f' b' c'' d''16"
    voice_1 = abjad.Voice(note_string, name="Voice_1")
    staff_1 = abjad.Staff([voice_1], name="Staff_1")
    abjad.show(staff_1)
