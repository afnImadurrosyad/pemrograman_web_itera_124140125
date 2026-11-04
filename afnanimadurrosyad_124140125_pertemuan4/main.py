"""Program utama yang menggunakan seluruh fungsi math_operations.

Menunjukkan dua cara impor modul yang berbeda:
1. `import math_operations` untuk fungsi geometri.
2. `from math_operations import ...` untuk konversi suhu dan konstanta PI.
"""

import math_operations
from math_operations import PI, celsius_ke_fahrenheit, celsius_ke_kelvin


def main():
    """Jalankan seluruh fungsi modul dengan nilai pengujian."""
    print("=" * 52)
    print("DEMO MODUL MATEMATIKA")
    print("=" * 52)

    print("\n-- Geometri (import math_operations) --")
    print(f"Persegi sisi 5        : luas "
          f"{math_operations.luas_persegi(5):.2f}, "
          f"keliling {math_operations.keliling_persegi(5):.2f}")
    print(f"Persegi panjang 8 x 3 : luas "
          f"{math_operations.luas_persegi_panjang(8, 3):.2f}, "
          f"keliling {math_operations.keliling_persegi_panjang(8, 3):.2f}")
    print(f"Lingkaran r = 7       : luas "
          f"{math_operations.luas_lingkaran(7):.2f}, "
          f"keliling {math_operations.keliling_lingkaran(7):.2f}")

    print("\n-- Konversi Suhu (from math_operations import ...) --")
    print(f"25 C = {celsius_ke_fahrenheit(25):.2f} F")
    print(f"25 C = {celsius_ke_kelvin(25):.2f} K")
    print(f"100 C = {celsius_ke_fahrenheit(100):.2f} F")
    print(f"100 C = {celsius_ke_kelvin(100):.2f} K")

    print(f"\nKonstanta PI yang dipakai modul: {PI}")


if __name__ == "__main__":
    main()
