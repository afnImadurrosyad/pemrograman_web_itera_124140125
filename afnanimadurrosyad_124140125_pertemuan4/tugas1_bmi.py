"""Program Penghitung BMI (Body Mass Index) Sederhana.

Menghitung BMI dari berat badan (kg) dan tinggi badan (m), lalu
menentukan kategori berat badan dengan percabangan if-elif-else.
"""

BERAT_MINIMUM = 0
TINGGI_MINIMUM = 0


def hitung_bmi(berat, tinggi):
    """Hitung nilai BMI dari berat dan tinggi.

    Args:
        berat (float): Berat badan dalam kilogram.
        tinggi (float): Tinggi badan dalam meter.

    Returns:
        float: Nilai BMI = berat / (tinggi * tinggi).
    """
    return berat / (tinggi * tinggi)


def kategori_bmi(bmi):
    """Tentukan kategori berat badan dari nilai BMI.

    Args:
        bmi (float): Nilai BMI yang sudah dihitung.

    Returns:
        str: Kategori berat badan.
    """
    if bmi < 18.5:
        return "Berat badan kurang"
    elif bmi < 25:
        return "Berat badan normal"
    elif bmi < 30:
        return "Berat badan berlebih"
    else:
        return "Obesitas"


def main():
    """Minta input berat dan tinggi, lalu cetak BMI dan kategorinya."""
    berat = float(input("Masukkan berat badan (kg): "))
    tinggi = float(input("Masukkan tinggi badan (m): "))

    if berat <= BERAT_MINIMUM or tinggi <= TINGGI_MINIMUM:
        print("Berat dan tinggi harus lebih dari 0.")
        return

    bmi = hitung_bmi(berat, tinggi)
    print(f"\nNilai BMI Anda: {bmi:.2f}")
    print(f"Kategori: {kategori_bmi(bmi)}")


if __name__ == "__main__":
    main()
