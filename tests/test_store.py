from __future__ import annotations

from datetime import date

from chile_balance.model import Entry, ExchangeRate
from chile_balance.store import write_entries, read_entries, write_rates, read_rates


def _make_entry(**overrides) -> Entry:
    defaults = dict(
        date=date(2024, 1, 15),
        side="asset",
        sector="central_government",
        category="financial.sovereign_funds.fees",
        amount=1_000_000.5,
        currency="USD",
        amount_pct_gdp=0.5,
        certainty="reported",
        source="dipres",
        source_date=date(2024, 2, 1),
    )
    defaults.update(overrides)
    return Entry(**defaults)


def test_roundtrip_write_then_read(tmp_path):
    csv_file = tmp_path / "balance.csv"
    entries = [
        _make_entry(),
        _make_entry(
            date=date(2024, 2, 15),
            side="liability",
            amount=2_000_000.0,
            currency="CLP",
            amount_pct_gdp=None,
            certainty="estimated",
        ),
    ]

    write_entries(csv_file, entries)
    result = read_entries(csv_file)

    assert len(result) == 2
    assert result[0] == entries[0]
    assert result[1] == entries[1]
    assert result[1].amount_pct_gdp is None


def test_separate_writes_with_distinct_keys_accumulate(tmp_path):
    csv_file = tmp_path / "balance.csv"
    batch1 = [_make_entry(date=date(2024, 1, 15), amount=100.0)]
    batch2 = [_make_entry(date=date(2024, 2, 15), amount=200.0)]

    write_entries(csv_file, batch1)
    write_entries(csv_file, batch2)

    result = read_entries(csv_file)
    amounts = sorted(e.amount for e in result)
    assert amounts == [100.0, 200.0]

    raw_lines = csv_file.read_text().strip().splitlines()
    header_count = sum(1 for line in raw_lines if line.startswith("date,"))
    assert header_count == 1


def test_write_entries_is_idempotent(tmp_path):
    csv_file = tmp_path / "balance.csv"
    entries = [
        _make_entry(),
        _make_entry(date=date(2024, 2, 15), category="financial.other"),
    ]

    write_entries(csv_file, entries)
    write_entries(csv_file, entries)

    result = read_entries(csv_file)
    assert sorted(result, key=lambda e: (e.date, e.category)) == sorted(
        entries, key=lambda e: (e.date, e.category)
    )


def test_read_nonexistent_file_returns_empty_list(tmp_path):
    csv_file = tmp_path / "does_not_exist.csv"
    assert read_entries(csv_file) == []


def test_rates_roundtrip(tmp_path):
    csv_file = tmp_path / "rates.csv"
    rates = [
        ExchangeRate(date=date(2024, 1, 15), usd_to_clp=935.5),
        ExchangeRate(date=date(2024, 1, 16), usd_to_clp=940.2),
    ]

    write_rates(csv_file, rates)
    result = read_rates(csv_file)

    assert len(result) == 2
    assert result[0] == rates[0]
    assert result[1] == rates[1]


def test_read_nonexistent_rates_returns_empty(tmp_path):
    assert read_rates(tmp_path / "nope.csv") == []


def test_write_rates_is_idempotent(tmp_path):
    csv_file = tmp_path / "rates.csv"
    rates = [
        ExchangeRate(date=date(2024, 1, 15), usd_to_clp=935.5),
        ExchangeRate(date=date(2024, 1, 16), usd_to_clp=940.2),
    ]

    write_rates(csv_file, rates)
    write_rates(csv_file, rates)

    result = read_rates(csv_file)
    assert result == rates


def test_write_rates_revision_overwrites_same_date(tmp_path):
    csv_file = tmp_path / "rates.csv"
    write_rates(csv_file, [ExchangeRate(date=date(2024, 1, 15), usd_to_clp=935.5)])
    write_rates(csv_file, [ExchangeRate(date=date(2024, 1, 15), usd_to_clp=999.9)])

    result = read_rates(csv_file)
    assert result == [ExchangeRate(date=date(2024, 1, 15), usd_to_clp=999.9)]
