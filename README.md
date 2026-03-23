# chile-public-balance

Constructs a consolidated public balance sheet for the Chilean state by collecting data from official government sources, normalizing it into a common schema, and rendering a static site with time-series charts.

Chile does not publish a single document covering both assets and liabilities of the state. The data is spread across the Banco Central, DIPRES, Hacienda, the Contraloria, and several other institutions. This project pulls from those sources and stitches them together.

## How it works

```
collect --> normalize --> store (CSV) --> build (static HTML)
```

**Collect:** Fetch data from government APIs and structured file downloads. Each source has its own collector module.

**Normalize:** Transform raw source data into canonical balance sheet entries. Each source has a corresponding normalizer that maps its terminology and units to the shared schema.

**Store:** Write entries to CSV files under version control. Flat files, diffable, auditable.

**Build:** Read the CSV and render a self-contained HTML page with Chart.js time-series charts.

## Data model

Every row in the balance sheet follows this schema:

| Field            | Type                   | Example                               |
| ---------------- | ---------------------- | ------------------------------------- |
| `date`           | date                   | `2024-03-31`                          |
| `side`           | `asset` or `liability` | `asset`                               |
| `sector`         | string                 | `central_bank`, `central_government`  |
| `category`       | dot-path string        | `financial.international_reserves`    |
| `amount_clp`     | integer                | `35500000000000`                      |
| `amount_pct_gdp` | float or null          | `15.2`                                |
| `certainty`      | string                 | `reported`, `estimated`, `contingent` |
| `source`         | string                 | `banco_central`                       |
| `source_date`    | date                   | `2024-04-15`                          |

Categories use dot-notation for hierarchical aggregation: `financial.sovereign_funds.fees` rolls up into `financial.sovereign_funds` rolls up into `financial`.

The `certainty` field distinguishes hard numbers from estimates and contingent liabilities. This matters: Chile's net position swings by roughly 42% of GDP depending on whether you include copper reserves (+25%) and pension liabilities (-17.5%).

## Getting started

Requires Python 3.10+.

```bash
# Install
pip install -e ".[dev]"

# Run tests
pytest

# Build the static site (uses data/balance.csv)
python -m chile_balance build

# Open it
open site/index.html
```

To collect data from the Banco Central API, register at [si3.bcentral.cl](https://si3.bcentral.cl/siete/) and set your credentials:

```bash
export BCENTRAL_USER="your_email"
export BCENTRAL_PASS="your_password"
python -m chile_balance collect banco_central
```

## Data sources

### Wired

- **Banco Central BDE API** - International reserves, external debt, government sector accounts, GDP series. REST API with JSON responses. Python SDK available.

### Planned

- **DIPRES open data** - Budget execution, Treasury assets, gross debt (CSV/Excel downloads)
- **Hacienda sovereign funds** - FEES and FRP portfolio reports (PDF)
- **DIPRES contingent liabilities** - PPP guarantees, student loans, pension guarantees (PDF)
- **Contraloria IGFE** - Entity-level balance sheets for 697 public sector entities (PDF)
- **CFA fiscal statistics** - Historical fiscal variables (Excel)

## Project structure

```
src/chile_balance/
    model.py                  # Entry dataclass with validation
    store.py                  # CSV read/write
    site.py                   # Static site generator
    pipeline.py               # Collect-normalize-store orchestration
    cli.py                    # Command-line interface
    collectors/
        banco_central.py      # BDE REST API client
    normalizers/
        banco_central.py      # Raw observations to canonical entries
```

## Architecture decisions

**Python** because the data engineering ecosystem is unmatched for this domain: requests, pdfplumber, openpyxl, and an official Banco Central SDK.

**CSV under git** for storage. The dataset is small (a few thousand rows after years of operation), updates infrequently, and benefits from diffable history. No database server to manage.

**Static site** for output. Data changes monthly at most. Pre-rendered HTML with Chart.js loads instantly and costs nothing to host.

**No frameworks.** No ORM, no task queue, no web framework. The scheduling mechanism is cron. The templating mechanism is string replacement. The deployment mechanism is `cp`.
