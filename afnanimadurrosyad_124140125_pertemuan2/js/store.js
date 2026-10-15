/* ============================================================
   store.js — state + penyimpanan localStorage.
   Menunjukkan: class, arrow function, spread/rest,
   array methods (map/filter/reduce).
   ============================================================ */

/** Pembungkus localStorage yang aman (tahan JSON rusak / storage penuh). */
export class Storage {
  constructor(key) {
    this.key = key;
  }

  load(fallback) {
    try {
      const raw = localStorage.getItem(this.key);
      return raw === null ? fallback : JSON.parse(raw);
    } catch {
      return fallback;
    }
  }

  save(data) {
    try {
      localStorage.setItem(this.key, JSON.stringify(data));
    } catch (err) {
      console.warn(`Gagal menyimpan ${this.key}:`, err);
    }
  }
}

let seq = Date.now();

/** Bikin objek todo baru. */
export const createTodo = (text) => ({
  id: `todo-${seq++}-${Math.random().toString(36).slice(2, 7)}`,
  text: text.trim(),
  done: false,
  createdAt: new Date().toISOString(),
});

// --- Update state secara immutable (spread) ---

/** Tambah todo ke daftar. */
export const addTodo = (todos, text) => [...todos, createTodo(text)];

/** Balik status selesai/belum sebuah todo. */
export const toggleTodo = (todos, id) =>
  todos.map((t) => (t.id === id ? { ...t, done: !t.done } : t));

/** Ubah teks sebuah todo. */
export const editTodoText = (todos, id, text) =>
  todos.map((t) => (t.id === id ? { ...t, text: text.trim() } : t));

/** Hapus sebuah todo. */
export const removeTodo = (todos, id) => todos.filter((t) => t.id !== id);

/** Hitung statistik dengan reduce: { total, aktif, selesai }. */
export const countTodos = (todos) =>
  todos.reduce(
    (acc, t) => {
      acc.total += 1;
      if (t.done) acc.selesai += 1;
      else acc.aktif += 1;
      return acc;
    },
    { total: 0, aktif: 0, selesai: 0 },
  );

/** Filter daftar sesuai tab + kata kunci pencarian. */
export const filterTodos = (todos, filter, query = '') => {
  const q = query.trim().toLowerCase();
  return todos
    .filter((t) => {
      if (filter === 'aktif') return !t.done;
      if (filter === 'selesai') return t.done;
      return true;
    })
    .filter((t) => (q ? t.text.toLowerCase().includes(q) : true))
    // Urutkan: yang belum selesai dulu, lalu yang terbaru.
    .sort((a, b) => Number(a.done) - Number(b.done) || b.createdAt.localeCompare(a.createdAt));
};
