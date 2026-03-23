from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from chile_balance.pipeline import run_banco_central, run_exchange_rates
from chile_balance.site import build_site

load_dotenv()

DEFAULT_OUTPUT = Path("data/balance.csv")
DEFAULT_RATES = Path("data/exchange_rates.csv")
DEFAULT_SITE_OUTPUT = Path("site/index.html")

# All stored amounts are normalized to MILLIONS of their currency.
# USD series from BDE are already in millions. CLP series from national
# accounts are in "miles de millones" (billions), so scale=1000 converts
# them to CLP millions for consistency.
#
# IMPORTANT: Series are chosen to avoid double-counting.
# - "Gobierno general" (F038 sector 20) does NOT include Banco Central.
# - "Banco Central" (F038 sector 30) is separate.
# - Sovereign funds (FEES/FRP) are INCLUDED in gobierno general totals.
# - External debt overlaps with both govt and BCCh liabilities.
BANCO_CENTRAL_SERIES = [
    # ═══════════════════════════════════════════════════════════════════
    # MAIN BALANCE SHEET (totals by sector, non-overlapping)
    # ═══════════════════════════════════════════════════════════════════

    # Government general: total financial assets (quarterly, CLP billions)
    {
        "series_id": "F038.000.STO.20.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "general_government",
        "category": "financial.total",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    # Banco Central: total financial assets (quarterly, CLP billions)
    {
        "series_id": "F038.000.STO.30.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "central_bank",
        "category": "financial.total",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    # Government general: total liabilities (quarterly, CLP billions)
    {
        "series_id": "F038.000.STO.10.20.N.2018.CLP.T",
        "side": "liability",
        "sector": "general_government",
        "category": "financial.total",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    # Banco Central: total liabilities (quarterly, CLP billions)
    {
        "series_id": "F038.000.STO.10.30.N.2018.CLP.T",
        "side": "liability",
        "sector": "central_bank",
        "category": "financial.total",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },

    # ═══════════════════════════════════════════════════════════════════
    # COMPOSITION BREAKDOWN (sub-items of govt general, for detail chart)
    # These are INSIDE the totals above — do NOT sum with them.
    # ═══════════════════════════════════════════════════════════════════

    # Govt assets by instrument type
    {
        "series_id": "F038.500.STO.20.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "general_government",
        "category": "breakdown.equity",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    {
        "series_id": "F038.200.STO.20.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "general_government",
        "category": "breakdown.cash_deposits",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    {
        "series_id": "F038.300.STO.20.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "general_government",
        "category": "breakdown.securities",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    {
        "series_id": "F038.400.STO.20.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "general_government",
        "category": "breakdown.loans",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    # Govt liabilities by instrument type
    {
        "series_id": "F038.300.STO.10.20.N.2018.CLP.T",
        "side": "liability",
        "sector": "general_government",
        "category": "breakdown.bonds",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    {
        "series_id": "F038.400.STO.10.20.N.2018.CLP.T",
        "side": "liability",
        "sector": "general_government",
        "category": "breakdown.loans",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },
    {
        "series_id": "F038.700.STO.10.20.N.2018.CLP.T",
        "side": "liability",
        "sector": "general_government",
        "category": "breakdown.other",
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    },

    # ═══════════════════════════════════════════════════════════════════
    # RATIOS (% of GDP, pre-computed by Banco Central)
    # ═══════════════════════════════════════════════════════════════════

    {
        "series_id": "F038.999.PPB2.20.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "general_government",
        "category": "ratio.net_financial_assets_pct_gdp",
        "currency": "CLP",
        "certainty": "reported",
        "source": "banco_central",
    },
    {
        "series_id": "F038.CNF.PPB2.20.10.N.2018.CLP.T",
        "side": "asset",
        "sector": "general_government",
        "category": "ratio.fiscal_balance_pct_gdp",
        "currency": "CLP",
        "certainty": "reported",
        "source": "banco_central",
    },
]


def _get_credentials() -> tuple[str, str]:
    user = os.environ.get("BCENTRAL_USER", "")
    password = os.environ.get("BCENTRAL_PASS", "")
    if not user or not password:
        raise SystemExit(
            "Set BCENTRAL_USER and BCENTRAL_PASS environment variables"
        )
    return user, password


def run_collect(collector: str | None = None) -> None:
    user, password = _get_credentials()
    today = date.today()

    collectors_to_run = ["banco_central"] if collector is None else [collector]

    for name in collectors_to_run:
        if name == "banco_central":
            configs = []
            for s in BANCO_CENTRAL_SERIES:
                config = dict(s)
                config["source_date"] = today
                configs.append(config)

            DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            run_banco_central(
                user=user,
                password=password,
                series_configs=configs,
                output_path=DEFAULT_OUTPUT,
                first_date="1982-01-01",
                last_date=today.isoformat(),
            )

            run_exchange_rates(
                user=user,
                password=password,
                rates_path=DEFAULT_RATES,
                first_date="1982-01-01",
                last_date=today.isoformat(),
            )
        else:
            raise SystemExit(f"Unknown collector: {name}")


def run_build() -> None:
    build_site(DEFAULT_OUTPUT, DEFAULT_RATES, DEFAULT_SITE_OUTPUT)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="chile-balance")
    subparsers = parser.add_subparsers(dest="command")

    collect_parser = subparsers.add_parser("collect", help="Run data collectors")
    collect_parser.add_argument(
        "collector",
        nargs="?",
        default=None,
        help="Specific collector to run (e.g. banco_central)",
    )

    subparsers.add_parser("build", help="Build static site from collected data")

    args = parser.parse_args(argv)

    if args.command == "collect":
        run_collect(collector=args.collector)
    elif args.command == "build":
        run_build()
    else:
        parser.print_help()
