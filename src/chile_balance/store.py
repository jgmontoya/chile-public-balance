from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from chile_balance.model import Entry, ExchangeRate

ENTRY_FIELDS = [
    "date", "side", "sector", "category", "amount", "currency",
    "amount_pct_gdp", "certainty", "source", "source_date",
]

RATE_FIELDS = ["date", "usd_to_clp"]


def _entry_key(entry: Entry) -> tuple[date, str, str, str, str]:
    return (entry.date, entry.side, entry.sector, entry.category, entry.currency)


def write_entries(path: Path, entries: list[Entry]) -> None:
    merged: dict[tuple[date, str, str, str, str], Entry] = {
        _entry_key(e): e for e in read_entries(path)
    }
    for entry in entries:
        merged[_entry_key(entry)] = entry

    ordered = sorted(merged.values(), key=_entry_key)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ENTRY_FIELDS)
        writer.writeheader()
        for entry in ordered:
            writer.writerow({
                "date": entry.date.isoformat(),
                "side": entry.side,
                "sector": entry.sector,
                "category": entry.category,
                "amount": entry.amount,
                "currency": entry.currency,
                "amount_pct_gdp": "" if entry.amount_pct_gdp is None else entry.amount_pct_gdp,
                "certainty": entry.certainty,
                "source": entry.source,
                "source_date": entry.source_date.isoformat(),
            })


def read_entries(path: Path) -> list[Entry]:
    if not path.exists():
        return []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        entries = []
        for row in reader:
            entries.append(Entry(
                date=date.fromisoformat(row["date"]),
                side=row["side"],
                sector=row["sector"],
                category=row["category"],
                amount=float(row["amount"]),
                currency=row["currency"],
                amount_pct_gdp=float(row["amount_pct_gdp"]) if row["amount_pct_gdp"] else None,
                certainty=row["certainty"],
                source=row["source"],
                source_date=date.fromisoformat(row["source_date"]),
            ))
        return entries


def write_rates(path: Path, rates: list[ExchangeRate]) -> None:
    merged: dict[date, ExchangeRate] = {r.date: r for r in read_rates(path)}
    for rate in rates:
        merged[rate.date] = rate

    ordered = sorted(merged.values(), key=lambda r: r.date)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RATE_FIELDS)
        writer.writeheader()
        for rate in ordered:
            writer.writerow({
                "date": rate.date.isoformat(),
                "usd_to_clp": rate.usd_to_clp,
            })


def read_rates(path: Path) -> list[ExchangeRate]:
    if not path.exists():
        return []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return [
            ExchangeRate(
                date=date.fromisoformat(row["date"]),
                usd_to_clp=float(row["usd_to_clp"]),
            )
            for row in reader
        ]
