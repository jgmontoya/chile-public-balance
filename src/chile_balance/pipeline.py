from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from math import isnan
from pathlib import Path
from typing import Any

from chile_balance.collectors.banco_central import fetch_series
from chile_balance.model import ExchangeRate
from chile_balance.normalizers.banco_central import normalize
from chile_balance.store import write_entries, write_rates

EXCHANGE_RATE_SERIES = "F073.TCO.PRE.Z.D"


def run_banco_central(
    user: str,
    password: str,
    series_configs: list[dict[str, Any]],
    output_path: Path,
    first_date: str,
    last_date: str,
) -> None:
    for config in series_configs:
        series_id = config["series_id"]
        metadata = {k: v for k, v in config.items() if k != "series_id"}

        observations = fetch_series(
            user=user,
            password=password,
            series_id=series_id,
            first_date=first_date,
            last_date=last_date,
        )

        entries = normalize(observations, metadata)
        write_entries(output_path, entries)


def run_exchange_rates(
    user: str,
    password: str,
    rates_path: Path,
    first_date: str,
    last_date: str,
) -> None:
    observations = fetch_series(
        user=user,
        password=password,
        series_id=EXCHANGE_RATE_SERIES,
        first_date=first_date,
        last_date=last_date,
    )

    rates = []
    for obs in observations:
        value = float(obs.value)
        if not isnan(value):
            rates.append(ExchangeRate(date=obs.date, usd_to_clp=value))

    write_rates(rates_path, rates)
