from __future__ import annotations

from datetime import date

import pytest

from chile_balance.model import Entry


def test_entry_creation_with_valid_fields():
    entry = Entry(
        date=date(2024, 1, 15),
        side="asset",
        sector="central_government",
        category="financial.sovereign_funds.fees",
        amount=1_000_000_000.0,
        currency="CLP",
        amount_pct_gdp=0.5,
        certainty="reported",
        source="dipres",
        source_date=date(2024, 2, 1),
    )

    assert entry.date == date(2024, 1, 15)
    assert entry.side == "asset"
    assert entry.sector == "central_government"
    assert entry.category == "financial.sovereign_funds.fees"
    assert entry.amount == 1_000_000_000.0
    assert entry.currency == "CLP"
    assert entry.amount_pct_gdp == 0.5
    assert entry.certainty == "reported"
    assert entry.source == "dipres"
    assert entry.source_date == date(2024, 2, 1)


def test_entry_rejects_invalid_side():
    with pytest.raises(ValueError, match="side"):
        Entry(
            date=date(2024, 1, 15),
            side="bogus",
            sector="central_government",
            category="financial.sovereign_funds.fees",
            amount=1_000_000_000.0,
            currency="USD",
            amount_pct_gdp=None,
            certainty="reported",
            source="dipres",
            source_date=date(2024, 2, 1),
        )


def test_entry_rejects_invalid_certainty():
    with pytest.raises(ValueError, match="certainty"):
        Entry(
            date=date(2024, 1, 15),
            side="asset",
            sector="central_government",
            category="financial.sovereign_funds.fees",
            amount=1_000_000_000.0,
            currency="USD",
            amount_pct_gdp=None,
            certainty="maybe",
            source="dipres",
            source_date=date(2024, 2, 1),
        )


def test_entry_rejects_invalid_currency():
    with pytest.raises(ValueError, match="currency"):
        Entry(
            date=date(2024, 1, 15),
            side="asset",
            sector="central_government",
            category="financial.sovereign_funds.fees",
            amount=1_000_000_000.0,
            currency="EUR",
            amount_pct_gdp=None,
            certainty="reported",
            source="dipres",
            source_date=date(2024, 2, 1),
        )
