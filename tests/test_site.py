from __future__ import annotations

from datetime import date

from chile_balance.model import Entry, ExchangeRate
from chile_balance.site import build_site, prepare_chart_data
from chile_balance.store import write_entries, write_rates


def _entry(d: date, side: str, amount: float, currency: str = "USD", category: str = "test") -> Entry:
    return Entry(
        date=d,
        side=side,
        sector="central_government",
        category=category,
        amount=amount,
        currency=currency,
        amount_pct_gdp=None,
        certainty="reported",
        source="test",
        source_date=d,
    )


def test_prepare_chart_data_aggregates_by_date_and_side():
    entries = [
        _entry(date(2024, 1, 1), "asset", 100.0, category="reserves"),
        _entry(date(2024, 1, 1), "asset", 200.0, category="funds"),
        _entry(date(2024, 1, 1), "liability", 150.0),
        _entry(date(2024, 6, 1), "asset", 120.0, category="reserves"),
        _entry(date(2024, 6, 1), "asset", 250.0, category="funds"),
        _entry(date(2024, 6, 1), "liability", 300.0),
    ]

    result = prepare_chart_data(entries)

    assert result["labels"] == ["2024-01-01", "2024-06-01"]
    assert result["USD"]["assets"] == [300.0, 370.0]
    assert result["USD"]["liabilities"] == [150.0, 300.0]


def test_prepare_chart_data_with_no_entries():
    result = prepare_chart_data([])

    assert result["labels"] == []
    assert result["USD"]["assets"] == []
    assert result["USD"]["liabilities"] == []


def test_prepare_chart_data_forward_fills_across_gaps():
    entries = [
        _entry(date(2024, 1, 1), "asset", 500.0),
        _entry(date(2024, 6, 1), "liability", 300.0),
    ]

    result = prepare_chart_data(entries)

    assert result["labels"] == ["2024-01-01", "2024-06-01"]
    # Asset is forward-filled from Jan to Jun (still 500)
    assert result["USD"]["assets"] == [500.0, 500.0]
    # Liability had no value in Jan, so 0 until Jun
    assert result["USD"]["liabilities"] == [0, 300.0]


def test_prepare_chart_data_converts_usd_to_clp_with_rates():
    entries = [
        _entry(date(2024, 1, 1), "asset", 1000.0, "USD"),
    ]
    rates = [
        ExchangeRate(date=date(2024, 1, 15), usd_to_clp=900.0),
    ]

    result = prepare_chart_data(entries, rates)

    assert result["USD"]["assets"] == [1000.0]
    assert result["CLP"]["assets"] == [900000.0]


def test_prepare_chart_data_excludes_breakdown_and_ratio_categories():
    entries = [
        _entry(date(2024, 1, 1), "asset", 1000.0, category="financial.total"),
        _entry(date(2024, 1, 1), "asset", 500.0, category="breakdown.equity"),
        _entry(date(2024, 1, 1), "asset", 99.0, category="ratio.net_financial_assets_pct_gdp"),
    ]

    result = prepare_chart_data(entries)

    # Only financial.total should be in the main chart
    assert result["USD"]["assets"] == [1000.0]


def test_prepare_breakdown_data_groups_by_category():
    from chile_balance.site import prepare_breakdown_data

    entries = [
        _entry(date(2024, 1, 1), "asset", 500.0, category="breakdown.equity"),
        _entry(date(2024, 1, 1), "asset", 300.0, category="breakdown.cash_deposits"),
        _entry(date(2024, 1, 1), "liability", 800.0, category="breakdown.bonds"),
        _entry(date(2024, 6, 1), "asset", 550.0, category="breakdown.equity"),
        _entry(date(2024, 6, 1), "asset", 320.0, category="breakdown.cash_deposits"),
        _entry(date(2024, 6, 1), "liability", 850.0, category="breakdown.bonds"),
    ]

    result = prepare_breakdown_data(entries)

    assert result["labels"] == ["2024-01-01", "2024-06-01"]
    # USD view (native currency, no conversion needed)
    assert "equity" in result["USD"]["assets"]
    assert result["USD"]["assets"]["equity"] == [500.0, 550.0]
    assert result["USD"]["assets"]["cash_deposits"] == [300.0, 320.0]
    assert "bonds" in result["USD"]["liabilities"]
    assert result["USD"]["liabilities"]["bonds"] == [800.0, 850.0]


def test_prepare_ratio_data_extracts_ratio_series():
    from chile_balance.site import prepare_ratio_data

    entries = [
        _entry(date(2024, 1, 1), "asset", -12.5, category="ratio.net_financial_assets_pct_gdp"),
        _entry(date(2024, 1, 1), "asset", -2.1, category="ratio.fiscal_balance_pct_gdp"),
        _entry(date(2024, 6, 1), "asset", -14.0, category="ratio.net_financial_assets_pct_gdp"),
        _entry(date(2024, 6, 1), "asset", -1.8, category="ratio.fiscal_balance_pct_gdp"),
    ]

    result = prepare_ratio_data(entries)

    assert result["labels"] == ["2024-01-01", "2024-06-01"]
    assert result["net_financial_assets_pct_gdp"] == [-12.5, -14.0]
    assert result["fiscal_balance_pct_gdp"] == [-2.1, -1.8]


def test_prepare_context_data_returns_multiple_series():
    from chile_balance.site import prepare_context_data

    entries = [
        _entry(date(2024, 1, 1), "asset", 4.5, category="context.copper_price_usd_lb"),
        _entry(date(2024, 1, 1), "asset", 5000.0, category="context.fees_usd"),
        _entry(date(2024, 1, 1), "asset", 8000.0, category="context.frp_usd"),
        _entry(date(2024, 6, 1), "asset", 4.8, category="context.copper_price_usd_lb"),
        _entry(date(2024, 6, 1), "asset", 5500.0, category="context.fees_usd"),
        _entry(date(2024, 6, 1), "asset", 8200.0, category="context.frp_usd"),
    ]

    result = prepare_context_data(entries)

    assert result["labels"] == ["2024-01-01", "2024-06-01"]
    assert result["USD"]["copper_price_usd_lb"] == [4.5, 4.8]
    assert result["USD"]["fees_usd"] == [5000.0, 5500.0]
    assert result["USD"]["frp_usd"] == [8000.0, 8200.0]


def test_build_site_produces_html_with_currency_toggle(tmp_path):
    csv_file = tmp_path / "balance.csv"
    rates_file = tmp_path / "rates.csv"
    entries = [
        _entry(date(2024, 1, 1), "asset", 1000.0),
        _entry(date(2024, 1, 1), "liability", 500.0),
    ]
    write_entries(csv_file, entries)
    write_rates(rates_file, [ExchangeRate(date=date(2024, 1, 15), usd_to_clp=900.0)])

    output = tmp_path / "index.html"
    build_site(csv_file, rates_file, output)

    html = output.read_text()
    assert "<!DOCTYPE html>" in html
    assert "currency-btn" in html
    assert "USD" in html
    assert "CLP" in html
    assert "1000" in html
    assert "dateFrom" in html
    assert "dateTo" in html
    assert "preset-btn" in html
    assert "assetBreakdownChart" in html
    assert "liabilityBreakdownChart" in html
    assert "ratioChart" in html
    assert "data-table" in html
    assert "theme-btn" in html


def test_build_site_includes_sovereign_fund_chart(tmp_path):
    csv_file = tmp_path / "balance.csv"
    rates_file = tmp_path / "rates.csv"
    entries = [
        _entry(date(2024, 1, 1), "asset", 1000.0),
        _entry(date(2024, 1, 1), "liability", 500.0),
    ]
    write_entries(csv_file, entries)
    write_rates(rates_file, [ExchangeRate(date=date(2024, 1, 15), usd_to_clp=900.0)])

    output = tmp_path / "index.html"
    build_site(csv_file, rates_file, output)

    html = output.read_text()
    assert "sovereignFundChart" in html


def test_build_site_with_no_data_shows_empty_state(tmp_path):
    csv_file = tmp_path / "balance.csv"
    rates_file = tmp_path / "rates.csv"
    output = tmp_path / "index.html"

    build_site(csv_file, rates_file, output)

    html = output.read_text()
    assert "No data yet" in html
    assert "balanceChart" not in html
