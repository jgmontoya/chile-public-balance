from __future__ import annotations

from unittest.mock import patch

from chile_balance.cli import main


def test_cli_collect_triggers_pipeline():
    with patch("chile_balance.cli.run_collect") as mock_run:
        main(["collect"])
        mock_run.assert_called_once_with(collector=None)


def test_cli_collect_specific_collector():
    with patch("chile_balance.cli.run_collect") as mock_run:
        main(["collect", "banco_central"])
        mock_run.assert_called_once_with(collector="banco_central")


def test_cli_build_triggers_site_generation():
    with patch("chile_balance.cli.run_build") as mock_build:
        main(["build"])
        mock_build.assert_called_once()
