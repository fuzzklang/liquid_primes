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

### Creating pitch palettes

#### Display help
```sh
poetry run python liquid_primes/palette --help
```

#### Output
Write generated data/pitches to stdout.
Currently space separated floats representing MIDI pitch.
Output format not stable.
```sh
poetry run python liquid_primes/palette -o
```

Write MusicXML output to `./tmp/`
```sh
poetry run python liquid_primes/palette -x
```

Playback (selected playback library/engine might change, currently using pygame).
Playback currently only supports quarter tones (limitation of MIDI playback).
```sh
poetry run python liquid_primes/palette -p
```

#### Manipulate pitches
Multiply intervals with a ratio, i.e. 0.5 ("shrinks" pitch intervals).
```sh
poetry run python liquid_primes/palette -r 0.5 -o
```

Or 1.25 ("expands" pitch intervals).
```sh
poetry run python liquid_primes/palette -r 1.25 -o
```

#### Tempo
Set tempo for MusicXML file or playback, given in quarter notes/beats per minutes.
Pitches are outputted as quarter notes.
```sh
poetry run python liquid_primes/palette -t 600 -p
```

### Creating score (distribute events over time)

Create and run scripts using the function from the different modules.

`./liquid_primes/scripts/write_events_to_json.py`: writes events to a JSON-format which can be read and played by a custom SuperCollider script.

`./liquid_primes/scripts/write_events_to_svg.py`: writes events to an SVG file which can be opened in i.e. InkScape.

```bash
poetry run python liquid_primes/scripts/write_events_to_svg.py
```
