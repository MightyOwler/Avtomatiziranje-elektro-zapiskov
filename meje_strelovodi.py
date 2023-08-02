from openpyxl import load_workbook

RDECA = "FF0000"
ORANZNA = "FFA500"
MODRA = "99FFFF"


def preveri_meje_strelovodi(seznam, trafo=True):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo

    slovar_problematicnih_meritev = dict()

    R = float(seznam[2].replace(">", "").replace(",", "."))
    if R > 1 and R < 10:
        slovar_problematicnih_meritev[2] = ORANZNA
    elif R >= 10:
        slovar_problematicnih_meritev[2] = RDECA

    return slovar_problematicnih_meritev
