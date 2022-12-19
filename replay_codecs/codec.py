from typing import List
from .uint8array import encode as uint8array_encode
from .uint8array import decode as uint8array_decode
from .b2048 import encode as b2048_encode
from .b2048 import decode as b2048_decode


def encode(keys: List[str]) -> str:
    return b2048_encode(uint8array_encode(keys))


def decode(string: str) -> List[str]:
    return uint8array_decode(b2048_decode(string))

