# Liquid primes
Generate pitch palettes.

## Requirements
- Python <= 3.10
- Poetry

## Install
```sh
poetry install
```

Optional dependencies for playback:

```sh
poetry install -E playback
```

## Usage
From project root.

### Display help
```sh
poetry run python liquid_primes --help
```

### Output
Write generated data/pitches to stdout.
Currently space separated floats representing MIDI pitch.
Output format not stable.
```sh
poetry run python liquid_primes -o
```

Write MusicXML output to `./tmp/`
```sh
poetry run python liquid_primes -x
```

Playback (selected playback library/engine might change, currently using pygame).
Playback currently only supports quarter tones (limitation of MIDI playback).
```sh
poetry run python liquid_primes -p
```

### Manipulate pitches
Multiply intervals with a ratio, i.e. 0.5 ("shrinks" pitch intervals).
```sh
poetry run python liquid_primes -r 0.5 -o
```

Or 1.25 ("expands" pitch intervals).
```sh
poetry run python liquid_primes -r 1.25 -o
```

### Tempo
Set tempo for MusicXML file or playback, given in quarter notes/beats per minutes.
Pitches are outputted as quarter notes.
```sh
poetry run python liquid_primes -t 600 -p
```
