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
        bonds: 'Bonds',
        other: 'Other',
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
        bonds: 'Bonos',
        other: 'Otros',
    },
};

var currentLang = (window.location.hash === '#es') ? 'es' : 'en';
function t(key) { return I18N[currentLang][key] || key; }
function numLocale() { return currentLang === 'es' ? 'es-CL' : 'en-US'; }

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
        });
    });

    var sticky = document.getElementById('stickyControls');
    window.addEventListener('scroll', function() {
        sticky.classList.toggle('scrolled', window.scrollY > 60);
    });
}
