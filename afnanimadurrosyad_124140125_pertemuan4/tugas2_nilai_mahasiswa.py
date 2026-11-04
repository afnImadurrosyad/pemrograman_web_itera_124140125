"""Program Pengelolaan Data Nilai Mahasiswa.

Menghitung nilai akhir dari bobot 30% UTS + 40% UAS + 30% tugas,
menentukan grade A-E, menampilkan data dalam tabel rapi, serta
mencari nilai akhir tertinggi dan terendah.
"""

# Data contoh untuk demonstrasi perhitungan. Bukan data nilai nyata.
DATA_MAHASISWA = [
    {"nama": "Andi Pratama", "nim": "124140001",
     "nilai_uts": 90, "nilai_uas": 92, "nilai_tugas": 88},
    {"nama": "Budi Santoso", "nim": "124140002",
     "nilai_uts": 75, "nilai_uas": 78, "nilai_tugas": 80},
    {"nama": "Citra Lestari", "nim": "124140003",
     "nilai_uts": 65, "nilai_uas": 68, "nilai_tugas": 70},
    {"nama": "Dewi Anggraini", "nim": "124140004",
     "nilai_uts": 55, "nilai_uas": 58, "nilai_tugas": 52},
    {"nama": "Eko Wijaya", "nim": "124140005",
     "nilai_uts": 40, "nilai_uas": 45, "nilai_tugas": 50},
    {"nama": "Fitri Rahmawati", "nim": "124140006",
     "nilai_uts": 80, "nilai_uas": 80, "nilai_tugas": 80},
]


def hitung_nilai_akhir(nilai_uts, nilai_uas, nilai_tugas):
    """Hitung nilai akhir dengan bobot 30% UTS, 40% UAS, 30% tugas.

    Args:
        nilai_uts (float): Nilai UTS.
        nilai_uas (float): Nilai UAS.
        nilai_tugas (float): Nilai tugas.

    Returns:
        float: Nilai akhir mahasiswa.
    """
    return (0.30 * nilai_uts) + (0.40 * nilai_uas) + (0.30 * nilai_tugas)


def tentukan_grade(nilai_akhir):
    """Tentukan grade A-E dari nilai akhir.

    Args:
        nilai_akhir (float): Nilai akhir mahasiswa.

    Returns:
        str: Grade A, B, C, D, atau E.
    """
    if nilai_akhir >= 80:
        return "A"
    elif nilai_akhir >= 70:
        return "B"
    elif nilai_akhir >= 60:
        return "C"
    elif nilai_akhir >= 50:
        return "D"
    else:
        return "E"


def main():
    """Hitung nilai akhir, tampilkan tabel, dan cari nilai ekstrem."""
    hasil = []
    for mahasiswa in DATA_MAHASISWA:
        nilai_akhir = hitung_nilai_akhir(
            mahasiswa["nilai_uts"], mahasiswa["nilai_uas"],
            mahasiswa["nilai_tugas"]
        )
        hasil.append(
            {
                "nama": mahasiswa["nama"],
                "nim": mahasiswa["nim"],
                "nilai_akhir": nilai_akhir,
                "grade": tentukan_grade(nilai_akhir),
            }
        )

    print("=" * 62)
    print("DAFTAR NILAI AKHIR MAHASISWA")
    print("=" * 62)
    print(f"{'Nama':<18}{'NIM':<12}{'Nilai Akhir':>13}  {'Grade':>5}")
    print("-" * 62)
    for item in hasil:
        print(f"{item['nama']:<18}{item['nim']:<12}"
              f"{item['nilai_akhir']:>13.2f}  {item['grade']:>5}")
    print("-" * 62)

    tertinggi = max(hasil, key=lambda item: item["nilai_akhir"])
    terendah = min(hasil, key=lambda item: item["nilai_akhir"])
    print(
        f"\nNilai Akhir Tertinggi: {tertinggi['nama']} "
        f"({tertinggi['nim']}) - {tertinggi['nilai_akhir']:.2f} "
        f"(Grade {tertinggi['grade']})"
    )
    print(
        f"Nilai Akhir Terendah: {terendah['nama']} "
        f"({terendah['nim']}) - {terendah['nilai_akhir']:.2f} "
        f"(Grade {terendah['grade']})"
    )


if __name__ == "__main__":
    main()
