from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest
import responses
from requests.exceptions import HTTPError

from chile_balance.collectors.banco_central import fetch_series, Observation


SAMPLE_RESPONSE = {
    "Codigo": 0,
    "Descripcion": "OK",
    "Series": {
        "Obs": [
            {"indexDateString": "01-01-2024", "value": "12345.67"},
            {"indexDateString": "01-02-2024", "value": "12456.78"},
        ]
    },
}


@responses.activate
def test_fetch_series_returns_parsed_observations():
    responses.add(
        responses.GET,
        "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx",
        json=SAMPLE_RESPONSE,
        status=200,
    )

    result = fetch_series(
        user="test_user",
        password="test_pass",
        series_id="F032.PIB.FLU.R.CLP.EP18.Z.Z.0.T110",
        first_date="2024-01-01",
        last_date="2024-02-01",
    )

    assert len(result) == 2
    assert result[0] == Observation(date=date(2024, 1, 1), value=Decimal("12345.67"))
    assert result[1] == Observation(date=date(2024, 2, 1), value=Decimal("12456.78"))


@responses.activate
def test_fetch_series_raises_on_http_error():
    responses.add(
        responses.GET,
        "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx",
        json={"error": "Unauthorized"},
        status=401,
    )

    with pytest.raises(HTTPError):
        fetch_series(
            user="bad_user",
            password="bad_pass",
            series_id="FAKE.SERIES",
            first_date="2024-01-01",
            last_date="2024-02-01",
        )


@responses.activate
def test_fetch_series_constructs_correct_url():
    responses.add(
        responses.GET,
        "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx",
        json=SAMPLE_RESPONSE,
        status=200,
    )

    fetch_series(
        user="my_user",
        password="my_pass",
        series_id="F032.PIB.FLU.R.CLP.EP18.Z.Z.0.T110",
        first_date="2024-01-01",
        last_date="2024-12-31",
    )

    assert len(responses.calls) == 1
    request = responses.calls[0].request
    assert "user=my_user" in request.url
    assert "pass=my_pass" in request.url
    assert "timeseries=F032.PIB.FLU.R.CLP.EP18.Z.Z.0.T110" in request.url
    assert "firstdate=2024-01-01" in request.url
    assert "lastdate=2024-12-31" in request.url
    assert "function=GetSeries" in request.url


@responses.activate
def test_fetch_series_raises_on_api_error_code():
    responses.add(
        responses.GET,
        "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx",
        json={
            "Codigo": -5,
            "Descripcion": "Invalid username or password",
            "Series": {"Obs": None},
        },
        status=200,
    )

    with pytest.raises(RuntimeError, match="BDE API error -5"):
        fetch_series(
            user="bad_user",
            password="bad_pass",
            series_id="FAKE.SERIES",
            first_date="2024-01-01",
            last_date="2024-02-01",
        )
