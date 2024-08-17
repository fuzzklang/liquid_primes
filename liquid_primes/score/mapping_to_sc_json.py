from liquid_primes.score.model import GlissEvent, Score, SCScore, SCVoice, SCEvent, Voice


def map_to_sc_json(score: Score) -> SCScore:
    return SCScore(voices=[_map_to_sc_voice(voice) for voice in score.voices])


def _map_to_sc_voice(voice: Voice) -> SCVoice:
    return SCVoice(name=voice.name, type=voice.type, events=[_map_to_sc_event(event) for event in voice.events])


def _map_to_sc_event(gliss_event: GlissEvent) -> SCEvent:
    sc_pitches = [gliss_event.start_pitch, *[p.end_pitch for p in gliss_event.gliss]]
    sc_durations = [p.duration for p in gliss_event.gliss]
    return SCEvent(onset=gliss_event.onset, durations=sc_durations, pitches=sc_pitches)
