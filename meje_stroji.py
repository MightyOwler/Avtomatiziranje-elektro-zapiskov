from openpyxl import load_workbook

RDECA = "FF0000"
ORANZNA = "FFA500"
MODRA = "99FFFF"


def preberi_float_z_mesta_v_seznamu(seznam, mesto, pomozno_mesto=None):
    if pomozno_mesto is not None:
        return (
            float(seznam[mesto].split("/")[pomozno_mesto].replace(",", "."))
            if seznam[mesto].split("/")[pomozno_mesto] != "X"
            else "X"
        )
    else:
        return float(seznam[mesto].replace(",", ".")) if seznam[mesto] != "X" else "X"


def preveri_meje_R_ISO(seznam):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo

    slovar_problematicnih_meritev = dict()

    return slovar_problematicnih_meritev


def preveri_meje_ZLOOP(seznam):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo

    slovar_problematicnih_meritev = dict()

    return slovar_problematicnih_meritev


def preveri_meje_NEPREKINJENOST(seznam):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo

    slovar_problematicnih_meritev = dict()

    if seznam[5] == "✗":
        slovar_problematicnih_meritev[3] = RDECA

    return slovar_problematicnih_meritev
