(function() {
  const currentPage = document.body.dataset.page || 'home';

  const navItems = [
    { href: 'index.html', page: 'home', label: 'Home', online: true },
    { href: 'news.html', page: 'news', label: 'News', online: true },
    { href: 'research.html', page: 'research', label: 'Research', online: true },
    { href: 'assets.html', page: 'assets', label: 'Frontier Assets', online: true },
    { href: 'funding.html', page: 'funding', label: 'Funding Ops', online: true },
    { href: 'portfolio.html', page: 'portfolio', label: 'Portfolio', online: false },
    { href: 'signals.html', page: 'signals', label: 'Frontier Signals', online: false },
    { href: 'commodities.html', page: 'commodities', label: 'Commodities', online: false },
    { href: 'recreation.html', page: 'recreation', label: 'Recreation Bay', online: true },
  ];

  const links = navItems.map(item => {
    const isActive = item.page === currentPage;
    const isDisabled = !item.online;
    let cls = 'nav-item';
    if (isActive) cls += ' active';
    if (isDisabled) cls += ' disabled';
    const dot = item.online
      ? '<span class="status-dot online"></span>'
      : '<span class="status-dot offline"></span>';
    const soonBadge = isDisabled
      ? '<span style="font-size:8px;color:#5A6178;border:1px solid #2A2F3A;padding:1px 4px;border-radius:2px;margin-left:6px">SOON</span>'
      : '';
    return `<a href="${item.href}" class="${cls}">
      <span class="nav-label">${item.label}${soonBadge}</span>
      ${dot}
    </a>`;
  }).join('');

  const sidebar = `
    <aside class="sidebar">
      <div class="sidebar-top">
        <a href="index.html" class="sidebar-logo">
          <img src="robotlogo.png" alt="Robotnik" class="sidebar-logo-img">
          <span class="sidebar-logo-text">ROBOTNIK</span>
        </a>
        <nav class="sidebar-nav">
          ${links}
        </nav>
      </div>
      <div class="sidebar-bottom">
        <div class="sidebar-tagline">
          <span style="color:var(--yellow)">ROBOTNIK</span> <span style="color:var(--text)">RE-ENTRY</span><br>
          <span style="color:var(--text)">IN PROGRESS</span><span class="animated-dots" style="color:var(--text)"></span>
          <div style="margin-top:0.4rem;color:var(--text-muted);line-height:1.5;">The intelligence layer<br>for the frontier<br>technology stack</div>
        </div>
      </div>
    </aside>
  `;

  const topBar = `
    <header class="top-bar">
      <div class="top-bar-left">
        <input type="text" class="top-search" placeholder="Search assets, news, research..." />
      </div>
      <div class="top-bar-right">
        <a href="#" onclick="openEarlyAccess();return false;" class="btn-y">Request Early Access</a>
      </div>
    </header>
  `;

  document.getElementById('nav-container').innerHTML = sidebar + topBar;

  // Early Access modal (shared across all pages)
  var modalDiv = document.createElement('div');
  modalDiv.id = 'early-access-modal';
  modalDiv.style.cssText = 'display:none;position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,0.8);align-items:center;justify-content:center;';
  modalDiv.innerHTML = `
    <div style="background:#0A0A0F;border:1px solid #333;border-radius:8px;padding:2rem 2.5rem;max-width:460px;width:90%;position:relative;font-family:var(--font);">
      <button onclick="document.getElementById('early-access-modal').style.display='none'" style="position:absolute;top:12px;right:16px;background:none;border:none;color:#888;font-size:18px;cursor:pointer;">&#10005;</button>
      <h3 style="color:#F5D921;font-size:12px;letter-spacing:0.1em;margin:0 0 0.75rem;">REQUEST EARLY ACCESS</h3>
      <p style="color:#8B92A5;font-size:10px;line-height:1.6;margin-bottom:1.25rem;">
        Join the Robotnik early access programme. Enterprise operatives receive the full Intelligence data layer, funding database, news archive, data export, and priority access to Portfolio Intelligence, Frontier Signals, and Commodities as they launch.
      </p>
      <div id="mailchimp-form-container">
        <form action="https://formspree.io/f/placeholder" method="POST" style="display:flex;flex-direction:column;gap:0.5rem;" onsubmit="this.querySelector('[type=submit]').textContent='Submitted!';this.querySelector('[type=submit]').disabled=true;">
          <input type="email" name="email" placeholder="Email address *" required style="width:100%;padding:0.5rem;background:#111;border:1px solid #333;color:#E0E0E0;border-radius:3px;font-family:var(--font);font-size:10px;">
          <input type="text" name="name" placeholder="Name *" required style="width:100%;padding:0.5rem;background:#111;border:1px solid #333;color:#E0E0E0;border-radius:3px;font-family:var(--font);font-size:10px;">
          <input type="text" name="company" placeholder="Company / Organisation" style="width:100%;padding:0.5rem;background:#111;border:1px solid #333;color:#E0E0E0;border-radius:3px;font-family:var(--font);font-size:10px;">
          <input type="url" name="linkedin" placeholder="LinkedIn profile URL" style="width:100%;padding:0.5rem;background:#111;border:1px solid #333;color:#E0E0E0;border-radius:3px;font-family:var(--font);font-size:10px;">
          <select name="source" style="width:100%;padding:0.5rem;background:#111;border:1px solid #333;color:#8B92A5;border-radius:3px;font-family:var(--font);font-size:10px;">
            <option value="">How did you hear about Robotnik?</option>
            <option value="linkedin">LinkedIn</option>
            <option value="twitter">Twitter / X</option>
            <option value="referral">Referral</option>
            <option value="search">Search</option>
            <option value="report">1Q26 Report</option>
            <option value="other">Other</option>
          </select>
          <button type="submit" style="width:100%;margin-top:0.5rem;padding:0.6rem;background:#F5D921;color:#0A0A0F;font-family:var(--font);font-weight:700;font-size:10px;letter-spacing:0.06em;border:none;border-radius:3px;cursor:pointer;">Submit Request &rarr;</button>
        </form>
        <p style="color:#5A6178;font-size:8px;margin-top:0.5rem;text-align:center;">Mailchimp integration pending. Form submissions are temporarily collected via email.</p>
      </div>
    </div>
  `;
  modalDiv.addEventListener('click', function(e) { if (e.target === modalDiv) modalDiv.style.display = 'none'; });
  document.body.appendChild(modalDiv);

  // ─────────────────────────────────────────────────────────────────
  // Top-bar search
  // ─────────────────────────────────────────────────────────────────
  // Client-side substring match across four existing datasets. The
  // Messari-style command palette (cmd+K, LLM query routing, etc.)
  // is the separate Q2 "Intelligence Queries" project — intentionally
  // out of scope here. Keep this stub: load JSON on first keystroke,
  // cache in memory, rank results per category (Research → Assets →
  // News → Funding), cap at 10 total.
  var searchInput = document.querySelector('.top-search');
  var searchHost = document.querySelector('.top-bar-left');
  if (searchInput && searchHost) {
    searchInput.setAttribute('autocomplete', 'off');
    searchInput.setAttribute('placeholder', 'Search assets, news, research, funding...');
    searchHost.style.position = 'relative';

    var dropdown = document.createElement('div');
    dropdown.className = 'search-dropdown';
    dropdown.style.display = 'none';
    searchHost.appendChild(dropdown);

    // Hardcoded for now — the only published research is the 1Q26 report.
    var RESEARCH = [{
      title: '1Q26 State of the Frontier Stack',
      desc: 'Inaugural quarterly report — semiconductors, robotics, space, critical materials',
      tags: ['1q26', 'report', 'quarterly', 'frontier stack', 'state of the frontier', 'nvidia', 'waymo', 'rare earth', 'rare earths'],
      url: 'report-1Q26.html',
    }];

    var _datasets = null;
    function loadDatasets() {
      if (_datasets) return Promise.resolve(_datasets);
      return Promise.all([
        fetch('data/markets/robotnik_public_markets.json').then(function(r){return r.ok?r.json():null;}).catch(function(){return null;}),
        fetch('data/news.json').then(function(r){return r.ok?r.json():null;}).catch(function(){return null;}),
        fetch('data/funding/rounds.json').then(function(r){return r.ok?r.json():null;}).catch(function(){return null;}),
      ]).then(function(out){
        _datasets = { pm: out[0], news: out[1], rounds: out[2] };
        return _datasets;
      });
    }

    function escHtml(s) {
      return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
      });
    }

    function searchAll(q, ds) {
      var ql = q.toLowerCase();
      var out = [];

      // 1. Research (hardcoded)
      RESEARCH.forEach(function(r){
        var hay = (r.title + ' ' + r.desc + ' ' + (r.tags || []).join(' ')).toLowerCase();
        if (hay.indexOf(ql) !== -1) {
          out.push({
            category: 'Research',
            primary: r.title,
            secondary: r.desc,
            url: r.url,
          });
        }
      });

      // 2. Assets
      if (ds.pm && ds.pm.entities) {
        var assetMatches = [];
        var tickers = Object.keys(ds.pm.entities);
        for (var i = 0; i < tickers.length; i++) {
          var ticker = tickers[i];
          var ent = ds.pm.entities[ticker];
          var tl = String(ticker || '').toLowerCase();
          var nl = String(ent.name || '').toLowerCase();
          var sl = String(ent.sector || '').toLowerCase();
          if (tl.indexOf(ql) !== -1 || nl.indexOf(ql) !== -1 || sl.indexOf(ql) !== -1) {
            // Rank: exact-ticker > ticker-prefix > name-prefix > substring.
            var rank = 3;
            if (tl === ql) rank = 0;
            else if (tl.indexOf(ql) === 0) rank = 1;
            else if (nl.indexOf(ql) === 0) rank = 2;
            assetMatches.push({
              category: 'Assets',
              primary: ent.name || ticker,
              secondary: ticker + (ent.sector ? (' · ' + ent.sector) : ''),
              url: 'assets.html?q=' + encodeURIComponent(ticker),
              _rank: rank,
            });
          }
        }
        assetMatches.sort(function(a,b){ return a._rank - b._rank; });
        out.push.apply(out, assetMatches);
      }

      // 3. News
      if (ds.news && Array.isArray(ds.news.items)) {
        for (var j = 0; j < ds.news.items.length; j++) {
          var item = ds.news.items[j];
          var tl2 = String(item.title || '').toLowerCase();
          var me = String(item.mentioned_entities || '').toLowerCase();
          var mt = String(item.mentioned_tickers || '').toLowerCase();
          if (tl2.indexOf(ql) !== -1 || me.indexOf(ql) !== -1 || mt.indexOf(ql) !== -1) {
            var sec = [item.source, item.date].filter(Boolean).join(' · ');
            out.push({
              category: 'News',
              primary: item.title,
              secondary: sec,
              url: item.url || 'news.html',
              external: !!item.url,
            });
          }
        }
      }

      // 4. Funding
      if (ds.rounds && Array.isArray(ds.rounds.rounds)) {
        for (var k = 0; k < ds.rounds.rounds.length; k++) {
          var rnd = ds.rounds.rounds[k];
          var co = String(rnd.company || '').toLowerCase();
          var lead = String(rnd.lead_investors || '').toLowerCase();
          var rsec = String(rnd.sector || '').toLowerCase();
          if (co.indexOf(ql) !== -1 || lead.indexOf(ql) !== -1 || rsec.indexOf(ql) !== -1) {
            var amt = rnd.amount_m ? ('$' + rnd.amount_m + 'm') : '';
            var secStr = [amt, rnd.round, rnd.date].filter(Boolean).join(' · ');
            out.push({
              category: 'Funding',
              primary: rnd.company,
              secondary: secStr,
              url: 'funding.html',
            });
          }
        }
      }

      return out.slice(0, 10);
    }

    var _results = [];
    var _activeIdx = -1;

    function rowNodes() {
      return dropdown.querySelectorAll('.search-dropdown__row');
    }

    function updateActive() {
      var nodes = rowNodes();
      for (var i = 0; i < nodes.length; i++) {
        nodes[i].classList.toggle('search-dropdown__row--active', i === _activeIdx);
      }
      if (_activeIdx >= 0 && nodes[_activeIdx]) {
        nodes[_activeIdx].scrollIntoView({ block: 'nearest' });
      }
    }

    var EMPTY_EXAMPLES = ['NVIDIA', 'rare earths', 'Waymo', '1Q26 report'];

    function renderEmptyState() {
      var html = '<div class="search-dropdown__empty">' +
                 '<span class="search-dropdown__try-label">Try:</span>';
      for (var i = 0; i < EMPTY_EXAMPLES.length; i++) {
        html += '<a class="search-dropdown__try-example" data-example="' +
                escHtml(EMPTY_EXAMPLES[i]) + '" href="#">' +
                escHtml(EMPTY_EXAMPLES[i]) + '</a>';
      }
      html += '</div>';
      dropdown.innerHTML = html;
      dropdown.style.display = 'block';
    }

    function renderResults(results, query) {
      _results = results;
      _activeIdx = -1;
      if (!results.length) {
        dropdown.innerHTML = '<div class="search-dropdown__no-results">' +
          'No results for "' + escHtml(query || '') + '".</div>';
        dropdown.style.display = 'block';
        return;
      }
      // Count per category for the header labels.
      var counts = {};
      for (var c = 0; c < results.length; c++) {
        counts[results[c].category] = (counts[results[c].category] || 0) + 1;
      }
      var html = '';
      var lastCat = '';
      for (var i = 0; i < results.length; i++) {
        var r = results[i];
        if (r.category !== lastCat) {
          html += '<div class="search-dropdown__category">' +
                  '<span>' + escHtml(r.category) + '</span>' +
                  '<span class="search-dropdown__category-count">(' + counts[r.category] + ')</span>' +
                  '</div>';
          lastCat = r.category;
        }
        var tgt = r.external ? ' target="_blank" rel="noopener"' : '';
        html += '<a class="search-dropdown__row" data-idx="' + i + '" href="' +
                escHtml(r.url) + '"' + tgt + '>' +
                '<div class="search-dropdown__row-primary">' + escHtml(r.primary) + '</div>' +
                '<div class="search-dropdown__row-secondary">' + escHtml(r.secondary) + '</div>' +
                '</a>';
      }
      dropdown.innerHTML = html;
      dropdown.style.display = 'block';
    }

    function closeDropdown() {
      dropdown.style.display = 'none';
      _activeIdx = -1;
    }

    function runQuery(q) {
      loadDatasets().then(function(ds){
        // Guard against stale responses if user kept typing.
        if (searchInput.value.trim() !== q) return;
        renderResults(searchAll(q, ds), q);
      });
    }

    searchInput.addEventListener('input', function(){
      var q = searchInput.value.trim();
      if (!q) { renderEmptyState(); return; }
      runQuery(q);
    });

    searchInput.addEventListener('focus', function(){
      if (!searchInput.value.trim()) renderEmptyState();
      else if (_results.length) renderResults(_results, searchInput.value.trim());
    });

    searchInput.addEventListener('keydown', function(e){
      var nodes = rowNodes();
      var n = nodes.length;
      if (e.key === 'ArrowDown') {
        if (!n) return;
        e.preventDefault();
        _activeIdx = (_activeIdx + 1) % n;
        updateActive();
      } else if (e.key === 'ArrowUp') {
        if (!n) return;
        e.preventDefault();
        _activeIdx = (_activeIdx - 1 + n) % n;
        updateActive();
      } else if (e.key === 'Enter') {
        if (_activeIdx >= 0 && nodes[_activeIdx]) {
          e.preventDefault();
          nodes[_activeIdx].click();
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeDropdown();
        searchInput.blur();
      }
    });

    // Click-outside closes the dropdown.
    document.addEventListener('click', function(e){
      if (!searchHost.contains(e.target)) closeDropdown();
    });

    // Clicking a "Try:" example fills the input and runs the search.
    dropdown.addEventListener('click', function(e){
      var tgt = e.target.closest('.search-dropdown__try-example');
      if (!tgt) return;
      e.preventDefault();
      var val = tgt.dataset.example || tgt.textContent;
      searchInput.value = val;
      searchInput.focus();
      runQuery(val.trim());
    });
  }
})();

// Global function to open early access modal
function openEarlyAccess() {
  var m = document.getElementById('early-access-modal');
  if (m) m.style.display = 'flex';
}
