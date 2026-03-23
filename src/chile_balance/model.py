from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Entry:
    date: date
    side: str
    sector: str
    category: str
    amount: float
    currency: str
    amount_pct_gdp: float | None
    certainty: str
    source: str
    source_date: date

    VALID_SIDES = ("asset", "liability")
    VALID_CERTAINTIES = ("reported", "estimated", "contingent")
    VALID_CURRENCIES = ("CLP", "USD", "UF")

    def __post_init__(self) -> None:
        if self.side not in self.VALID_SIDES:
            raise ValueError(
                f"side must be one of {self.VALID_SIDES}, got {self.side!r}"
            )
        if self.certainty not in self.VALID_CERTAINTIES:
            raise ValueError(
                f"certainty must be one of {self.VALID_CERTAINTIES}, got {self.certainty!r}"
            )
        if self.currency not in self.VALID_CURRENCIES:
            raise ValueError(
                f"currency must be one of {self.VALID_CURRENCIES}, got {self.currency!r}"
            )


@dataclass(frozen=True)
class ExchangeRate:
    date: date
    usd_to_clp: float
