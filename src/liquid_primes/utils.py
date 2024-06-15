import logging
import sys

def read_nums_from_stdin() -> list[int]:
    line = sys.stdin.readlines()[0]
    logging.debug(f"read from stdin, {line=}")
    if not line:
        raise ValueError("No input given")
    values = line.strip().split()
    row = [float(val) for val in values]
    return row