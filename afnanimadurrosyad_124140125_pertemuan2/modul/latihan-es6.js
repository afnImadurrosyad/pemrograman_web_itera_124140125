/* ============================================================
   latihan-es6.js — Latihan mengikuti modul Pertemuan 2:
   "JavaScript Next Gen (ES6+)".
   Jalankan: node modul/latihan-es6.js
   ============================================================ */

// 1. let/const + arrow function + template literals
const sapa = (nama) => `Halo, ${nama}! Selamat belajar ES6+.`;
console.log('1.', sapa('Afnan'));

// 2. Destructuring object & array
const mahasiswa = { nama: 'Afnan Imadurrosyad', nim: '124140125', kelas: 'RB' };
const { nama, nim, kelas } = mahasiswa;
const [pertama, kedua] = ['Bandar Lampung', 'Jakarta', 'Bandung'];
console.log('2.', `${nama} (${nim}) kelas ${kelas} — kota: ${pertama}, ${kedua}`);

// 3. Spread (gabung array) & rest (sisa argumen)
const tugasA = ['Belajar ES6', 'Buat dashboard'];
const tugasB = ['Push ke GitHub'];
const semua = [...tugasA, ...tugasB];
const jumlahkan = (...angka) => angka.reduce((a, b) => a + b, 0);
console.log('3.', semua, '| total:', jumlahkan(10, 20, 30));

// 4. Modern array methods: map, filter, reduce
const todos = [
  { teks: 'Kerjakan PAW', selesai: true },
  { teks: 'Baca paper ECG-Mamba', selesai: false },
  { teks: 'Olahraga', selesai: false },
];
const ringkasan = todos
  .filter((t) => !t.selesai)
  .map((t) => t.teks.toUpperCase());
const persen = Math.round(
  (todos.filter((t) => t.selesai).length / todos.length) * 100,
);
console.log('4. Belum selesai:', ringkasan, `| progres: ${persen}%`);

// 5. Class + default parameter
class Pengingat {
  constructor(pesan, jam = '07:00') {
    this.pesan = pesan;
    this.jam = jam;
  }
  info() {
    return `[${this.jam}] ${this.pesan}`;
  }
}
console.log('5.', new Pengingat('Kumpulkan tugas PAW').info());

// 6. Async/await + fetch (butuh Node 18+)
const cekCuaca = async () => {
  try {
    const res = await fetch(
      'https://api.open-meteo.com/v1/forecast?latitude=-5.42917&longitude=105.26111&current=temperature_2m',
    );
    const { current } = await res.json();
    console.log('6. Suhu Bandar Lampung sekarang:', current.temperature_2m, '°C');
  } catch {
    console.log('6. Gagal fetch cuaca (cek koneksi internet).');
  }
};
cekCuaca();
