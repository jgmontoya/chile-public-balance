from __future__ import annotations

from typing import Any

from chile_balance.collectors.banco_central import Observation
from chile_balance.model import Entry


def normalize(
    observations: list[Observation],
    metadata: dict[str, Any],
) -> list[Entry]:
    scale = metadata.get("scale", 1.0)
    entries = []
    for obs in observations:
        entry = Entry(
            date=obs.date,
            side=metadata["side"],
            sector=metadata["sector"],
            category=metadata["category"],
            amount=float(obs.value) * scale,
            currency=metadata["currency"],
            amount_pct_gdp=None,
            certainty=metadata["certainty"],
            source=metadata["source"],
            source_date=metadata["source_date"],
        )
        entries.append(entry)
    return entries
