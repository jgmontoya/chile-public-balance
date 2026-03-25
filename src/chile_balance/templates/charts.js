var I18N = {
    en: {
        pageTitle: 'Chile Public Balance Sheet',
        pageSubtitle: 'Assets and liabilities of the Chilean state over time',
        balanceTitle: 'Public Sector Balance Sheet',
        govtAssets: 'Government Assets',
        govtLiabilities: 'Government Liabilities',
        ratioTitle: 'Fiscal Indicators (% of GDP)',
        assets: 'Assets',
        liabilities: 'Liabilities',
        netPosition: 'Net position',
        netFinancialAssets: 'Net Financial Assets (% GDP)',
        fiscalBalance: 'Fiscal Balance (% GDP)',
        date: 'Date',
        usdMillions: 'USD millions',
        clpMillions: 'CLP millions',
        pctGdp: '% of GDP',
        noData: 'No data yet. Run collectors first.',
        equity: 'Equity (SOEs)',
        cash_deposits: 'Cash & Deposits',
        securities: 'Securities',
        loans: 'Loans',
        bonds_short: 'Bonds (short-term)',
        bonds_long: 'Bonds (long-term)',
        other: 'Other',
        govtDebt: 'Government Debt (% GDP)',
        contingentLiabilities: 'Contingent Liabilities (% GDP)',
        copperTitle: 'Copper Price',
        copperPrice: 'Copper',
        usdPerLb: 'USD/lb',
        clpPerLb: 'CLP/lb',
        evtCopper: 'Copper nationalized',
        evtCoup: 'Coup',
        evtBanking: 'Banking crisis',
        evtDemocracy: 'Democracy',
        evtSupercycle: 'Supercycle',
        evtFunds: 'FEES/FRP',
        evtGFC: 'GFC 2008',
        evtEarthquake: 'Earthquake 8.8',
        evtEstallido: 'Estallido',
        evtCovid: 'COVID-19',
        evtReferendum: 'Plebiscito',
        infoBalance: 'Total financial assets and liabilities of the General Government and Central Bank. Quarterly, from national accounts by institutional sector (F038). Source: Banco Central de Chile.',
        infoAssets: 'Government general financial assets by instrument type: equity in state-owned enterprises, cash and deposits, securities, loans, and other accounts. Source: Banco Central de Chile (F038).',
        infoLiabilities: 'Government general liabilities by maturity and type: long-term bonds, short-term bonds, loans, and other. Source: Banco Central de Chile (F038).',
        infoRatios: 'Net financial assets, fiscal balance, government debt, and contingent liabilities as percentage of GDP. Quarterly ratios from Banco Central (F038). Contingent liabilities from annual DIPRES reports (2007-2025).',
        infoCopper: 'Monthly copper price (BML London). Chile is the world\'s largest copper producer and fiscal revenues are highly correlated with the copper price. Source: Banco Central de Chile.',
        sovereignFundsTitle: 'Sovereign Funds',
        fees: 'FEES',
        frp: 'FRP',
        infoSovereignFunds: 'FEES (Economic and Social Stabilization Fund) and FRP (Pension Reserve Fund), created in 2006 under the Fiscal Responsibility Law. These funds are included in government general assets. Source: Banco Central de Chile (F051).',
    },
    es: {
        pageTitle: 'Balance Público de Chile',
        pageSubtitle: 'Activos y pasivos del Estado chileno a lo largo del tiempo',
        balanceTitle: 'Balance del Sector Público',
        govtAssets: 'Activos del Gobierno',
        govtLiabilities: 'Pasivos del Gobierno',
        ratioTitle: 'Indicadores Fiscales (% del PIB)',
        assets: 'Activos',
        liabilities: 'Pasivos',
        netPosition: 'Posición neta',
        netFinancialAssets: 'Activos Financieros Netos (% PIB)',
        fiscalBalance: 'Balance Fiscal (% PIB)',
        date: 'Fecha',
        usdMillions: 'Millones USD',
        clpMillions: 'Millones CLP',
        pctGdp: '% del PIB',
        noData: 'Sin datos. Ejecute los recolectores primero.',
        equity: 'Participaciones (empresas públicas)',
        cash_deposits: 'Efectivo y depósitos',
        securities: 'Títulos de deuda',
        loans: 'Préstamos',
        bonds_short: 'Bonos (corto plazo)',
        bonds_long: 'Bonos (largo plazo)',
        other: 'Otros',
        govtDebt: 'Deuda del Gobierno (% PIB)',
        contingentLiabilities: 'Pasivos Contingentes (% PIB)',
        copperTitle: 'Precio del Cobre',
        copperPrice: 'Cobre',
        usdPerLb: 'USD/lb',
        clpPerLb: 'CLP/lb',
        evtCopper: 'Nacionalizacion',
        evtCoup: 'Golpe',
        evtBanking: 'Crisis bancaria',
        evtDemocracy: 'Democracia',
        evtSupercycle: 'Superciclo',
        evtFunds: 'FEES/FRP',
        evtGFC: 'Crisis 2008',
        evtEarthquake: 'Terremoto 8.8',
        evtEstallido: 'Estallido',
        evtCovid: 'COVID-19',
        evtReferendum: 'Plebiscito',
        infoBalance: 'Activos y pasivos financieros totales del Gobierno General y Banco Central. Trimestral, de cuentas nacionales por sector institucional (F038). Fuente: Banco Central de Chile.',
        infoAssets: 'Activos financieros del gobierno general por tipo de instrumento: participaciones en empresas estatales, efectivo y depositos, titulos, prestamos y otras cuentas. Fuente: Banco Central de Chile (F038).',
        infoLiabilities: 'Pasivos del gobierno general por plazo y tipo: bonos de largo plazo, bonos de corto plazo, prestamos y otros. Fuente: Banco Central de Chile (F038).',
        infoRatios: 'Activos financieros netos, balance fiscal, deuda del gobierno y pasivos contingentes como porcentaje del PIB. Ratios trimestrales del Banco Central (F038). Pasivos contingentes de informes anuales de DIPRES (2007-2025).',
        infoCopper: 'Precio mensual del cobre (BML Londres). Chile es el mayor productor de cobre del mundo y los ingresos fiscales estan altamente correlacionados con el precio del cobre. Fuente: Banco Central de Chile.',
        sovereignFundsTitle: 'Fondos Soberanos',
        fees: 'FEES',
        frp: 'FRP',
        infoSovereignFunds: 'FEES (Fondo de Estabilizacion Economica y Social) y FRP (Fondo de Reserva de Pensiones), creados en 2006 bajo la Ley de Responsabilidad Fiscal. Estos fondos estan incluidos en los activos del gobierno general. Fuente: Banco Central de Chile (F051).',
    },
};

var currentLang = (window.location.hash === '#es') ? 'es' : 'en';
function t(key) { return I18N[currentLang][key] || key; }
function numLocale() { return currentLang === 'es' ? 'es-CL' : 'en-US'; }

var EVENTS = [
    {date: '1971-07-11', i18n: 'evtCopper'},
    {date: '1973-09-11', i18n: 'evtCoup'},
    {date: '1982-06-01', i18n: 'evtBanking'},
    {date: '1990-03-11', i18n: 'evtDemocracy'},
    {date: '2003-01-01', i18n: 'evtSupercycle'},
    {date: '2006-03-01', i18n: 'evtFunds'},
    {date: '2008-09-15', i18n: 'evtGFC'},
    {date: '2010-02-27', i18n: 'evtEarthquake'},
    {date: '2019-10-18', i18n: 'evtEstallido'},
    {date: '2020-03-15', i18n: 'evtCovid'},
    {date: '2022-09-04', i18n: 'evtReferendum'},
];

var PRESIDENTS = [
    {name: 'Alessandri',      start: '1958-11-03', end: '1964-11-03', color: 'rgba(59, 130, 246, 0.07)'},
    {name: 'Frei Montalva',   start: '1964-11-03', end: '1970-11-03', color: 'rgba(234, 179, 8, 0.07)'},
    {name: 'Allende',         start: '1970-11-03', end: '1973-09-11', color: 'rgba(239, 68, 68, 0.07)'},
    {name: 'Pinochet',        start: '1973-09-11', end: '1990-03-11', color: 'rgba(107, 114, 128, 0.07)'},
    {name: 'Aylwin',          start: '1990-03-11', end: '1994-03-11', color: 'rgba(234, 179, 8, 0.07)'},
    {name: 'Frei Ruiz-Tagle', start: '1994-03-11', end: '2000-03-11', color: 'rgba(234, 179, 8, 0.07)'},
    {name: 'Lagos',           start: '2000-03-11', end: '2006-03-11', color: 'rgba(239, 68, 68, 0.07)'},
    {name: 'Bachelet I',      start: '2006-03-11', end: '2010-03-11', color: 'rgba(234, 179, 8, 0.07)'},
    {name: 'Piñera I',        start: '2010-03-11', end: '2014-03-11', color: 'rgba(59, 130, 246, 0.07)'},
    {name: 'Bachelet II',     start: '2014-03-11', end: '2018-03-11', color: 'rgba(234, 179, 8, 0.07)'},
    {name: 'Piñera II',       start: '2018-03-11', end: '2022-03-11', color: 'rgba(59, 130, 246, 0.07)'},
    {name: 'Boric',           start: '2022-03-11', end: '2026-03-11', color: 'rgba(239, 68, 68, 0.07)'},
    {name: 'Kast',            start: '2026-03-11', end: '2030-03-11', color: 'rgba(59, 130, 246, 0.07)'},
];

var BREAKDOWN_COLORS = {
    equity:        {border: '#7c3aed', bg: 'rgba(124, 58, 237, 0.6)'},
    cash_deposits: {border: '#0891b2', bg: 'rgba(8, 145, 178, 0.6)'},
    securities:    {border: '#2563eb', bg: 'rgba(37, 99, 235, 0.6)'},
    loans:         {border: '#059669', bg: 'rgba(5, 150, 105, 0.6)'},
    bonds_short:   {border: '#f59e0b', bg: 'rgba(245, 158, 11, 0.6)'},
    bonds_long:    {border: '#dc2626', bg: 'rgba(220, 38, 38, 0.6)'},
    other:         {border: '#9ca3af', bg: 'rgba(156, 163, 175, 0.6)'},
};

function breakdownLabel(key) { return t(key) || key; }

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
        if (currency === 'USD') return t('usdMillions');
        return t('clpMillions');
    }

    function copperUnit(currency) {
        return currency === 'USD' ? t('usdPerLb') : t('clpPerLb');
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
        var unit = formatLabel(currency);
        return {
            labels: BAL.labels.slice(s, e),
            datasets: [
                {
                    label: t('assets') + ' (' + unit + ')',
                    data: BAL[currency].assets.slice(s, e),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    fill: true, tension: 0.3,
                },
                {
                    label: t('liabilities') + ' (' + unit + ')',
                    data: BAL[currency].liabilities.slice(s, e),
                    borderColor: '#dc2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.1)',
                    fill: true, tension: 0.3,
                },
                {
                    label: t('netPosition') + ' (' + unit + ')',
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

        EVENTS.forEach(function(ev, i) {
            if (ev.date < firstLabel || ev.date > lastLabel) return;
            var x = snapToLabel(ev.date, labels);
            annotations['event' + i] = {
                type: 'line', xMin: x, xMax: x,
                drawTime: 'beforeDatasetsDraw',
                borderColor: 'rgba(220, 38, 38, 0.25)', borderWidth: 1, borderDash: [2, 3],
                label: {
                    display: true, content: t(ev.i18n),
                    drawTime: 'beforeDatasetsDraw',
                    position: 'start', backgroundColor: 'rgba(220, 38, 38, 0.04)',
                    color: 'rgba(220, 38, 38, 0.5)', font: {size: 8}, padding: {x: 3, y: 2},
                    rotation: -45, yAdjust: -15,
                },
            };
        });

        return annotations;
    }

    function fmtShort(val) {
        var abs = Math.abs(val);
        var sign = val < 0 ? '-' : '';
        if (abs >= 1e9) return sign + (abs / 1e9).toFixed(1) + 'T';
        if (abs >= 1e6) return sign + (abs / 1e6).toFixed(1) + 'B';
        if (abs >= 1e3) return sign + (abs / 1e3).toFixed(1) + 'K';
        return sign + abs.toFixed(0);
    }

    function fmtFull(val) {
        return val.toLocaleString(numLocale(), {maximumFractionDigits: 0});
    }

    var tooltipCb = {
        label: function(ctx) {
            return ctx.dataset.label + ': ' + fmtFull(ctx.parsed.y);
        }
    };
    var tickCb = function(val) { return fmtShort(val); };

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
                label: breakdownLabel(key),
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
                title: {display: true, text: t('balanceTitle')},
                legend: {position: 'top'},
                tooltip: {callbacks: tooltipCb},
                annotation: {annotations: buildAnnotations(initialData.labels)},
            },
            scales: {
                x: {type: 'category', title: {display: true, text: t('date')}},
                y: {title: {display: true, text: formatLabel(currentCurrency)}, ticks: {callback: tickCb}},
            },
        },
    });

    // ── Breakdown charts ───────────────────────────────────────────
    var BD = DATA.breakdown;
    var assetBDChart = null;
    var liabilityBDChart = null;

    if (BD.labels.length > 0) {
        var stackPlugins = function(titleKey, labels) {
            return {legend: {position: 'top'}, tooltip: {mode: 'index', callbacks: tooltipCb}, title: {display: true, text: t(titleKey)}, annotation: {annotations: buildAnnotations(labels)}};
        };

        assetBDChart = new Chart(document.getElementById('assetBreakdownChart'), {
            type: 'bar',
            data: {labels: BD.labels, datasets: makeStackedDatasets(BD[currentCurrency].assets)},
            options: {
                responsive: true,
                plugins: stackPlugins('govtAssets', BD.labels),
                scales: {x: {stacked: true, title: {display: true, text: t('date')}}, y: {stacked: true, title: {display: true, text: formatLabel(currentCurrency)}, ticks: {callback: tickCb}}},
            },
        });

        liabilityBDChart = new Chart(document.getElementById('liabilityBreakdownChart'), {
            type: 'bar',
            data: {labels: BD.labels, datasets: makeStackedDatasets(BD[currentCurrency].liabilities)},
            options: {
                responsive: true,
                plugins: stackPlugins('govtLiabilities', BD.labels),
                scales: {x: {stacked: true, title: {display: true, text: t('date')}}, y: {stacked: true, title: {display: true, text: formatLabel(currentCurrency)}, ticks: {callback: tickCb}}},
            },
        });
    }

    // ── Ratio chart (% of GDP) ─────────────────────────────────────
    var RT = DATA.ratios;
    var ratioChart = null;

    if (RT.labels && RT.labels.length > 0) {
        var ratioSeries = [
            {key: 'net_financial_assets_pct_gdp', i18nKey: 'netFinancialAssets', color: '#16a34a', bg: 'rgba(22, 163, 74, 0.1)'},
            {key: 'fiscal_balance_pct_gdp', i18nKey: 'fiscalBalance', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.1)'},
            {key: 'govt_debt_pct_gdp', i18nKey: 'govtDebt', color: '#dc2626', bg: 'rgba(220, 38, 38, 0.1)'},
            {key: 'contingent_liabilities_pct_gdp', i18nKey: 'contingentLiabilities', color: '#7c3aed', bg: 'rgba(124, 58, 237, 0.1)'},
        ];

        var rtAnn = buildAnnotations(RT.labels);
        rtAnn.zeroLine = {type: 'line', yMin: 0, yMax: 0, borderColor: 'rgba(0,0,0,0.2)', borderWidth: 1, borderDash: [4, 4]};

        ratioChart = new Chart(document.getElementById('ratioChart'), {
            type: 'line',
            data: {
                labels: RT.labels,
                datasets: ratioSeries.filter(function(rs) { return RT[rs.key]; }).map(function(rs) {
                    return {label: t(rs.i18nKey), data: RT[rs.key], borderColor: rs.color, backgroundColor: rs.bg, fill: true, tension: 0.3};
                }),
            },
            options: {
                responsive: true,
                plugins: {title: {display: true, text: t('ratioTitle')}, legend: {position: 'top'}, annotation: {annotations: rtAnn}},
                scales: {x: {title: {display: true, text: t('date')}}, y: {title: {display: true, text: t('pctGdp')}}},
            },
        });
    }

    // ── Copper price chart ─────────────────────────────────────────
    var CX = DATA.context;
    var copperChart = null;

    if (CX.labels && CX.labels.length > 0 && CX.USD && CX.USD.copper_price_usd_lb) {
        copperChart = new Chart(document.getElementById('copperChart'), {
            type: 'line',
            data: {
                labels: CX.labels,
                datasets: [{
                    label: t('copperPrice'),
                    data: CX[currentCurrency].copper_price_usd_lb,
                    borderColor: '#b45309',
                    backgroundColor: 'rgba(180, 83, 9, 0.1)',
                    fill: true, tension: 0.3, pointRadius: 0,
                }],
            },
            options: {
                responsive: true,
                plugins: {
                    title: {display: true, text: t('copperTitle') + ' (' + copperUnit(currentCurrency) + ')'},
                    legend: {display: false},
                    annotation: {annotations: buildAnnotations(CX.labels)},
                },
                scales: {
                    x: {title: {display: true, text: t('date')}},
                    y: {title: {display: true, text: copperUnit(currentCurrency)}, ticks: {callback: tickCb}},
                },
            },
        });
    } else {
        var cc = document.getElementById('copperChartContainer');
        if (cc) cc.style.display = 'none';
    }

    // ── Sovereign fund chart ────────────────────────────────────────
    var sovereignFundChart = null;

    if (CX.labels && CX.labels.length > 0 && CX.USD && CX.USD.fees_usd) {
        var sfDatasets = [
            {key: 'fees_usd', i18nKey: 'fees', color: '#2563eb', bg: 'rgba(37, 99, 235, 0.1)'},
            {key: 'frp_usd', i18nKey: 'frp', color: '#16a34a', bg: 'rgba(22, 163, 74, 0.1)'},
        ];

        sovereignFundChart = new Chart(document.getElementById('sovereignFundChart'), {
            type: 'line',
            data: {
                labels: CX.labels,
                datasets: sfDatasets.filter(function(sf) { return CX[currentCurrency][sf.key]; }).map(function(sf) {
                    return {
                        label: t(sf.i18nKey),
                        data: CX[currentCurrency][sf.key],
                        borderColor: sf.color,
                        backgroundColor: sf.bg,
                        fill: true, tension: 0.3, pointRadius: 0,
                    };
                }),
            },
            options: {
                responsive: true,
                plugins: {
                    title: {display: true, text: t('sovereignFundsTitle') + ' (' + formatLabel(currentCurrency) + ')'},
                    legend: {position: 'top'},
                    tooltip: {callbacks: tooltipCb},
                    annotation: {annotations: buildAnnotations(CX.labels)},
                },
                scales: {
                    x: {title: {display: true, text: t('date')}},
                    y: {title: {display: true, text: formatLabel(currentCurrency)}, ticks: {callback: tickCb}},
                },
            },
        });
    } else {
        var sfc = document.getElementById('sovereignFundChartContainer');
        if (sfc) sfc.style.display = 'none';
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
                    return {label: t(rs.i18nKey), data: RT[rs.key].slice(rr[0], rr[1]), borderColor: rs.color, backgroundColor: rs.bg, fill: true, tension: 0.3};
                }),
            };
            ratioChart.options.plugins.annotation.annotations = rAnn;
            ratioChart.update();
        }

        // Copper chart
        if (copperChart && CX.labels.length > 0) {
            var cr = getFilteredIndices(CX.labels);
            var cl = CX.labels.slice(cr[0], cr[1]);
            copperChart.data = {
                labels: cl,
                datasets: [{
                    label: t('copperPrice'), data: CX[currentCurrency].copper_price_usd_lb.slice(cr[0], cr[1]),
                    borderColor: '#b45309', backgroundColor: 'rgba(180, 83, 9, 0.1)',
                    fill: true, tension: 0.3, pointRadius: 0,
                }],
            };
            copperChart.options.plugins.title.text = t('copperTitle') + ' (' + copperUnit(currentCurrency) + ')';
            copperChart.options.scales.y.title.text = copperUnit(currentCurrency);
            copperChart.options.plugins.annotation.annotations = buildAnnotations(cl);
            copperChart.update();
        }

        // Sovereign fund chart
        if (sovereignFundChart && CX.labels.length > 0) {
            var sr = getFilteredIndices(CX.labels);
            var sl2 = CX.labels.slice(sr[0], sr[1]);
            sovereignFundChart.data = {
                labels: sl2,
                datasets: sfDatasets.filter(function(sf) { return CX[currentCurrency][sf.key]; }).map(function(sf) {
                    return {
                        label: t(sf.i18nKey), data: CX[currentCurrency][sf.key].slice(sr[0], sr[1]),
                        borderColor: sf.color, backgroundColor: sf.bg,
                        fill: true, tension: 0.3, pointRadius: 0,
                    };
                }),
            };
            sovereignFundChart.options.plugins.title.text = t('sovereignFundsTitle') + ' (' + formatLabel(currentCurrency) + ')';
            sovereignFundChart.options.scales.y.title.text = formatLabel(currentCurrency);
            sovereignFundChart.options.plugins.annotation.annotations = buildAnnotations(sl2);
            sovereignFundChart.update();
        }

        renderDataTable();
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
        updateAllCharts();
    });

    inputTo.addEventListener('change', function() {
        dateTo = this.value;
        document.querySelectorAll('.preset-btn').forEach(function(b) { b.classList.remove('active'); });
        updateAllCharts();
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

    // Language toggle — update HTML text and rebuild all charts
    function applyLanguage() {
        document.getElementById('htmlRoot').lang = currentLang === 'es' ? 'es' : 'en';
        document.querySelectorAll('[data-i18n]').forEach(function(el) {
            var key = el.getAttribute('data-i18n');
            if (I18N[currentLang][key]) el.textContent = I18N[currentLang][key];
        });
        document.querySelectorAll('.lang-btn').forEach(function(b) {
            b.classList.toggle('active', b.dataset.lang === currentLang);
        });
    }
    applyLanguage();

    document.querySelectorAll('.lang-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            currentLang = this.dataset.lang;
            window.location.hash = currentLang === 'es' ? '#es' : '#en';
            applyLanguage();

            // Rebuild balance chart titles and labels
            var newBal = getBalanceData(currentCurrency);
            balanceChart.data = newBal;
            balanceChart.options.plugins.title.text = t('balanceTitle');
            balanceChart.options.scales.x.title.text = t('date');
            balanceChart.options.scales.y.title.text = formatLabel(currentCurrency);
            balanceChart.options.plugins.annotation.annotations = buildAnnotations(newBal.labels);
            balanceChart.update();

            // Rebuild breakdown charts
            if (assetBDChart && BD.labels.length > 0) {
                var r = getFilteredIndices(BD.labels);
                var sl = BD.labels.slice(r[0], r[1]);
                var bdc = BD[currentCurrency];

                assetBDChart.data = {labels: sl, datasets: makeStackedDatasets(sliceObj(bdc.assets, r[0], r[1]))};
                assetBDChart.options.plugins.title.text = t('govtAssets');
                assetBDChart.options.scales.x.title.text = t('date');
                assetBDChart.options.scales.y.title.text = formatLabel(currentCurrency);
                assetBDChart.options.plugins.annotation.annotations = buildAnnotations(sl);
                assetBDChart.update();

                liabilityBDChart.data = {labels: sl, datasets: makeStackedDatasets(sliceObj(bdc.liabilities, r[0], r[1]))};
                liabilityBDChart.options.plugins.title.text = t('govtLiabilities');
                liabilityBDChart.options.scales.x.title.text = t('date');
                liabilityBDChart.options.scales.y.title.text = formatLabel(currentCurrency);
                liabilityBDChart.options.plugins.annotation.annotations = buildAnnotations(sl);
                liabilityBDChart.update();
            }

            // Rebuild ratio chart
            if (ratioChart && RT.labels.length > 0) {
                var rr = getFilteredIndices(RT.labels);
                var rl = RT.labels.slice(rr[0], rr[1]);
                var rAnn = buildAnnotations(rl);
                rAnn.zeroLine = {type: 'line', yMin: 0, yMax: 0, borderColor: 'rgba(0,0,0,0.2)', borderWidth: 1, borderDash: [4, 4]};

                ratioChart.data = {
                    labels: rl,
                    datasets: ratioSeries.filter(function(rs) { return RT[rs.key]; }).map(function(rs) {
                        return {label: t(rs.i18nKey), data: RT[rs.key].slice(rr[0], rr[1]), borderColor: rs.color, backgroundColor: rs.bg, fill: true, tension: 0.3};
                    }),
                };
                ratioChart.options.plugins.title.text = t('ratioTitle');
                ratioChart.options.scales.x.title.text = t('date');
                ratioChart.options.scales.y.title.text = t('pctGdp');
                ratioChart.options.plugins.annotation.annotations = rAnn;
                ratioChart.update();
            }

            if (copperChart) {
                copperChart.options.plugins.title.text = t('copperTitle') + ' (' + copperUnit(currentCurrency) + ')';
                copperChart.options.scales.x.title.text = t('date');
                copperChart.options.scales.y.title.text = copperUnit(currentCurrency);
                copperChart.data.datasets[0].label = t('copperPrice');
                copperChart.update();
            }

            if (sovereignFundChart) {
                sovereignFundChart.options.plugins.title.text = t('sovereignFundsTitle') + ' (' + formatLabel(currentCurrency) + ')';
                sovereignFundChart.options.scales.x.title.text = t('date');
                sovereignFundChart.options.scales.y.title.text = formatLabel(currentCurrency);
                sovereignFundChart.data.datasets.forEach(function(ds, i) {
                    ds.label = t(sfDatasets[i].i18nKey);
                });
                sovereignFundChart.update();
            }

            renderDataTable();
        });
    });

    // ── Dark mode ───────────────────────────────────────────────────
    function getChartColors() {
        var style = getComputedStyle(document.documentElement);
        return {
            grid: style.getPropertyValue('--chart-grid').trim(),
            text: style.getPropertyValue('--chart-text').trim(),
        };
    }

    function applyThemeToChart(ch) {
        var c = getChartColors();
        if (!ch) return;
        var scales = ch.options.scales;
        Object.keys(scales).forEach(function(axis) {
            if (scales[axis].ticks) scales[axis].ticks.color = c.text;
            if (scales[axis].title) scales[axis].title.color = c.text;
            if (scales[axis].grid) scales[axis].grid.color = c.grid;
            else scales[axis].grid = {color: c.grid};
        });
        if (ch.options.plugins.legend) ch.options.plugins.legend.labels = {color: c.text};
        if (ch.options.plugins.title) ch.options.plugins.title.color = c.text;
    }

    function applyThemeToAllCharts() {
        [balanceChart, assetBDChart, liabilityBDChart, ratioChart, copperChart, sovereignFundChart].forEach(applyThemeToChart);
        [balanceChart, assetBDChart, liabilityBDChart, ratioChart, copperChart, sovereignFundChart].forEach(function(ch) {
            if (ch) ch.update();
        });
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        document.getElementById('themeIcon').textContent = theme === 'dark' ? '\u2600' : '\u263E';
        localStorage.setItem('theme', theme);
        setTimeout(applyThemeToAllCharts, 10);
    }

    var savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setTheme('dark');
    }

    document.getElementById('themeToggle').addEventListener('click', function() {
        var current = document.documentElement.getAttribute('data-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
    });

    // ── Data table ────────────────────────────────────────────────
    function renderDataTable() {
        var range = getFilteredIndices(BAL.labels);
        var s = range[0], e = range[1];
        var labels = BAL.labels.slice(s, e);
        var assets = BAL[currentCurrency].assets.slice(s, e);
        var liab = BAL[currentCurrency].liabilities.slice(s, e);
        var net = BAL[currentCurrency].net.slice(s, e);

        var thead = document.getElementById('dataTableHead');
        var tbody = document.getElementById('dataTableBody');

        thead.innerHTML = '<tr><th>' + t('date') + '</th><th>' + t('assets')
            + '</th><th>' + t('liabilities') + '</th><th>' + t('netPosition') + '</th></tr>';

        var rows = [];
        for (var i = labels.length - 1; i >= 0; i--) {
            var netClass = net[i] >= 0 ? 'positive' : 'negative';
            rows.push(
                '<tr><td>' + labels[i]
                + '</td><td>' + fmtFull(assets[i])
                + '</td><td>' + fmtFull(liab[i])
                + '</td><td class="' + netClass + '">' + fmtFull(net[i])
                + '</td></tr>'
            );
        }
        tbody.innerHTML = rows.join('');
    }

    renderDataTable();

    var sticky = document.getElementById('stickyControls');
    window.addEventListener('scroll', function() {
        sticky.classList.toggle('scrolled', window.scrollY > 60);
    });
}
