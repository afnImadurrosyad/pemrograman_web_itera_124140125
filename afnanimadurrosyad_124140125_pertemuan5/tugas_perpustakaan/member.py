"""Class Member: anggota perpustakaan yang meminjam item.

Praktikum PAW Pertemuan 5 — Sistem Manajemen Perpustakaan Sederhana.
Nama: Afnan Imadurrosyad | NIM: 124140125 | Kelas: RB
"""


class Member:
    """Anggota perpustakaan.

    Encapsulation: nama dan ID anggota disimpan sebagai atribut
    private, daftar pinjaman sebagai atribut protected.
    """

    def __init__(self, id_member, nama):
        self.__id_member = id_member
        self.__nama = nama
        self._daftar_pinjaman = []

    @property
    def id_member(self):
        """ID anggota (read-only)."""
        return self.__id_member

    @property
    def nama(self):
        """Nama anggota (read-only)."""
        return self.__nama

    @property
    def jumlah_pinjaman(self):
        """Jumlah item yang sedang dipinjam anggota ini."""
        return len(self._daftar_pinjaman)

    def pinjam(self, item):
        """Pinjam satu item. Gagal jika item sedang dipinjam orang lain."""
        if not item.pinjam():
            return False
        self._daftar_pinjaman.append(item)
        return True

    def kembalikan(self, item):
        """Kembalikan satu item yang dipinjam anggota ini."""
        if item not in self._daftar_pinjaman:
            return False
        item.kembalikan()
        self._daftar_pinjaman.remove(item)
        return True

    def daftar_pinjaman(self):
        """Kembalikan salinan daftar item yang sedang dipinjam."""
        return list(self._daftar_pinjaman)
