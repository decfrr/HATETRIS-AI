from typing import Any, List


class Run:
    def __init__(self, length: int, entry: Any):
        self.length = length
        self.entry = entry


def encode(arr: List[Any], max_run_length: int) -> List[Run]:
    runs = []
    for entry in arr:
        if (
            runs and
            runs[-1].entry == entry and
            runs[-1].length < max_run_length
        ):
            runs[-1].length += 1
        else:
            runs.append(Run(length=1, entry=entry))
    return runs


def decode(runs: List[Run]) -> List[Any]:
    decoded = []
    for run in runs:
        decoded.extend([run.entry] * run.length)
    return decoded
