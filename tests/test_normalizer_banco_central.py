from __future__ import annotations

from datetime import date
from decimal import Decimal

from chile_balance.collectors.banco_central import Observation
from chile_balance.model import Entry
from chile_balance.normalizers.banco_central import normalize


def test_normalize_produces_correct_entries():
    observations = [
        Observation(date=date(2024, 1, 1), value=Decimal("37438.37")),
    ]
    metadata = {
        "side": "asset",
        "sector": "central_bank",
        "category": "financial.international_reserves",
        "currency": "USD",
        "certainty": "reported",
        "source": "banco_central",
        "source_date": date(2024, 3, 1),
    }

    result = normalize(observations, metadata)

    assert len(result) == 1
    entry = result[0]
    assert isinstance(entry, Entry)
    assert entry.date == date(2024, 1, 1)
    assert entry.side == "asset"
    assert entry.amount == 37438.37
    assert entry.currency == "USD"
    assert entry.amount_pct_gdp is None
    assert entry.source == "banco_central"


def test_normalize_preserves_decimal_precision():
    metadata = {
        "side": "liability",
        "sector": "central_bank",
        "category": "debt.bonds",
        "currency": "CLP",
        "certainty": "reported",
        "source": "banco_central",
        "source_date": date(2024, 3, 1),
    }

    observations = [
        Observation(date=date(2024, 1, 1), value=Decimal("1234567890.99")),
        Observation(date=date(2024, 2, 1), value=Decimal("0.0")),
    ]

    result = normalize(observations, metadata)

    assert result[0].amount == 1234567890.99
    assert result[1].amount == 0.0
