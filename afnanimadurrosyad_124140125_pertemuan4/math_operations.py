"""Modul Matematika: geometri dan konversi suhu."""

PI = 3.14159


def luas_persegi(sisi):
    """Hitung luas persegi.

    Args:
        sisi (float): Panjang sisi persegi.

    Returns:
        float: Luas persegi.
    """
    return sisi * sisi


def keliling_persegi(sisi):
    """Hitung keliling persegi.

    Args:
        sisi (float): Panjang sisi persegi.

    Returns:
        float: Keliling persegi.
    """
    return 4 * sisi


def luas_persegi_panjang(panjang, lebar):
    """Hitung luas persegi panjang.

    Args:
        panjang (float): Panjang persegi panjang.
        lebar (float): Lebar persegi panjang.

    Returns:
        float: Luas persegi panjang.
    """
    return panjang * lebar


def keliling_persegi_panjang(panjang, lebar):
    """Hitung keliling persegi panjang.

    Args:
        panjang (float): Panjang persegi panjang.
        lebar (float): Lebar persegi panjang.

    Returns:
        float: Keliling persegi panjang.
    """
    return 2 * (panjang + lebar)


def luas_lingkaran(jari_jari):
    """Hitung luas lingkaran.

    Args:
        jari_jari (float): Jari-jari lingkaran.

    Returns:
        float: Luas lingkaran.
    """
    return PI * jari_jari * jari_jari


def keliling_lingkaran(jari_jari):
    """Hitung keliling lingkaran.

    Args:
        jari_jari (float): Jari-jari lingkaran.

    Returns:
        float: Keliling lingkaran.
    """
    return 2 * PI * jari_jari


def celsius_ke_fahrenheit(celsius):
    """Konversi suhu Celsius ke Fahrenheit.

    Args:
        celsius (float): Suhu dalam derajat Celsius.

    Returns:
        float: Suhu dalam derajat Fahrenheit.
    """
    return (celsius * 9 / 5) + 32


def celsius_ke_kelvin(celsius):
    """Konversi suhu Celsius ke Kelvin.

    Args:
        celsius (float): Suhu dalam derajat Celsius.

    Returns:
        float: Suhu dalam Kelvin.
    """
    return celsius + 273.15
