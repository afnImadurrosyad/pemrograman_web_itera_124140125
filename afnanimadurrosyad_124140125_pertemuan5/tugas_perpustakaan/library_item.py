"""Abstract class LibraryItem beserta subclass Book dan Magazine.

Praktikum PAW Pertemuan 5 — Sistem Manajemen Perpustakaan Sederhana.
Nama: Afnan Imadurrosyad | NIM: 124140125 | Kelas: RB
"""

from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Item generik di perpustakaan.

    Encapsulation: id, judul, dan status pinjam disimpan sebagai
    atribut private (name mangling ``__``) sehingga hanya bisa
    dibaca/diubah lewat property dan method yang disediakan.
    Tahun terbit disimpan sebagai atribut protected (``_``).
    """

    def __init__(self, id_item, judul, tahun_terbit):
        self.__id = id_item
        self.__judul = judul
        self._tahun_terbit = tahun_terbit
        self.__dipinjam = False

    @property
    def id(self):
        """ID item (read-only)."""
        return self.__id

    @property
    def judul(self):
        """Judul item (read-only)."""
        return self.__judul

    @property
    def tahun_terbit(self):
        """Tahun terbit item."""
        return self._tahun_terbit

    @property
    def is_dipinjam(self):
        """Status pinjam item: True jika sedang dipinjam."""
        return self.__dipinjam

    @property
    def status(self):
        """Status ketersediaan dalam bentuk teks."""
        return "Dipinjam" if self.__dipinjam else "Tersedia"

    def pinjam(self):
        """Tandai item sebagai dipinjam. Gagal jika sudah dipinjam."""
        if self.__dipinjam:
            return False
        self.__dipinjam = True
        return True

    def kembalikan(self):
        """Tandai item sebagai tersedia kembali."""
        if not self.__dipinjam:
            return False
        self.__dipinjam = False
        return True

    @abstractmethod
    def get_detail(self):
        """Kembalikan deskripsi lengkap item (di-override tiap subclass)."""

    @abstractmethod
    def hitung_denda(self, hari_terlambat):
        """Hitung denda keterlambatan (Rp) untuk sejumlah hari."""


class Book(LibraryItem):
    """Buku: subclass LibraryItem dengan penulis dan jumlah halaman."""

    DENDA_PER_HARI = 1000

    def __init__(self, id_item, judul, tahun_terbit, penulis, jumlah_halaman):
        super().__init__(id_item, judul, tahun_terbit)
        self.penulis = penulis
        self.jumlah_halaman = jumlah_halaman

    def get_detail(self):
        return (
            f"[Buku] {self.judul} ({self.tahun_terbit}) - "
            f"{self.penulis}, {self.jumlah_halaman} halaman | {self.status}"
        )

    def hitung_denda(self, hari_terlambat):
        if hari_terlambat <= 0:
            return 0
        return hari_terlambat * self.DENDA_PER_HARI


class Magazine(LibraryItem):
    """Majalah: subclass LibraryItem dengan edisi dan bulan terbit."""

    DENDA_PER_HARI = 500

    def __init__(self, id_item, judul, tahun_terbit, edisi, bulan_terbit):
        super().__init__(id_item, judul, tahun_terbit)
        self.edisi = edisi
        self.bulan_terbit = bulan_terbit

    def get_detail(self):
        return (
            f"[Majalah] {self.judul} ({self.tahun_terbit}) - "
            f"Edisi {self.edisi}, {self.bulan_terbit} | {self.status}"
        )

    def hitung_denda(self, hari_terlambat):
        if hari_terlambat <= 0:
            return 0
        return hari_terlambat * self.DENDA_PER_HARI
