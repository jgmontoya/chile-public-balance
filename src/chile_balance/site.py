from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from chile_balance.model import Entry, ExchangeRate
from chile_balance.store import read_entries, read_rates

_TEMPLATES = Path(__file__).parent / "templates"


def _read_template(name: str) -> str:
    return (_TEMPLATES / name).read_text()


def _build_rate_lookup(rates: list[ExchangeRate]) -> dict[str, float]:
    """Map YYYY-MM to the last known exchange rate for that month."""
    monthly: dict[str, float] = {}
    for rate in sorted(rates, key=lambda r: r.date):
        key = rate.date.strftime("%Y-%m")
        monthly[key] = rate.usd_to_clp
    return monthly


def _convert_amount(amount: float, currency: str, target: str, rate: float | None) -> float:
    if currency == target:
        return amount
    if rate is None:
        return 0.0
    if currency == "USD" and target == "CLP":
        return amount * rate
    if currency == "CLP" and target == "USD":
        return amount / rate
    return amount


def _forward_fill(sparse: dict[date, float], timeline: list[date]) -> list[float]:
    """Fill gaps in a sparse time series by carrying the last known value forward."""
    result = []
    last = 0.0
    for d in timeline:
        if d in sparse:
            last = sparse[d]
        result.append(last)
    return result


def prepare_chart_data(
    entries: list[Entry],
    rates: list[ExchangeRate] | None = None,
) -> dict[str, Any]:
    rate_lookup = _build_rate_lookup(rates) if rates else {}

    # Group entries by (side, sector, category) — each is a distinct time series
    SeriesKey = tuple[str, str, str, str]  # (side, sector, category, currency)
    series: dict[SeriesKey, dict[date, float]] = defaultdict(dict)

    for entry in entries:
        if entry.category.startswith(("breakdown.", "ratio.", "context.")):
            continue
        key = (entry.side, entry.sector, entry.category, entry.currency)
        series[key][entry.date] = entry.amount

    # Build the full monthly timeline from all dates across all series
    all_dates: set[date] = set()
    for points in series.values():
        all_dates.update(points.keys())
    timeline = sorted(all_dates)

    if not timeline:
        return {
            "labels": [],
            "USD": {"assets": [], "liabilities": []},
            "CLP": {"assets": [], "liabilities": []},
        }

    # Forward-fill each series, convert to both currencies, then sum by side
    usd_assets = [0.0] * len(timeline)
    usd_liabilities = [0.0] * len(timeline)
    clp_assets = [0.0] * len(timeline)
    clp_liabilities = [0.0] * len(timeline)

    for (side, sector, category, currency), sparse in series.items():
        filled = _forward_fill(sparse, timeline)

        for i, d in enumerate(timeline):
            month_key = d.strftime("%Y-%m")
            rate = rate_lookup.get(month_key)

            usd_val = _convert_amount(filled[i], currency, "USD", rate)
            clp_val = _convert_amount(filled[i], currency, "CLP", rate)

            if side == "asset":
                usd_assets[i] += usd_val
                clp_assets[i] += clp_val
            elif side == "liability":
                usd_liabilities[i] += usd_val
                clp_liabilities[i] += clp_val

    return {
        "labels": [d.isoformat() for d in timeline],
        "USD": {
            "assets": [round(v, 2) for v in usd_assets],
            "liabilities": [round(v, 2) for v in usd_liabilities],
            "net": [round(a - l, 2) for a, l in zip(usd_assets, usd_liabilities)],
        },
        "CLP": {
            "assets": [round(v, 2) for v in clp_assets],
            "liabilities": [round(v, 2) for v in clp_liabilities],
            "net": [round(a - l, 2) for a, l in zip(clp_assets, clp_liabilities)],
        },
    }


def prepare_breakdown_data(
    entries: list[Entry],
    rates: list[ExchangeRate] | None = None,
) -> dict[str, Any]:
    rate_lookup = _build_rate_lookup(rates) if rates else {}
    breakdown_entries = [e for e in entries if e.category.startswith("breakdown.")]

    # Group by (side, label) with currency info
    SKey = tuple[str, str, str]  # (side, label, currency)
    series: dict[SKey, dict[date, float]] = defaultdict(dict)

    for entry in breakdown_entries:
        label = entry.category.removeprefix("breakdown.")
        series[(entry.side, label, entry.currency)][entry.date] = entry.amount

    all_dates: set[date] = set()
    for points in series.values():
        all_dates.update(points.keys())
    timeline = sorted(all_dates)

    def build_for_currency(target: str) -> dict[str, dict[str, list[float]]]:
        assets: dict[str, list[float]] = {}
        liabilities: dict[str, list[float]] = {}
        for (side, label, currency), sparse in sorted(series.items()):
            filled = _forward_fill(sparse, timeline)
            converted = []
            for i, d in enumerate(timeline):
                rate = rate_lookup.get(d.strftime("%Y-%m"))
                converted.append(round(_convert_amount(filled[i], currency, target, rate), 2))
            target_dict = assets if side == "asset" else liabilities
            target_dict[label] = converted
        return {"assets": assets, "liabilities": liabilities}

    return {
        "labels": [d.isoformat() for d in timeline],
        "USD": build_for_currency("USD"),
        "CLP": build_for_currency("CLP"),
    }


def prepare_ratio_data(entries: list[Entry]) -> dict[str, Any]:
    ratio_entries = [e for e in entries if e.category.startswith("ratio.")]

    series: dict[str, dict[date, float]] = defaultdict(dict)
    for entry in ratio_entries:
        label = entry.category.removeprefix("ratio.")
        series[label][entry.date] = entry.amount

    all_dates: set[date] = set()
    for points in series.values():
        all_dates.update(points.keys())
    timeline = sorted(all_dates)

    result: dict[str, Any] = {"labels": [d.isoformat() for d in timeline]}
    for label, sparse in sorted(series.items()):
        result[label] = [round(v, 2) for v in _forward_fill(sparse, timeline)]

    return result


def prepare_context_data(
    entries: list[Entry],
    rates: list[ExchangeRate] | None = None,
) -> dict[str, Any]:
    rate_lookup = _build_rate_lookup(rates) if rates else {}
    context_entries = [e for e in entries if e.category.startswith("context.")]

    # Track currency per series
    series: dict[str, dict[date, float]] = defaultdict(dict)
    currencies: dict[str, str] = {}
    for entry in context_entries:
        label = entry.category.removeprefix("context.")
        series[label][entry.date] = entry.amount
        currencies[label] = entry.currency

    all_dates: set[date] = set()
    for points in series.values():
        all_dates.update(points.keys())
    timeline = sorted(all_dates)

    def build_for_currency(target: str) -> dict[str, list[float]]:
        result = {}
        for label, sparse in sorted(series.items()):
            filled = _forward_fill(sparse, timeline)
            converted = []
            for i, d in enumerate(timeline):
                rate = rate_lookup.get(d.strftime("%Y-%m"))
                converted.append(round(_convert_amount(filled[i], currencies[label], target, rate), 4))
            result[label] = converted
        return result

    return {
        "labels": [d.isoformat() for d in timeline],
        "USD": build_for_currency("USD"),
        "CLP": build_for_currency("CLP"),
    }


def build_site(data_path: Path, rates_path: Path, output_path: Path) -> None:
    from datetime import datetime

    entries = read_entries(data_path)
    rates = read_rates(rates_path)
    chart_data = prepare_chart_data(entries, rates)
    breakdown_data = prepare_breakdown_data(entries, rates)
    ratio_data = prepare_ratio_data(entries)
    context_data = prepare_context_data(entries, rates)

    has_data = len(chart_data["labels"]) > 0

    last_date = chart_data["labels"][-1] if has_data else ""
    updated_text = f'<span style="margin-left: 0.5rem; color: #9ca3af;">Data through {last_date}. Built {datetime.now().strftime("%Y-%m-%d")}.</span>' if has_data else ""

    all_data = json.dumps({
        "balance": chart_data,
        "breakdown": breakdown_data,
        "ratios": ratio_data,
        "context": context_data,
    })

    html = _read_template("page.html")
    chart_script = _read_template("charts.js")
    canvas_html = _read_template("controls.html")
    empty_html = _read_template("empty.html")

    html = html.replace("CHART_DATA", all_data)
    html = html.replace("CHART_CONTENT", canvas_html if has_data else empty_html)
    html = html.replace("CHART_SCRIPT", chart_script if has_data else "")
    html = html.replace("LAST_UPDATED", updated_text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
