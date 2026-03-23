from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from chile_balance.pipeline import run_banco_central, run_exchange_rates
from chile_balance.series_config import BANCO_CENTRAL_SERIES
from chile_balance.site import build_site

load_dotenv()

DEFAULT_OUTPUT = Path("data/balance.csv")
DEFAULT_RATES = Path("data/exchange_rates.csv")
DEFAULT_SITE_OUTPUT = Path("site/index.html")


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
