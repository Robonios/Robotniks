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
})();

// Global function to open early access modal
function openEarlyAccess() {
  var m = document.getElementById('early-access-modal');
  if (m) m.style.display = 'flex';
}
