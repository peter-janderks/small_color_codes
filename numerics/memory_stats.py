import json
import math
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

import sinter


@dataclass(frozen=True)
class MemoryEstimate:
    metadata: dict
    error_rate: float
    standard_error: float


def combine_x_and_z(stats: Iterable[sinter.TaskStats]) -> list[MemoryEstimate]:
    """Pool shots within each basis and estimate the error rate per logical qubit."""
    runs = defaultdict(dict)
    for stat in stats:
        metadata = stat.json_metadata.copy()
        basis = metadata.pop("basis")
        if basis not in ("X", "Z"):
            raise ValueError(f"Unexpected memory basis {basis!r} for {metadata}")

        # The strong ID is basis-specific. Match on the decoder and the remaining
        # metadata, using sorted JSON so key order does not matter.
        key = stat.decoder, json.dumps(metadata, sort_keys=True)
        counts = runs[key]
        counts[basis] = counts.get(basis, sinter.AnonTaskStats()) + stat.to_anon_stats()

    missing = [
        f"missing {'Z' if 'X' in counts else 'X'} basis for {decoder}: {metadata}"
        for (decoder, metadata), counts in runs.items()
        if len(counts) != 2
    ]
    if missing:
        raise ValueError("Unpaired X/Z memory results:\n" + "\n".join(missing))

    combined = []
    for (decoder, metadata_json), counts in runs.items():
        x, z = counts["X"], counts["Z"]
        if x.shots == 0 or z.shots == 0:
            raise ValueError(f"Zero shots in a memory basis for {decoder}: {metadata_json}")
        metadata = json.loads(metadata_json)
        k = metadata["k"]
        q_x = x.errors / x.shots
        q_z = z.errors / z.shots
        variance = q_x * (1 - q_x) / x.shots + q_z * (1 - q_z) / z.shots
        combined.append(MemoryEstimate(metadata, (q_x + q_z) / k, math.sqrt(variance) / k))
    return combined
