from __future__ import annotations

from datetime import date

import responses

from chile_balance.pipeline import run_banco_central
from chile_balance.store import read_entries


SAMPLE_RESPONSE = {
    "Codigo": 0,
    "Descripcion": "Success",
    "Series": {
        "Obs": [
            {"indexDateString": "01-01-2024", "value": "37438.37"},
            {"indexDateString": "01-02-2024", "value": "36153.84"},
        ]
    },
}


@responses.activate
def test_pipeline_collects_normalizes_and_stores(tmp_path):
    responses.add(
        responses.GET,
        "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx",
        json=SAMPLE_RESPONSE,
        status=200,
    )

    csv_file = tmp_path / "balance.csv"
    series_config = {
        "series_id": "F062.A5.STO.PF.USD.M",
        "side": "asset",
        "sector": "central_bank",
        "category": "financial.international_reserves",
        "currency": "USD",
        "certainty": "reported",
        "source": "banco_central",
        "source_date": date(2024, 3, 1),
    }

    run_banco_central(
        user="test_user",
        password="test_pass",
        series_configs=[series_config],
        output_path=csv_file,
        first_date="2024-01-01",
        last_date="2024-02-01",
    )

    entries = read_entries(csv_file)
    assert len(entries) == 2
    assert entries[0].date == date(2024, 1, 1)
    assert entries[0].amount == 37438.37
    assert entries[0].currency == "USD"
    assert entries[1].date == date(2024, 2, 1)
    assert entries[1].amount == 36153.84
