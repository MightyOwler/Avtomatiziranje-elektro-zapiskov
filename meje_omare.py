from openpyxl import load_workbook

RDECA = "FF0000"
ORANZNA = "FFA500"
MODRA = "99FFFF"


def preveri_meje_omare(seznam):
    # funkcija prejme seznam s 3 elementi (pot je 4), ter binarno vrendost trafo

    slovar_problematicnih_meritev = dict()

    if seznam[1] == "X":
        slovar_problematicnih_meritev[1] = MODRA
    else:
        if float(seznam[1].replace(">", "").replace(",", ".")) > 1 and 10 > float(
            seznam[1].replace(">", "").replace(",", ".")
        ):
            slovar_problematicnih_meritev[1] = ORANZNA
        elif float(seznam[1].replace(">", "").replace(",", ".")) >= 10:
            slovar_problematicnih_meritev[1] = RDECA

    return slovar_problematicnih_meritev
