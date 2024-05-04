import logging
from random import randint

import abjad
from abjad import Block, LilyPondFile, Score

import pygame


def show_score(score: Score) -> None:
    abjad.show(score)

def export_midi(score_block: Block, file_path: str) -> bool:
    lilypond_file = LilyPondFile([score_block])
    (_,_,_,return_code) = abjad.persist.as_midi(lilypond_file, file_path)
    is_success = return_code == 0
    if not is_success:
        logging.warning(f"Exporting to midi failed, return code: {return_code}")
    return is_success


def filename(min_pitch: int, max_pitch:int, reference_pitch) -> str:
    # trunk-ignore(bandit/B311)
    return f"/min_{min_pitch}_max{max_pitch}_ref{reference_pitch}_{randint(100,999)}"


def play_midi(midi_file_path):
    """Stream music_file in a blocking manner"""
    def play(path: str):
        clock = pygame.time.Clock()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30) # check if playback has finished

    # listen for interruptions
    try:
    # use the midi file you just saved
        play(midi_file_path)
    except KeyboardInterrupt as err:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit from err


def init_mixer(volume:float=0.8, channels:int=2):
    freq = 48000
    bitsize = -16   # unsigned 16 bit
    channels = channels
    buffer = 1024
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(volume)
