"""Series configuration for Banco Central data collection.

All stored amounts are normalized to MILLIONS of their currency.
USD series from BDE are already in millions. CLP series from national
accounts are in "miles de millones" (billions), so scale=1000 converts
them to CLP millions for consistency.

IMPORTANT: Series are chosen to avoid double-counting.
- "Gobierno general" (F038 sector 20) does NOT include Banco Central.
- "Banco Central" (F038 sector 30) is separate.
- Sovereign funds (FEES/FRP) are INCLUDED in gobierno general totals.
- External debt overlaps with both govt and BCCh liabilities.
"""

from __future__ import annotations


_DROP = object()  # sentinel to remove a default key


def _f038(
    series_id: str, side: str, sector: str, category: str, **overrides: object
) -> dict:
    """Build an F038 series config with common defaults.

    Pass ``key=_DROP`` to omit a default key entirely (e.g. ``scale=_DROP``
    for ratio series that should not be scaled).
    """
    base = {
        "series_id": series_id,
        "side": side,
        "sector": sector,
        "category": category,
        "currency": "CLP",
        "scale": 1000,
        "certainty": "reported",
        "source": "banco_central",
    }
    base.update(overrides)
    return {k: v for k, v in base.items() if v is not _DROP}


BANCO_CENTRAL_SERIES = [
    # ═══════════════════════════════════════════════════════════════════
    # MAIN BALANCE SHEET (totals by sector, non-overlapping)
    # ═══════════════════════════════════════════════════════════════════

    # Government general: total financial assets (quarterly, CLP billions)
    _f038("F038.000.STO.20.10.N.2018.CLP.T", "asset", "general_government", "financial.total"),
    # Banco Central: total financial assets (quarterly, CLP billions)
    _f038("F038.000.STO.30.10.N.2018.CLP.T", "asset", "central_bank", "financial.total"),
    # Government general: total liabilities (quarterly, CLP billions)
    _f038("F038.000.STO.10.20.N.2018.CLP.T", "liability", "general_government", "financial.total"),
    # Banco Central: total liabilities (quarterly, CLP billions)
    _f038("F038.000.STO.10.30.N.2018.CLP.T", "liability", "central_bank", "financial.total"),

    # ═══════════════════════════════════════════════════════════════════
    # COMPOSITION BREAKDOWN (sub-items of govt general, for detail chart)
    # These are INSIDE the totals above — do NOT sum with them.
    # ═══════════════════════════════════════════════════════════════════

    # Govt assets by instrument type
    _f038("F038.500.STO.20.10.N.2018.CLP.T", "asset", "general_government", "breakdown.equity"),
    _f038("F038.200.STO.20.10.N.2018.CLP.T", "asset", "general_government", "breakdown.cash_deposits"),
    _f038("F038.300.STO.20.10.N.2018.CLP.T", "asset", "general_government", "breakdown.securities"),
    _f038("F038.400.STO.20.10.N.2018.CLP.T", "asset", "general_government", "breakdown.loans"),
    _f038("F038.700.STO.20.10.N.2018.CLP.T", "asset", "general_government", "breakdown.other"),
    # Govt liabilities by instrument type
    _f038("F038.300.STO.10.20.N.2018.CLP.T", "liability", "general_government", "breakdown.bonds"),
    _f038("F038.400.STO.10.20.N.2018.CLP.T", "liability", "general_government", "breakdown.loans"),
    _f038("F038.700.STO.10.20.N.2018.CLP.T", "liability", "general_government", "breakdown.other"),

    # ═══════════════════════════════════════════════════════════════════
    # RATIOS (% of GDP, pre-computed by Banco Central)
    # ═══════════════════════════════════════════════════════════════════

    _f038(
        "F038.999.PPB2.20.10.N.2018.CLP.T", "asset", "general_government",
        "ratio.net_financial_assets_pct_gdp", scale=_DROP,
    ),
    _f038(
        "F038.CNF.PPB2.20.10.N.2018.CLP.T", "asset", "general_government",
        "ratio.fiscal_balance_pct_gdp", scale=_DROP,
    ),
]
