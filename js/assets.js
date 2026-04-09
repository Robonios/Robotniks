// ===== FRONTIER ASSETS PAGE =====
// Loads data from robotnik_public_markets.json — equity entities only (no tokens)

var assetsData = [];
var assetsFiltered = [];
var assetsSector = 'all';
var assetsSort = 'mcap';
var assetsSortDir = -1;
var assetsPerPage = 50;
var assetsCurrentPage = 0;

var SECTOR_MAP_A = {
  'Semiconductors': 'semi', 'Semiconductor': 'semi',
  'Robotics': 'robo',
  'Space': 'space',
  'Materials': 'materials', 'Materials & Inputs': 'materials',
};
var SECTOR_LABELS_A = { semi:'Semi', robo:'Robo', space:'Space', materials:'Materials' };
var SECTOR_CSS_A = { semi:'sector-semi', robo:'sector-robo', space:'sector-space', materials:'sector-materials' };

function fmtPriceA(price, currency) {
  if (!price) return '\u2014';
  var c = (currency || 'USD').toUpperCase();
  var sym = c === 'GBP' ? '\u00a3' : c === 'EUR' ? '\u20ac' : c === 'JPY' ? '\u00a5' : c === 'KRW' ? '\u20a9' :
            c === 'HKD' ? 'HK$' : c === 'CHF' ? 'CHF ' : c === 'TWD' ? 'NT$' : c === 'CNY' ? '\u00a5' :
            c === 'SEK' ? 'SEK ' : c === 'NOK' ? 'NOK ' : c === 'CAD' ? 'C$' : c === 'AUD' ? 'A$' : '$';
  return sym + price.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
}

function fmtMcapA(n) {
  if (!n || n <= 0) return '\u2014';
  if (n >= 1e12) return '$' + (n / 1e12).toFixed(2) + 'T';
  if (n >= 1e9) return '$' + (n / 1e9).toFixed(1) + 'B';
  if (n >= 1e6) return '$' + (n / 1e6).toFixed(0) + 'M';
  return '$' + n.toLocaleString();
}

function fmtPctA(v) {
  if (v === null || v === undefined) return '\u2014';
  var cls = v >= 0 ? 'v-green' : 'v-red';
  var sign = v >= 0 ? '+' : '';
  return '<span class="' + cls + '">' + sign + v.toFixed(2) + '%</span>';
}

function fmtPE(v) {
  if (!v || v <= 0) return '\u2014';
  return v.toFixed(1);
}

function fmtVol(v) {
  if (!v || v <= 0) return '\u2014';
  if (v >= 1e9) return (v / 1e9).toFixed(1) + 'B';
  if (v >= 1e6) return (v / 1e6).toFixed(1) + 'M';
  if (v >= 1e3) return (v / 1e3).toFixed(0) + 'K';
  return v.toLocaleString();
}

// Load data — filter out tokens
(function loadAssets() {
  var cb = '?v=' + Date.now();
  fetch('data/markets/robotnik_public_markets.json' + cb)
    .then(function(r) { return r.ok ? r.json() : null; })
    .then(function(data) {
      if (!data || !data.entities) {
        document.getElementById('assets-summary').textContent = 'Data not yet available. Run calculate_metrics.py first.';
        return;
      }
      // Filter out tokens
      assetsData = Object.values(data.entities).filter(function(e) {
        var sk = SECTOR_MAP_A[e.sector];
        return sk !== undefined; // undefined = Token or unknown sector = excluded
      });

      var total = assetsData.length;
      var withMcap = assetsData.filter(function(e) { return e.market_cap && e.market_cap > 0; }).length;
      document.getElementById('assets-summary').textContent =
        total + ' entities \u00b7 ' + withMcap + ' with market cap \u00b7 Updated ' +
        new Date(data.last_updated).toLocaleDateString('en-US', {month:'short',day:'numeric',year:'numeric'});

      // Sector counts
      var sectorCounts = {};
      assetsData.forEach(function(e) {
        var s = SECTOR_MAP_A[e.sector] || 'unknown';
        sectorCounts[s] = (sectorCounts[s] || 0) + 1;
      });
      var totalMcap = assetsData.reduce(function(sum, e) { return sum + (e.market_cap || 0); }, 0);
      var statsHtml = 'Total Market Cap: ' + fmtMcapA(totalMcap) + '<br>';
      ['semi','robo','space','materials'].forEach(function(s) {
        statsHtml += (SECTOR_LABELS_A[s] || s) + ': ' + (sectorCounts[s] || 0) + ' entities<br>';
      });
      document.getElementById('assets-quick-stats').innerHTML = statsHtml;

      // Tab counts
      var tabs = document.querySelectorAll('#asset-tabs .market-tab');
      tabs.forEach(function(t) {
        var s = t.dataset.sector;
        if (s === 'all') {
          t.textContent = 'All (' + total + ')';
        } else {
          t.textContent = (SECTOR_LABELS_A[s] || s) + ' (' + (sectorCounts[s] || 0) + ')';
        }
      });

      renderAssetsTable();
    });
})();

function filterAssets(btn) {
  document.querySelectorAll('#asset-tabs .market-tab').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  assetsSector = btn.dataset.sector;
  assetsCurrentPage = 0;
  renderAssetsTable();
}

function sortAssets(col) {
  if (assetsSort === col) {
    assetsSortDir *= -1;
  } else {
    assetsSort = col;
    assetsSortDir = -1;
  }
  renderAssetsTable();
}

function assetsPage(delta) {
  var maxPage = Math.ceil(assetsFiltered.length / assetsPerPage) - 1;
  assetsCurrentPage = Math.max(0, Math.min(maxPage, assetsCurrentPage + delta));
  renderAssetsTable();
}

function renderAssetsTable() {
  var tbody = document.getElementById('assets-tbody');
  if (!tbody || !assetsData.length) return;

  var search = (document.getElementById('asset-search').value || '').toLowerCase().trim();

  // Filter
  assetsFiltered = assetsData.filter(function(e) {
    var sectorKey = SECTOR_MAP_A[e.sector] || 'unknown';
    if (assetsSector !== 'all' && sectorKey !== assetsSector) return false;
    if (search && !e.ticker.toLowerCase().includes(search) && !e.name.toLowerCase().includes(search)) return false;
    return true;
  });

  // Sort
  assetsFiltered.sort(function(a, b) {
    var va, vb;
    switch (assetsSort) {
      case 'ticker': va = a.ticker; vb = b.ticker; return va < vb ? -assetsSortDir : va > vb ? assetsSortDir : 0;
      case 'company': va = a.name; vb = b.name; return va < vb ? -assetsSortDir : va > vb ? assetsSortDir : 0;
      case 'price': return ((a.price || 0) - (b.price || 0)) * assetsSortDir;
      case '24h': return ((a.change_24h_pct || 0) - (b.change_24h_pct || 0)) * assetsSortDir;
      case '7d': return ((a.change_7d_pct || 0) - (b.change_7d_pct || 0)) * assetsSortDir;
      case '30d': return ((a.change_30d_pct || 0) - (b.change_30d_pct || 0)) * assetsSortDir;
      case 'ytd': return ((a.change_ytd_pct || 0) - (b.change_ytd_pct || 0)) * assetsSortDir;
      case '1y': return ((a.change_1y_pct || 0) - (b.change_1y_pct || 0)) * assetsSortDir;
      case 'pe': return ((a.pe_ratio || 9999) - (b.pe_ratio || 9999)) * assetsSortDir;
      case 'vol': return ((a.volume || 0) - (b.volume || 0)) * assetsSortDir;
      default: return ((a.market_cap || 0) - (b.market_cap || 0)) * assetsSortDir;
    }
  });

  // Paginate
  var start = assetsCurrentPage * assetsPerPage;
  var pageData = assetsFiltered.slice(start, start + assetsPerPage);

  // Render rows
  var rows = pageData.map(function(e, i) {
    var sKey = SECTOR_MAP_A[e.sector] || 'semi';
    var secCss = SECTOR_CSS_A[sKey] || 'sector-semi';
    var secLabel = SECTOR_LABELS_A[sKey] || e.sector;
    var subsec = e.subsector || '\u2014';
    return '<tr>' +
      '<td>' + (start + i + 1) + '</td>' +
      '<td class="ticker">' + e.ticker + '</td>' +
      '<td class="company-name">' + e.name + '</td>' +
      '<td><span class="sector-tag ' + secCss + '">' + secLabel + '</span></td>' +
      '<td style="font-size:9px;color:var(--text-dim);">' + subsec + '</td>' +
      '<td class="r">' + fmtPriceA(e.price, e.currency) + '</td>' +
      '<td style="font-size:9px;color:var(--text-dim);">' + (e.currency || 'USD') + '</td>' +
      '<td class="r">' + fmtPctA(e.change_24h_pct) + '</td>' +
      '<td class="r">' + fmtPctA(e.change_7d_pct) + '</td>' +
      '<td class="r">' + fmtPctA(e.change_30d_pct) + '</td>' +
      '<td class="r">' + fmtPctA(e.change_ytd_pct) + '</td>' +
      '<td class="r">' + fmtMcapA(e.market_cap) + '</td>' +
      '<td class="r">' + fmtPE(e.pe_ratio) + '</td>' +
      '<td class="r" style="font-size:9px;">' + fmtVol(e.volume) + '</td>' +
      '</tr>';
  }).join('');

  tbody.innerHTML = rows || '<tr><td colspan="14" style="text-align:center;padding:2rem;color:var(--text-dim);">No data available</td></tr>';

  // Pagination info
  var totalPages = Math.ceil(assetsFiltered.length / assetsPerPage);
  document.getElementById('assets-showing').textContent =
    'Showing ' + (assetsFiltered.length ? start + 1 : 0) + '\u2013' + Math.min(start + assetsPerPage, assetsFiltered.length) + ' of ' + assetsFiltered.length;
  document.getElementById('assets-page-info').textContent = 'Page ' + (assetsCurrentPage + 1) + ' of ' + Math.max(totalPages, 1);
  document.getElementById('assets-prev').disabled = assetsCurrentPage === 0;
  document.getElementById('assets-next').disabled = assetsCurrentPage >= totalPages - 1;

  // Sort arrows
  ['#','ticker','company','price','24h','7d','30d','ytd','mcap','pe','vol'].forEach(function(col) {
    var el = document.getElementById('sa-' + col);
    if (el) el.textContent = assetsSort === col ? (assetsSortDir === -1 ? '\u25bc' : '\u25b2') : '';
  });
}
