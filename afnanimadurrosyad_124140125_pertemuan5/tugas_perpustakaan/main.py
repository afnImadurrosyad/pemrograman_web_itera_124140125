"""Demo Sistem Manajemen Perpustakaan Sederhana (PAW Pertemuan 5).

Menjalankan:  python main.py   (dari dalam folder tugas_perpustakaan/)
Data buku/majalah di bawah adalah data contoh untuk demonstrasi.
"""

from library_item import Book, Magazine
from library import Library
from member import Member


def main():
    perpus = Library("Perpustakaan ITERA")

    print("=== 1. Menambahkan item ===")
    perpus.tambah_item(Book("B001", "Laskar Pelangi", 2005,
                            "Andrea Hirata", 529))
    perpus.tambah_item(Book("B002", "Bumi Manusia", 1980,
                            "Pramoedya Ananta Toer", 535))
    perpus.tambah_item(Book("B003", "Filosofi Teras", 2018,
                            "Henry Manampiring", 346))
    perpus.tambah_item(Magazine("M001", "National Geographic Indonesia",
                                2024, "45", "November"))
    perpus.tambah_item(Magazine("M002", "Tempo", 2024,
                                "5120", "Oktober"))
    print(f"Total item: {perpus.total_item}")

    print("\n=== 2. Katalog lengkap (polymorphism: get_detail) ===")
    perpus.tampilkan_katalog()

    print("\n=== 3. Mencari item berdasarkan judul ===")
    for item in perpus.cari_item("pelangi"):
        print(f"  Ditemukan: {item.get_detail()}")

    print("\n=== 4. Mencari item berdasarkan id ===")
    for item in perpus.cari_item("M001"):
        print(f"  Ditemukan: {item.get_detail()}")

    print("\n=== 5. Peminjaman oleh anggota ===")
    anggota = Member("A001", "Afnan Imadurrosyad")
    perpus.pinjam_item("B001", anggota)
    perpus.pinjam_item("B001", anggota)  # gagal: sudah dipinjam
    print(f"Pinjaman {anggota.nama}: {anggota.jumlah_pinjaman} item")

    print("\n=== 6. Katalog item yang tersedia saja ===")
    perpus.tampilkan_katalog(tersedia_saja=True)

    print("\n=== 7. Denda keterlambatan (polymorphism: hitung_denda) ===")
    for item in perpus.cari_item("B001") + perpus.cari_item("M001"):
        print(f"  {item.judul}: telat 3 hari -> "
              f"Rp{item.hitung_denda(3):,}")

    print("\n=== 8. Pengembalian ===")
    perpus.kembalikan_item("B001", anggota)
    print(f"Pinjaman {anggota.nama}: {anggota.jumlah_pinjaman} item")
    perpus.tampilkan_katalog(tersedia_saja=True)


if __name__ == "__main__":
    main()
