import numpy as np
from .run_length import encode as rle_encode
from .run_length import decode as rle_decode
from .run_length import Run
from typing import List

forward_entry_lookup = {
    'L': 0b0000,
    'R': 0b0100,
    'D': 0b1000,
    'U': 0b1100
}

forward_length_lookup = {
    1: 0b0000,
    2: 0b0001,
    3: 0b0010,
    4: 0b0011
}

reverse_entry_lookup = {
    0b0000: 'L',
    0b0100: 'R',
    0b1000: 'D',
    0b1100: 'U'
}

reverse_number_lookup = {
    0b0000: 1,
    0b0001: 2,
    0b0010: 3,
    0b0011: 4
}


def encode(keys: List[str]) -> np.array:
    rle = rle_encode(keys, 0b100)

    nybbles = [
        forward_entry_lookup[run.entry] +
        forward_length_lookup[run.length]
        for run in rle
    ]

    # Can't have an odd number of nybbles. This would break in mid-byte!
    # This is an extra 'L' on the end
    if len(nybbles) % 2 == 1:
        nybbles.append(0b0000)

    octets = [
        (nybbles[i] << 4) + (nybbles[i + 1] << 0)
        for i in range(0, len(nybbles), 2)
    ]
    return np.array(octets, dtype=np.uint8)


def decode(uint8array: np.array) -> List[str]:
    nybbles = []

    for octet in uint8array:
        nybbles.append((octet >> 4) & 0b1111)
        nybbles.append((octet >> 0) & 0b1111)

    rle = [
        Run(
            length=reverse_number_lookup[nybble & 0b0011],
            entry=reverse_entry_lookup[nybble & 0b1100]
        )
        for nybble in nybbles
    ]

    return rle_decode(rle)
