from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

import requests

BASE_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"


@dataclass(frozen=True)
class Observation:
    date: date
    value: Decimal


def fetch_series(
    user: str,
    password: str,
    series_id: str,
    first_date: str,
    last_date: str,
) -> list[Observation]:
    params = {
        "user": user,
        "pass": password,
        "function": "GetSeries",
        "timeseries": series_id,
        "firstdate": first_date,
        "lastdate": last_date,
    }

    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    code = data.get("Codigo", 0)
    if code != 0:
        desc = data.get("Descripcion", "Unknown error")
        raise RuntimeError(f"BDE API error {code}: {desc}")

    obs_list = data.get("Series", {}).get("Obs") or []

    observations = []
    for obs in obs_list:
        raw_value = obs["value"]
        if raw_value in ("NaN", "nan", "", None):
            continue
        parsed_date = datetime.strptime(obs["indexDateString"], "%d-%m-%Y").date()
        value = Decimal(raw_value)
        observations.append(Observation(date=parsed_date, value=value))

    return observations
