const API = window.location.origin;
const $ = s => document.querySelector(s);

const form     = $('#search-form');
const input    = $('#search-input');
const hero     = $('#hero');
const results  = $('#results');
const list     = $('#results-list');
const info     = $('#results-info');
const clear    = $('#results-clear');
const loader   = $('#loader');
const empty    = $('#empty');
const stats    = $('#stats-panel');
const statsG   = $('#stats-grid');
const statsBtn = $('#stats-toggle');
const statsX   = $('#stats-close');
const countEl  = $('#doc-count');
const countPill = $('#doc-count-pill');

let busy = false;

// ⌘K shortcut
document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); input.focus(); }
    if (e.key === 'Escape') input.blur();
});

// Search
form.addEventListener('submit', e => { e.preventDefault(); go(input.value.trim()); });
document.querySelectorAll('.chip').forEach(c =>
    c.addEventListener('click', () => { input.value = c.dataset.q; go(c.dataset.q); })
);

async function go(q) {
    if (!q || busy) return;
    busy = true;
    hero.classList.add('compact');
    results.hidden = true;
    empty.hidden = true;
    stats.hidden = true;
    loader.hidden = false;

    try {
        const r = await fetch(`${API}/api/search?q=${encodeURIComponent(q)}&top_k=10`);
        const d = await r.json();
        loader.hidden = true;
        if (!d.results.length) { empty.hidden = false; }
        else { render(d); results.hidden = false; }
    } catch {
        loader.hidden = true;
        empty.hidden = false;
        empty.querySelector('p').textContent = 'Could not reach API.';
    }
    busy = false;
}

function render(d) {
    info.textContent = `${d.total} results for "${d.query}"`;
    list.innerHTML = d.results.map((r, i) => `
        <a href="${esc(r.url)}" target="_blank" rel="noopener" class="item" id="result-${i}" style="animation-delay:${i*.02}s">
            <span class="item__rank">${i+1}</span>
            <div class="item__body">
                <div class="item__row">
                    <h3 class="item__title">${esc(r.title || 'Untitled')}</h3>
                    <span class="item__score">${r.score}</span>
                </div>
                <p class="item__preview">${esc(r.preview)}</p>
                <div class="item__meta">
                    <span class="item__src item__src--${r.source}">${r.source}</span>
                    <span class="item__url">${esc(short(r.url))}</span>
                </div>
            </div>
        </a>
    `).join('');
}

// Clear
clear.addEventListener('click', () => {
    hero.classList.remove('compact');
    results.hidden = true;
    empty.hidden = true;
    input.value = '';
    input.focus();
});

// Stats
statsBtn.addEventListener('click', async () => {
    if (!stats.hidden) { stats.hidden = true; return; }
    try {
        const r = await fetch(`${API}/api/stats`);
        const d = await r.json();
        const cm = { github:'github', reddit:'reddit', medium:'medium' };
        statsG.innerHTML = `
            <div class="stat-tile"><div class="stat-tile__val stat-tile__val--all">${d.total_documents.toLocaleString()}</div><div class="stat-tile__lbl">Total</div></div>
            ${Object.entries(d.sources).map(([n,c]) => `
                <div class="stat-tile"><div class="stat-tile__val stat-tile__val--${cm[n]||'all'}">${c.toLocaleString()}</div><div class="stat-tile__lbl">${n}</div></div>
            `).join('')}
        `;
        stats.hidden = false;
    } catch {}
});
statsX.addEventListener('click', () => { stats.hidden = true; });

// Init count
(async () => {
    try {
        const r = await fetch(`${API}/api/stats`);
        const d = await r.json();
        const n = d.total_documents.toLocaleString();
        countEl.textContent = n;
        countPill.textContent = `${n} docs`;
    } catch {}
})();

// Helpers
function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
function short(u) { try { const o = new URL(u); let p = o.pathname; if (p.length > 30) p = p.slice(0,27)+'…'; return o.hostname+p; } catch { return u.slice(0,40); } }
