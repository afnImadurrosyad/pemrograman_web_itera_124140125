/* ============================================================
   main.js — entry point varian "Midnight Bento" (dark-only).
   Tanpa toggle tema: satu palet gelap untuk seluruh aplikasi.
   Menunjukkan: module import/export, async/await, arrow function,
   destructuring, spread, try/catch, optional chaining.
   ============================================================ */

import { DEFAULT_CITY, FALLBACK_QUOTES, fetchQuote, fetchWeather, geocodeCity } from './api.js';
import { Storage, addTodo, countTodos, editTodoText, filterTodos, removeTodo, toggleTodo } from './store.js';
import {
  el, escapeHtml, markActiveFilter, renderError, renderGreeting,
  renderQuote, renderStats, renderTodos, renderWeather, startClock,
} from './ui.js';

// --- Penyimpanan lokal (key sendiri supaya tidak bentrok dengan varian terang) ---
const todoStore = new Storage('dashdark.todos.v1');
const cityStore = new Storage('dashdark.city.v1');

// --- State aplikasi ---
let todos = todoStore.load([]);
let filter = 'semua';
let query = '';
let editingId = null;
let city = cityStore.load(DEFAULT_CITY);

const persistTodos = () => todoStore.save(todos);

/** Render ulang daftar + statistik todo. */
function refreshTodos() {
  const visible = filterTodos(todos, filter, query);
  renderTodos(visible, { editingId });
  renderStats(countTodos(todos));
}

// --- Cuaca ---
async function loadWeather() {
  const btn = el('weatherRefresh');
  btn.disabled = true;
  try {
    const data = await fetchWeather(city);
    renderWeather(data, city.name);
  } catch (err) {
    renderError('weatherBody', err.message, 'Muat ulang cuaca');
  } finally {
    btn.disabled = false;
  }
}

// --- Quote ---
async function loadQuote() {
  try {
    const data = await fetchQuote();
    renderQuote(data);
  } catch {
    // Jaringan gagal: pakai quote cadangan supaya aplikasi tetap hidup.
    const fallback = FALLBACK_QUOTES[Math.floor(Math.random() * FALLBACK_QUOTES.length)];
    renderQuote(fallback, true);
  }
}

// --- Event: form tambah todo ---
el('todoForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const input = el('todoInput');
  const text = input.value.trim();
  if (!text) {
    input.focus();
    return;
  }
  todos = addTodo(todos, text); // spread: state baru, bukan mutasi
  persistTodos();
  input.value = '';
  input.focus();
  refreshTodos();
});

// --- Event: klik di dalam daftar todo (toggle / edit / hapus / simpan) ---
el('todoList').addEventListener('click', (e) => {
  const { toggle, edit, delete: del, save } = e.target.dataset;

  if (toggle) {
    todos = toggleTodo(todos, toggle);
    persistTodos();
    refreshTodos();
    return;
  }
  if (del && confirm('Hapus tugas ini?')) {
    todos = removeTodo(todos, del);
    persistTodos();
    refreshTodos();
    return;
  }
  if (edit) {
    editingId = edit;
    refreshTodos();
    el('todoList').querySelector('[data-edit-input]')?.focus();
    return;
  }
  if (e.target.hasAttribute('data-cancel')) {
    editingId = null;
    refreshTodos();
    return;
  }
  if (save) {
    const input = el('todoList').querySelector('[data-edit-input]');
    const text = input?.value.trim() ?? '';
    if (text) {
      todos = editTodoText(todos, save, text);
      persistTodos();
    }
    editingId = null;
    refreshTodos();
  }
});

// Tombol "coba lagi" di dalam kartu cuaca (muncul saat fetch gagal).
el('weatherBody').addEventListener('click', (e) => {
  if (e.target.hasAttribute('data-retry')) loadWeather();
});

// Simpan dengan Enter / batal dengan Escape saat mode edit.
el('todoList').addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.target.hasAttribute('data-edit-input')) {
    e.target.closest('.todo-item')?.querySelector('[data-save]')?.click();
  }
  if (e.key === 'Escape') {
    editingId = null;
    refreshTodos();
  }
});

// --- Event: filter tab ---
document.querySelector('.filters').addEventListener('click', (e) => {
  const btn = e.target.closest('.chip');
  if (!btn) return;
  filter = btn.dataset.filter;
  markActiveFilter(filter);
  refreshTodos();
});

// --- Event: pencarian ---
el('todoSearch').addEventListener('input', (e) => {
  query = e.target.value;
  refreshTodos();
});

// --- Event: ganti kota cuaca ---
el('cityForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = el('cityInput');
  const name = input.value.trim();
  if (!name) return;
  el('weatherBody').innerHTML = `<p class="muted">Mencari kota "${escapeHtml(name)}"…</p>`;
  try {
    city = await geocodeCity(name);
    cityStore.save(city);
    input.value = '';
    await loadWeather();
  } catch (err) {
    renderError('weatherBody', err.message, 'Muat ulang cuaca');
  }
});

// --- Event: refresh cuaca & quote ---
el('weatherRefresh').addEventListener('click', loadWeather);
el('quoteRefresh').addEventListener('click', loadQuote);
el('quoteBody').addEventListener('click', (e) => {
  if (e.target.hasAttribute('data-retry')) loadQuote();
});

// --- Inisialisasi (tanpa tema: gelap selalu) ---
renderGreeting('Afnan');
startClock();
refreshTodos();
loadWeather();
loadQuote();
