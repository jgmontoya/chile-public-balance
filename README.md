# chile-public-balance

Constructs a consolidated public balance sheet for the Chilean state by collecting data from official government sources, normalizing it into a common schema, and rendering a static site with time-series charts.

Chile does not publish a single document covering both assets and liabilities of the state. The data is spread across the Banco Central, DIPRES, Hacienda, the Contraloria, and several other institutions. This project pulls from those sources and stitches them together.

**Live site:** [jgmontoya.github.io/chile-public-balance](https://jgmontoya.github.io/chile-public-balance)

## How it works

```
collect --> normalize --> store (CSV) --> build (static HTML)
```

**Collect:** Fetch data from the Banco Central BDE REST API. Each source has its own collector module.

**Normalize:** Transform raw API responses into canonical balance sheet entries. Scale and unit conversion happens here.

**Store:** Write entries to CSV files under version control. Flat files, diffable, auditable.

**Build:** Read the CSV, compute dual-currency views (USD/CLP), and render a self-contained HTML page with Chart.js charts.

## Data model

Every row in the balance sheet follows this schema:

| Field            | Type                   | Example                            |
| ---------------- | ---------------------- | ---------------------------------- |
| `date`           | date                   | `2024-03-31`                       |
| `side`           | `asset` or `liability` | `asset`                            |
| `sector`         | string                 | `central_bank`, `general_government` |
| `category`       | dot-path string        | `financial.total`                  |
| `amount`         | float                  | `100685.12`                        |
| `currency`       | `CLP`, `USD`, `UF`    | `CLP`                              |
| `amount_pct_gdp` | float or null          | `15.2`                             |
| `certainty`      | string                 | `reported`, `estimated`, `contingent` |
| `source`         | string                 | `banco_central`                    |
| `source_date`    | date                   | `2024-04-15`                       |

Categories use dot-notation prefixes to route data to different charts:
- `financial.total` -- main balance sheet chart
- `breakdown.*` -- asset/liability composition charts
- `ratio.*` -- fiscal indicator charts (% of GDP)
- `context.*` -- contextual data (copper price)

## What it shows

- **Balance sheet:** Government general + Central Bank assets vs liabilities over time (quarterly, from 2002)
- **Composition:** Government assets by type (equity, cash, securities, loans) and liabilities by maturity (short/long-term bonds, loans)
- **Fiscal indicators:** Net financial assets, fiscal balance, and government debt as % of GDP
- **Copper price:** Monthly from 1960, the key driver of Chilean fiscal health
- **Presidential terms:** Background bands showing each administration
- **Controls:** USD/CLP toggle, date range filter with presets (1Y/5Y/10Y/20Y), EN/ES language toggle, dark mode

## Getting started

Requires Python 3.10+.

```bash
pip install -e ".[dev]"
pytest
python -m chile_balance build
open site/index.html
```

To collect fresh data from the Banco Central API, register at [si3.bcentral.cl](https://si3.bcentral.cl/siete/), activate API access, and set credentials in `.env`:

```
BCENTRAL_USER=your_email
BCENTRAL_PASS=your_password
```

Then run:

```bash
python -m chile_balance collect
python -m chile_balance build
```

## Data sources

### Active

- **Banco Central BDE API** -- 16 series covering balance sheet totals, composition breakdowns, fiscal ratios, exchange rates, and copper price. Quarterly and monthly data, some series back to 1960.

### Planned

- **DIPRES open data** -- Budget execution, Treasury assets, gross debt (CSV/Excel)
- **DIPRES contingent liabilities** -- PPP guarantees, student loans, pension guarantees (PDF)
- **Contraloria IGFE** -- Entity-level balance sheets for 697 public sector entities (PDF)

## Project structure

```
src/chile_balance/
    model.py              # Entry and ExchangeRate dataclasses
    store.py              # CSV read/write
    site.py               # Data preparation for charts
    pipeline.py           # Collect-normalize-store orchestration
    cli.py                # Command-line interface
    series_config.py      # BDE API series definitions
    collectors/
        banco_central.py  # BDE REST API client
    normalizers/
        banco_central.py  # Raw observations to canonical entries
    templates/
        page.html         # HTML shell with CSS
        charts.js         # Chart rendering and interactivity
        controls.html     # Filter controls and chart containers
        empty.html        # Empty state
```

## Deployment

The site auto-deploys to GitHub Pages every Monday via GitHub Actions. The workflow collects fresh data, runs tests, commits updated CSVs, and deploys the built site.
