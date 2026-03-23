from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from chile_balance.model import Entry, ExchangeRate
from chile_balance.store import read_entries, read_rates

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chile Public Balance Sheet</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 960px;
            margin: 0 auto;
            padding: 2rem 1rem;
            color: #1a1a1a;
            background: #fafafa;
        }
        h1 { font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }
        .subtitle { color: #666; font-size: 0.875rem; margin-bottom: 1.5rem; }
        .sticky-controls {
            position: sticky;
            top: 0;
            z-index: 10;
            background: #fafafa;
            padding: 0.75rem 0;
            border-bottom: 1px solid transparent;
            transition: border-color 0.15s;
        }
        .sticky-controls.scrolled {
            border-bottom-color: #e5e7eb;
        }
        .controls {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .controls button {
            padding: 0.375rem 0.75rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            background: white;
            cursor: pointer;
            font-size: 0.8125rem;
            color: #374151;
            transition: all 0.15s;
        }
        .controls button.active {
            background: #1a1a1a;
            color: white;
            border-color: #1a1a1a;
        }
        .date-controls {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        .date-controls input[type="date"] {
            padding: 0.375rem 0.5rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 0.8125rem;
            color: #374151;
            background: white;
        }
        .date-controls .separator {
            color: #9ca3af;
            font-size: 0.8125rem;
        }
        .presets {
            display: flex;
            gap: 0.25rem;
            margin-left: 0.5rem;
        }
        .presets button {
            padding: 0.25rem 0.5rem;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            background: white;
            cursor: pointer;
            font-size: 0.75rem;
            color: #374151;
            transition: all 0.15s;
        }
        .presets button.active {
            background: #1a1a1a;
            color: white;
            border-color: #1a1a1a;
        }
        .chart-container {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        .empty-state {
            text-align: center;
            padding: 4rem 1rem;
            color: #999;
        }
        .section-title {
            font-size: 1.125rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 0.75rem;
        }
        .chart-stack {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
    </style>
</head>
<body>
    <h1>Chile Public Balance Sheet</h1>
    <p class="subtitle">Assets and liabilities of the Chilean state over time</p>
    CHART_CONTENT
    <script>
    const DATA = CHART_DATA;
    CHART_SCRIPT
    </script>
</body>
</html>
"""

CHART_SCRIPT = """\
var PRESIDENTS = [
    {name: 'Lagos', start: '2000-03-11', end: '2006-03-11', color: 'rgba(239, 68, 68, 0.07)'},
    {name: 'Bachelet I', start: '2006-03-11', end: '2010-03-11', color: 'rgba(234, 179, 8, 0.07)'},
    {name: 'Piñera I', start: '2010-03-11', end: '2014-03-11', color: 'rgba(59, 130, 246, 0.07)'},
    {name: 'Bachelet II', start: '2014-03-11', end: '2018-03-11', color: 'rgba(234, 179, 8, 0.07)'},
    {name: 'Piñera II', start: '2018-03-11', end: '2022-03-11', color: 'rgba(59, 130, 246, 0.07)'},
    {name: 'Boric', start: '2022-03-11', end: '2026-03-11', color: 'rgba(239, 68, 68, 0.07)'},
    {name: 'Kast', start: '2026-03-11', end: '2030-03-11', color: 'rgba(59, 130, 246, 0.07)'},
];

var BREAKDOWN_COLORS = {
    equity:        {border: '#7c3aed', bg: 'rgba(124, 58, 237, 0.6)'},
    cash_deposits: {border: '#0891b2', bg: 'rgba(8, 145, 178, 0.6)'},
    securities:    {border: '#2563eb', bg: 'rgba(37, 99, 235, 0.6)'},
    loans:         {border: '#059669', bg: 'rgba(5, 150, 105, 0.6)'},
    bonds:         {border: '#dc2626', bg: 'rgba(220, 38, 38, 0.6)'},
    other:         {border: '#9ca3af', bg: 'rgba(156, 163, 175, 0.6)'},
};

var BREAKDOWN_LABELS = {
    equity: 'Equity (SOEs)',
    cash_deposits: 'Cash & Deposits',
    securities: 'Securities',
    loans: 'Loans',
    bonds: 'Bonds',
    other: 'Other',
};

if (DATA.balance.labels.length > 0) {
    var BAL = DATA.balance;
    let currentCurrency = 'USD';
    let dateFrom = '';
    let dateTo = '';

    var inputFrom = document.getElementById('dateFrom');
    var inputTo = document.getElementById('dateTo');

    inputFrom.min = BAL.labels[0];
    inputFrom.max = BAL.labels[BAL.labels.length - 1];
    inputTo.min = BAL.labels[0];
    inputTo.max = BAL.labels[BAL.labels.length - 1];

    function formatLabel(currency) {
        if (currency === 'USD') return 'USD millions';
        return 'CLP millions';
    }

    function getFilteredIndices(labels) {
        var start = 0;
        var end = labels.length;
        if (dateFrom) {
            start = labels.findIndex(function(l) { return l >= dateFrom; });
            if (start === -1) start = labels.length;
        }
        if (dateTo) {
            for (var i = labels.length - 1; i >= 0; i--) {
                if (labels[i] <= dateTo) { end = i + 1; break; }
            }
        }
        return [start, end];
    }

    function getBalanceData(currency) {
        var range = getFilteredIndices(BAL.labels);
        var s = range[0], e = range[1];
        return {
            labels: BAL.labels.slice(s, e),
            datasets: [
                {
                    label: 'Assets (' + formatLabel(currency) + ')',
                    data: BAL[currency].assets.slice(s, e),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    fill: true, tension: 0.3,
                },
                {
                    label: 'Liabilities (' + formatLabel(currency) + ')',
                    data: BAL[currency].liabilities.slice(s, e),
                    borderColor: '#dc2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.1)',
                    fill: true, tension: 0.3,
                },
                {
                    label: 'Net position (' + formatLabel(currency) + ')',
                    data: BAL[currency].net.slice(s, e),
                    borderColor: '#16a34a',
                    backgroundColor: 'rgba(22, 163, 74, 0.05)',
                    fill: true, tension: 0.3, borderDash: [6, 3],
                },
            ],
        };
    }

    function snapToLabel(dateStr, labels) {
        var best = 0;
        for (var i = 0; i < labels.length; i++) {
            if (labels[i] <= dateStr) best = i;
            else break;
        }
        return best;
    }

    function buildAnnotations(labels) {
        var annotations = {};
        if (!labels || labels.length === 0) return annotations;
        var firstLabel = labels[0];
        var lastLabel = labels[labels.length - 1];

        PRESIDENTS.forEach(function(p, i) {
            if (p.end < firstLabel || p.start > lastLabel) return;
            var xMin = snapToLabel(p.start, labels);
            var xMax = snapToLabel(p.end, labels);
            if (xMax === xMin) xMax = Math.min(xMin + 1, labels.length - 1);

            annotations['band' + i] = {
                type: 'box', xMin: xMin, xMax: xMax,
                backgroundColor: p.color, borderWidth: 0,
                label: {
                    display: true, content: p.name,
                    position: {x: 'center', y: 'start'},
                    color: '#9ca3af', font: {size: 11, weight: 'normal'}, padding: 4,
                },
            };
            annotations['line' + i] = {
                type: 'line', xMin: xMin, xMax: xMin,
                borderColor: 'rgba(156, 163, 175, 0.3)', borderWidth: 1, borderDash: [4, 4],
            };
        });
        return annotations;
    }

    var numFmt = {maximumFractionDigits: 0};
    var tooltipCb = {
        label: function(ctx) {
            return ctx.dataset.label + ': ' + ctx.parsed.y.toLocaleString('en-US', numFmt);
        }
    };
    var tickCb = function(val) { return val.toLocaleString('en-US', numFmt); };

    function sliceObj(obj, s, e) {
        var result = {};
        Object.keys(obj).forEach(function(k) { result[k] = obj[k].slice(s, e); });
        return result;
    }

    function makeStackedDatasets(items) {
        var datasets = [];
        Object.keys(items).forEach(function(key) {
            var c = BREAKDOWN_COLORS[key] || {border: '#6b7280', bg: 'rgba(107, 114, 128, 0.6)'};
            datasets.push({
                label: BREAKDOWN_LABELS[key] || key,
                data: items[key],
                backgroundColor: c.bg,
                borderColor: c.border,
                borderWidth: 1,
                fill: true,
            });
        });
        return datasets;
    }

    // ── Main balance chart ─────────────────────────────────────────
    var initialData = getBalanceData(currentCurrency);
    var balanceChart = new Chart(document.getElementById('balanceChart'), {
        type: 'line',
        data: initialData,
        options: {
            responsive: true,
            plugins: {
                title: {display: true, text: 'Public Sector Balance Sheet'},
                legend: {position: 'top'},
                tooltip: {callbacks: tooltipCb},
                annotation: {annotations: buildAnnotations(initialData.labels)},
            },
            scales: {
                x: {type: 'category', title: {display: true, text: 'Date'}},
                y: {title: {display: true, text: formatLabel(currentCurrency)}, ticks: {callback: tickCb}},
            },
        },
    });

    // ── Breakdown charts ───────────────────────────────────────────
    var BD = DATA.breakdown;
    var assetBDChart = null;
    var liabilityBDChart = null;

    if (BD.labels.length > 0) {
        var stackPlugins = function(title, labels) {
            return {legend: {position: 'top'}, tooltip: {mode: 'index', callbacks: tooltipCb}, title: {display: true, text: title}, annotation: {annotations: buildAnnotations(labels)}};
        };

        assetBDChart = new Chart(document.getElementById('assetBreakdownChart'), {
            type: 'bar',
            data: {labels: BD.labels, datasets: makeStackedDatasets(BD[currentCurrency].assets)},
            options: {
                responsive: true,
                plugins: stackPlugins('Government Assets', BD.labels),
                scales: {x: {stacked: true, title: {display: true, text: 'Date'}}, y: {stacked: true, title: {display: true, text: formatLabel(currentCurrency)}, ticks: {callback: tickCb}}},
            },
        });

        liabilityBDChart = new Chart(document.getElementById('liabilityBreakdownChart'), {
            type: 'bar',
            data: {labels: BD.labels, datasets: makeStackedDatasets(BD[currentCurrency].liabilities)},
            options: {
                responsive: true,
                plugins: stackPlugins('Government Liabilities', BD.labels),
                scales: {x: {stacked: true, title: {display: true, text: 'Date'}}, y: {stacked: true, title: {display: true, text: formatLabel(currentCurrency)}, ticks: {callback: tickCb}}},
            },
        });
    }

    // ── Ratio chart (% of GDP) ─────────────────────────────────────
    var RT = DATA.ratios;
    var ratioChart = null;

    if (RT.labels && RT.labels.length > 0) {
        var ratioSeries = [
            {key: 'net_financial_assets_pct_gdp', label: 'Net Financial Assets (% GDP)', color: '#16a34a', bg: 'rgba(22, 163, 74, 0.1)'},
            {key: 'fiscal_balance_pct_gdp', label: 'Fiscal Balance (% GDP)', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)'},
        ];

        var rtAnn = buildAnnotations(RT.labels);
        rtAnn.zeroLine = {type: 'line', yMin: 0, yMax: 0, borderColor: 'rgba(0,0,0,0.2)', borderWidth: 1, borderDash: [4, 4]};

        ratioChart = new Chart(document.getElementById('ratioChart'), {
            type: 'line',
            data: {
                labels: RT.labels,
                datasets: ratioSeries.filter(function(rs) { return RT[rs.key]; }).map(function(rs) {
                    return {label: rs.label, data: RT[rs.key], borderColor: rs.color, backgroundColor: rs.bg, fill: true, tension: 0.3};
                }),
            },
            options: {
                responsive: true,
                plugins: {title: {display: true, text: 'Fiscal Indicators (% of GDP)'}, legend: {position: 'top'}, annotation: {annotations: rtAnn}},
                scales: {x: {title: {display: true, text: 'Date'}}, y: {title: {display: true, text: '% of GDP'}}},
            },
        });
    }

    // ── Global update ──────────────────────────────────────────────
    function updateAllCharts() {
        // Balance chart
        var newBal = getBalanceData(currentCurrency);
        balanceChart.data = newBal;
        balanceChart.options.scales.y.title.text = formatLabel(currentCurrency);
        balanceChart.options.plugins.annotation.annotations = buildAnnotations(newBal.labels);
        balanceChart.update();

        // Breakdown charts
        if (assetBDChart && BD.labels.length > 0) {
            var r = getFilteredIndices(BD.labels);
            var sl = BD.labels.slice(r[0], r[1]);
            var ann = buildAnnotations(sl);
            var bdc = BD[currentCurrency];

            assetBDChart.data = {labels: sl, datasets: makeStackedDatasets(sliceObj(bdc.assets, r[0], r[1]))};
            assetBDChart.options.plugins.annotation.annotations = ann;
            assetBDChart.options.scales.y.title.text = formatLabel(currentCurrency);
            assetBDChart.update();

            liabilityBDChart.data = {labels: sl, datasets: makeStackedDatasets(sliceObj(bdc.liabilities, r[0], r[1]))};
            liabilityBDChart.options.plugins.annotation.annotations = ann;
            liabilityBDChart.options.scales.y.title.text = formatLabel(currentCurrency);
            liabilityBDChart.update();
        }

        // Ratio chart
        if (ratioChart && RT.labels.length > 0) {
            var rr = getFilteredIndices(RT.labels);
            var rl = RT.labels.slice(rr[0], rr[1]);
            var rAnn = buildAnnotations(rl);
            rAnn.zeroLine = {type: 'line', yMin: 0, yMax: 0, borderColor: 'rgba(0,0,0,0.2)', borderWidth: 1, borderDash: [4, 4]};

            ratioChart.data = {
                labels: rl,
                datasets: ratioSeries.filter(function(rs) { return RT[rs.key]; }).map(function(rs) {
                    return {label: rs.label, data: RT[rs.key].slice(rr[0], rr[1]), borderColor: rs.color, backgroundColor: rs.bg, fill: true, tension: 0.3};
                }),
            };
            ratioChart.options.plugins.annotation.annotations = rAnn;
            ratioChart.update();
        }
    }

    document.querySelectorAll('.currency-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            currentCurrency = this.dataset.currency;
            document.querySelectorAll('.currency-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            updateAllCharts();
        });
    });

    inputFrom.addEventListener('change', function() {
        dateFrom = this.value;
        document.querySelectorAll('.preset-btn').forEach(function(b) { b.classList.remove('active'); });
        updateChart();
    });

    inputTo.addEventListener('change', function() {
        dateTo = this.value;
        document.querySelectorAll('.preset-btn').forEach(function(b) { b.classList.remove('active'); });
        updateChart();
    });

    document.querySelectorAll('.preset-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var years = parseInt(this.dataset.years);
            var lastDate = BAL.labels[BAL.labels.length - 1];
            document.querySelectorAll('.preset-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');

            if (years === 0) {
                dateFrom = ''; dateTo = '';
                inputFrom.value = ''; inputTo.value = '';
            } else {
                var d = new Date(lastDate);
                d.setFullYear(d.getFullYear() - years);
                dateFrom = d.toISOString().slice(0, 10);
                dateTo = lastDate;
                inputFrom.value = dateFrom;
                inputTo.value = dateTo;
            }
            updateAllCharts();
        });
    });

    var sticky = document.getElementById('stickyControls');
    window.addEventListener('scroll', function() {
        sticky.classList.toggle('scrolled', window.scrollY > 60);
    });
}
"""

CANVAS_HTML = """\
<div class="sticky-controls" id="stickyControls">
    <div class="controls">
        <button class="currency-btn active" data-currency="USD">USD</button>
        <button class="currency-btn" data-currency="CLP">CLP</button>
    </div>
    <div class="date-controls">
        <input type="date" id="dateFrom" aria-label="From date">
        <span class="separator">to</span>
        <input type="date" id="dateTo" aria-label="To date">
        <div class="presets">
            <button class="preset-btn" data-years="1">1Y</button>
            <button class="preset-btn" data-years="5">5Y</button>
            <button class="preset-btn" data-years="10">10Y</button>
            <button class="preset-btn" data-years="20">20Y</button>
            <button class="preset-btn active" data-years="0">All</button>
        </div>
    </div>
</div>
<div class="chart-container">
    <canvas id="balanceChart"></canvas>
</div>
<div class="chart-stack">
    <div class="chart-container">
        <canvas id="assetBreakdownChart"></canvas>
    </div>
    <div class="chart-container">
        <canvas id="liabilityBreakdownChart"></canvas>
    </div>
</div>
<div class="chart-container">
    <canvas id="ratioChart"></canvas>
</div>"""

EMPTY_HTML = '<div class="chart-container"><p class="empty-state">No data yet. Run collectors first.</p></div>'


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
        if entry.category.startswith("breakdown.") or entry.category.startswith("ratio."):
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


def build_site(data_path: Path, rates_path: Path, output_path: Path) -> None:
    entries = read_entries(data_path)
    rates = read_rates(rates_path)
    chart_data = prepare_chart_data(entries, rates)
    breakdown_data = prepare_breakdown_data(entries, rates)
    ratio_data = prepare_ratio_data(entries)

    has_data = len(chart_data["labels"]) > 0

    all_data = json.dumps({
        "balance": chart_data,
        "breakdown": breakdown_data,
        "ratios": ratio_data,
    })

    html = HTML_TEMPLATE.replace("CHART_DATA", all_data)
    html = html.replace("CHART_CONTENT", CANVAS_HTML if has_data else EMPTY_HTML)
    html = html.replace("CHART_SCRIPT", CHART_SCRIPT if has_data else "")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
