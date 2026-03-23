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


def write_entries(path: Path, entries: list[Entry]) -> None:
    write_header = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ENTRY_FIELDS)
        if write_header:
            writer.writeheader()
        for entry in entries:
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
    write_header = not path.exists() or path.stat().st_size == 0
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RATE_FIELDS)
        if write_header:
            writer.writeheader()
        for rate in rates:
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
