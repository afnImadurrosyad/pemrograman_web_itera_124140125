"""Class Library: pengelola koleksi item perpustakaan.

Praktikum PAW Pertemuan 5 — Sistem Manajemen Perpustakaan Sederhana.
Nama: Afnan Imadurrosyad | NIM: 124140125 | Kelas: RB
"""

from library_item import LibraryItem


class Library:
    """Perpustakaan yang menyimpan dan mengelola koleksi item.

    Encapsulation: koleksi disimpan sebagai atribut private
    ``__koleksi`` (dict id -> LibraryItem) dan hanya diakses
    lewat method yang disediakan.
    """

    def __init__(self, nama="Perpustakaan"):
        self.nama = nama
        self.__koleksi = {}

    @property
    def total_item(self):
        """Jumlah seluruh item dalam koleksi."""
        return len(self.__koleksi)

    def tambah_item(self, item):
        """Tambahkan item ke koleksi.

        Menolak item yang bukan LibraryItem dan ID yang sudah ada.
        """
        if not isinstance(item, LibraryItem):
            print("Gagal: hanya objek LibraryItem yang bisa ditambahkan.")
            return False
        if item.id in self.__koleksi:
            print(f"Gagal: ID {item.id} sudah ada di koleksi.")
            return False
        self.__koleksi[item.id] = item
        print(f"Ditambahkan: {item.judul} ({item.id})")
        return True

    def tampilkan_katalog(self, tersedia_saja=False):
        """Tampilkan daftar item; saring hanya yang tersedia bila diminta."""
        if not self.__koleksi:
            print("Katalog masih kosong.")
            return
        for item in self.__koleksi.values():
            if tersedia_saja and item.is_dipinjam:
                continue
            print(f"  {item.id} | {item.get_detail()}")

    def cari_item(self, kata_kunci):
        """Cari item berdasarkan judul (substring) atau id persis.

        Pencarian judul tidak peka huruf besar/kecil.
        """
        kata = kata_kunci.strip().lower()
        hasil = []
        for item in self.__koleksi.values():
            if kata == item.id.lower() or kata in item.judul.lower():
                hasil.append(item)
        return hasil

    def pinjam_item(self, id_item, member):
        """Pinjamkan item ke anggota berdasarkan id."""
        item = self.__koleksi.get(id_item)
        if item is None:
            print(f"Item {id_item} tidak ditemukan.")
            return False
        if member.pinjam(item):
            print(f"{member.nama} meminjam: {item.judul}")
            return True
        print(f"Gagal: {item.judul} sedang dipinjam.")
        return False

    def kembalikan_item(self, id_item, member):
        """Kembalikan item yang dipinjam anggota berdasarkan id."""
        item = self.__koleksi.get(id_item)
        if item is None:
            print(f"Item {id_item} tidak ditemukan.")
            return False
        if member.kembalikan(item):
            print(f"{member.nama} mengembalikan: {item.judul}")
            return True
        print(f"Gagal: {item.judul} tidak dipinjam oleh {member.nama}.")
        return False
