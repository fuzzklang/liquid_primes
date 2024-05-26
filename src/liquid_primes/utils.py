import logging
import sys

def read_ints_from_stdin() -> list[int]:
    line = sys.stdin.readlines()[0]
    logging.debug(f"read from stdin, {line=}")
    if not line:
        raise ValueError("No input given")
    values = line.strip().split()
    row = [int(val) for val in values]
    return row