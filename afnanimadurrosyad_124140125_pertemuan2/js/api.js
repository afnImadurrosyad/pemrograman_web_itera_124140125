/* ============================================================
   api.js — semua akses jaringan (async/await).
   Kedua API publik, tanpa API key:
   - Cuaca   : Open-Meteo (https://open-meteo.com)
   - Quote   : DummyJSON  (https://dummyjson.com)
   - Geocode : Open-Meteo Geocoding (untuk ganti kota)
   ============================================================ */

/** Kota default — gampang diubah, dipakai saat pertama kali dibuka. */
export const DEFAULT_CITY = {
  name: 'Bandar Lampung',
  latitude: -5.42917,
  longitude: 105.26111,
};

/** Label Bahasa Indonesia untuk kode cuaca WMO. */
export const WEATHER_LABELS = {
  0: 'Cerah', 1: 'Cerah berawan', 2: 'Berawan', 3: 'Mendung',
  45: 'Berkabut', 48: 'Berkabut (embun beku)',
  51: 'Gerimis ringan', 53: 'Gerimis', 55: 'Gerimis lebat',
  56: 'Gerimis beku ringan', 57: 'Gerimis beku',
  61: 'Hujan ringan', 63: 'Hujan', 65: 'Hujan lebat',
  66: 'Hujan beku ringan', 67: 'Hujan beku',
  71: 'Salju ringan', 73: 'Salju', 75: 'Salju lebat', 77: 'Butiran salju',
  80: 'Hujan rintik ringan', 81: 'Hujan rintik', 82: 'Hujan rintik lebat',
  85: 'Hujan salju ringan', 86: 'Hujan salju lebat',
  95: 'Badai petir', 96: 'Badai petir + hujan es ringan', 99: 'Badai petir + hujan es',
};

/**
 * Ambil cuaca terkini untuk sebuah koordinat.
 * @param {{ latitude: number, longitude: number }} coords
 * @returns {Promise<{ suhu: number, kelembapan: number, kode: number, kondisi: string, angin: number, waktu: string }>}
 */
export async function fetchWeather({ latitude, longitude }) {
  const url =
    `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}` +
    `&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=Asia%2FJakarta`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Gagal memuat cuaca (HTTP ${res.status})`);

  // Destructuring: ambil objek `current`, lalu pecah field yang dipakai.
  const { current } = await res.json();
  const {
    temperature_2m: suhu,
    relative_humidity_2m: kelembapan,
    weather_code: kode,
    wind_speed_10m: angin,
    time: waktu,
  } = current;

  return {
    suhu: Math.round(suhu),
    kelembapan,
    kode,
    kondisi: WEATHER_LABELS[kode] ?? 'Tidak diketahui',
    angin: Math.round(angin),
    waktu,
  };
}

/**
 * Cari koordinat sebuah nama kota (untuk fitur ganti kota).
 * @param {string} name
 * @returns {Promise<{ name: string, latitude: number, longitude: number }>}
 */
export async function geocodeCity(name) {
  const url =
    `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(name)}` +
    `&count=1&language=id&format=json`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Gagal mencari kota (HTTP ${res.status})`);
  const { results } = await res.json();
  if (!results?.length) throw new Error(`Kota "${name}" tidak ditemukan.`);
  const { name: kota, latitude, longitude } = results[0];
  return { name: kota, latitude, longitude };
}

/**
 * Ambil satu quote acak.
 * @returns {Promise<{ quote: string, author: string }>}
 */
export async function fetchQuote() {
  const res = await fetch('https://dummyjson.com/quotes/random');
  if (!res.ok) throw new Error(`Gagal memuat quote (HTTP ${res.status})`);
  const { quote, author } = await res.json();
  return { quote, author };
}

/** Quote cadangan kalau jaringan bermasalah — aplikasi tetap bisa dipakai. */
export const FALLBACK_QUOTES = [
  { quote: 'Sedikit demi sedikit, lama-lama menjadi bukit.', author: 'Peribahasa Indonesia' },
  { quote: 'Belajar bukan tentang menjadi yang tercepat, tapi tentang tidak berhenti.', author: 'Anonim' },
  { quote: 'Kode yang rapi adalah hadiah untuk dirimu di masa depan.', author: 'Anonim' },
];
