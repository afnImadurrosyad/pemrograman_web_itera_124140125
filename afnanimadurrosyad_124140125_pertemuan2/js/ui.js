/* ============================================================
   ui.js — render ke DOM untuk varian "Midnight Bento" (dark-only).
   Menunjukkan: template literals, arrow function, destructuring,
   optional chaining, nullish coalescing.
   ============================================================ */

/** Ambil elemen berdasarkan id. */
export const el = (id) => document.getElementById(id);

/** Escape HTML agar teks todo/kota aman dari injeksi. */
export const escapeHtml = (str) =>
  String(str ?? '').replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

/** Sapaan Bahasa Indonesia berdasarkan jam. */
export const greetingFor = (hour) => {
  if (hour < 11) return 'Selamat pagi';
  if (hour < 15) return 'Selamat siang';
  if (hour < 19) return 'Selamat sore';
  return 'Selamat malam';
};

const dateFmt = new Intl.DateTimeFormat('id-ID', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
});
const timeFmt = new Intl.DateTimeFormat('id-ID', {
  hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
});

/** Isi sapaan + tanggal di tile greeting. */
export function renderGreeting(name) {
  const now = new Date();
  el('greeting').textContent = `${greetingFor(now.getHours())}, ${name}`;
  const long = dateFmt.format(now);
  el('dateLine').textContent = long;
  el('topDate').textContent = long;
}

/** Jam live di topbar, update tiap detik. */
export function startClock() {
  const tick = () => {
    el('clock').textContent = timeFmt.format(new Date());
  };
  tick();
  return setInterval(tick, 1000);
}

/** Statistik ringkas di tile greeting + pill di tile todo. */
export function renderStats({ total, aktif, selesai }) {
  el('miniStats').innerHTML = `
    <div class="stat"><b>${aktif}</b><span>Aktif</span></div>
    <div class="stat"><b>${selesai}</b><span>Selesai</span></div>
    <div class="stat"><b>${total}</b><span>Total</span></div>`;
  el('todoCount').textContent = `${total} tugas`;
}

/** Tandai chip filter yang aktif. */
export function markActiveFilter(filter) {
  document.querySelectorAll('.chip').forEach((chip) => {
    const on = chip.dataset.filter === filter;
    chip.classList.toggle('is-active', on);
    chip.setAttribute('aria-selected', String(on));
  });
}

/** Render daftar todo (mode tampil / mode edit). */
export function renderTodos(todos, { editingId } = {}) {
  const list = el('todoList');
  if (!todos.length) {
    list.innerHTML = `<li class="empty"><p class="muted">Belum ada tugas di sini. Tambahkan yang pertama di atas ✨</p></li>`;
    return;
  }
  list.innerHTML = todos.map((t) => {
    if (t.id === editingId) {
      return `<li class="todo-item" data-id="${t.id}">
        <div class="todo-edit">
          <input type="text" data-edit-input value="${escapeHtml(t.text)}" maxlength="120" aria-label="Ubah tugas">
          <button class="btn btn-accent" data-save="${t.id}">Simpan</button>
          <button class="btn" data-cancel>Batal</button>
        </div>
      </li>`;
    }
    return `<li class="todo-item${t.done ? ' done' : ''}" data-id="${t.id}">
      <button class="todo-check" data-toggle="${t.id}" aria-label="${t.done ? 'Tandai belum selesai' : 'Tandai selesai'}">✓</button>
      <span class="todo-text">${escapeHtml(t.text)}</span>
      <span class="todo-actions">
        <button class="mini-btn" data-edit="${t.id}">Ubah</button>
        <button class="mini-btn danger" data-delete="${t.id}">Hapus</button>
      </span>
    </li>`;
  }).join('');
}

/** Render kartu cuaca dengan suhu besar + grid detail. */
export function renderWeather(data, cityName) {
  el('weatherBody').innerHTML = `
    <div class="weather-hero">
      <div class="weather-temp">${data.suhu}<small>°C</small></div>
      <div>
        <p class="weather-cond">${escapeHtml(data.kondisi)}</p>
        <p class="weather-city muted">📍 ${escapeHtml(cityName)}</p>
      </div>
    </div>
    <div class="weather-grid">
      <div class="weather-cell"><b>${data.kelembapan}%</b><span>Kelembapan</span></div>
      <div class="weather-cell"><b>${data.angin} km/j</b><span>Angin</span></div>
      <div class="weather-cell"><b>${escapeHtml((data.waktu ?? '').slice(11, 16))}</b><span>Diperbarui</span></div>
    </div>`;
}

/** Render quote harian. */
export function renderQuote({ quote, author }, isFallback = false) {
  el('quoteBody').innerHTML = `
    <blockquote>“${escapeHtml(quote)}”</blockquote>
    <cite>— ${escapeHtml(author)}${isFallback ? ' <span class="muted">(offline)</span>' : ''}</cite>`;
}

/** Kotak error dengan tombol coba lagi. */
export function renderError(targetId, message, retryLabel = 'Coba lagi') {
  el(targetId).innerHTML = `
    <div class="error-box">
      <p>${escapeHtml(message)}</p>
      <button class="btn" data-retry>${escapeHtml(retryLabel)}</button>
    </div>`;
}
