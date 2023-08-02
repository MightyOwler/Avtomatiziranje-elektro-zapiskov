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


def preveri_meje_R_ISO(seznam, meja_izolacijske_upornosti_stroji_riso_oranzna=100):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo

    slovar_problematicnih_meritev = dict()

    if seznam[3] == "X":
        slovar_problematicnih_meritev[3] = MODRA
    else:
        if (
            float(seznam[3].replace(">", "").replace(",", ".").replace(" MΩ", ""))
            <= meja_izolacijske_upornosti_stroji_riso_oranzna
        ):
            slovar_problematicnih_meritev[3] = ORANZNA

        if seznam[4] == "✗":
            slovar_problematicnih_meritev[3] = RDECA

    return slovar_problematicnih_meritev


def preveri_meje_ZLOOP(seznam):
    # funkcija prejme seznam z 12 elementi

    slovar_problematicnih_meritev = dict()

    Ipsc_meja = (
        "X" if seznam[4] == "X" else float(seznam[4].replace(",", ".").replace(">", ""))
    )
    z_meja = (
        "X"
        if seznam[10] == "X"
        else float(seznam[10].replace(",", ".").replace(">", ""))
    )
    Ipsc = (
        "X"
        if seznam[6] == "X"
        else float(seznam[6].split("/")[0].replace(",", ".").replace(">", ""))
    )
    Z = (
        "X"
        if seznam[6] == "X"
        else float(seznam[6].split("/")[1].replace(",", ".").replace(">", ""))
    )

    if Z == "X" or z_meja == "X":
        slovar_problematicnih_meritev[6] = MODRA
    elif z_meja / 1000 < Z and (z_meja + 25) / 1000 > Z:
        slovar_problematicnih_meritev[6] = ORANZNA

    if Ipsc == "X" or Ipsc_meja == "X":
        slovar_problematicnih_meritev[6] = MODRA
    elif Ipsc_meja < Ipsc and (Ipsc_meja + 25) > Z:
        slovar_problematicnih_meritev[6] = ORANZNA

    if seznam[7] == "✗":
        slovar_problematicnih_meritev[6] = RDECA

    return slovar_problematicnih_meritev


def preveri_meje_NEPREKINJENOST(seznam):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo

    slovar_problematicnih_meritev = dict()

    if seznam[5] == "✗":
        slovar_problematicnih_meritev[3] = RDECA

    return slovar_problematicnih_meritev
