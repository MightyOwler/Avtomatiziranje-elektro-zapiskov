from openpyxl import load_workbook

rdeca = "FF0000"
oranzna = "FFA500"
modra = "99FFFF"

def preberi_float_z_mesta_v_seznamu(seznam, mesto, pomozno_mesto = None):
    if pomozno_mesto:
        return float(seznam[mesto].split("/")[pomozno_mesto].replace(",",".")) if seznam[mesto].split("/")[pomozno_mesto] != "X" else "X"
    else:
        return float(seznam[mesto].replace(",",".")) if seznam[mesto] != "X" else "X"

def preveri_meje_osnovne(seznam, trafo = True):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo
    
    slovar_problematicnih_meritev = dict()
    
    # faktorja, ki določata občutljivost oranžne barve
    faktor_za_oranzno_barvo_tok = 1.5     #1.5 pomeni, da je barva oranžna v primeru, ko je rezultat manjši od 1.5-kratnika najnižje dovoljene meje
    faktor_za_oranzno_barvo_upornost = 0.7    #0.7 pomeni, da je barva oranžna v primeru, ko je rezultat večji od 0.7-kratnika najvišje dovoljene meje
    
    tip_varovalke = seznam[8]
    i_varovalke = preberi_float_z_mesta_v_seznamu(seznam, 9)
    t_varovalke = preberi_float_z_mesta_v_seznamu(seznam, 10)
    
    pot = seznam[25]
    
    # Če je luč, obravnavamo mejo drugače
    if "lamp" in pot or "Lamp" in pot:
        meja_du = 0.05 if trafo else 0.03
    else:
        meja_du = 0.07 if trafo else 0.05

    ik1 = preberi_float_z_mesta_v_seznamu(seznam, 11, pomozno_mesto=1)
    ik2 = preberi_float_z_mesta_v_seznamu(seznam, 12, pomozno_mesto=1)
    zs = preberi_float_z_mesta_v_seznamu(seznam, 11, pomozno_mesto=0)
    zl = preberi_float_z_mesta_v_seznamu(seznam, 11, pomozno_mesto= 0)
    du = preberi_float_z_mesta_v_seznamu(seznam, 12, pomozno_mesto= 2)
    if type(du) == float:
        du /= 100
    
    rlow = seznam[5]
    riso = seznam[7]
    
    if rlow != "X":
        if ">" in rlow:
            slovar_problematicnih_meritev[5] = rdeca
        else:
            # meja_rlow = 1
            rlow = float(rlow.replace(",","."))
            if rlow > 1:
                slovar_problematicnih_meritev[5] = rdeca
            elif rlow > 0.8: 
                slovar_problematicnih_meritev[5] = oranzna
            
    elif riso != "X":
        if not ">" in riso:
            # meja_riso = 1
            riso = float(riso.replace(",","."))
            if riso < 1:
                slovar_problematicnih_meritev[7] = rdeca
            elif riso < 2: 
                slovar_problematicnih_meritev[7] = oranzna

    excel_delovna_datoteka = load_workbook("Meje za meritve.xlsx", data_only=True)

    # Označimo z rdečo neobstoječe čase varovalk
    
    t_varovalke_je_ustrezen = False
    for vrednost in [0.1, 0.2, 0.4, 5.0]:
        if t_varovalke == vrednost:
            t_varovalke_je_ustrezen = True
            break
    
    if not t_varovalke_je_ustrezen:
        slovar_problematicnih_meritev[10] = rdeca
        stolpec = 1

    if tip_varovalke in ["gG", "NV", "gL"]:
        excel_delovni_list = excel_delovna_datoteka["gG"]
        prva_vrstica = 6
        zadnja_vrstica = 34
        
        slovar_t_varovalk_in_stolpcev = {0.1: 1, 0.2: 4, 0.4:7, 5.0:10}
        
        if t_varovalke == 0.1:
            zadnja_vrstica = 30
        
        stolpec = slovar_problematicnih_meritev.get(t_varovalke, 0)
        
        stolpec1 = [excel_delovni_list.cell(row=i,column=stolpec).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec2 = [excel_delovni_list.cell(row=i,column=stolpec + 1).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec3 = [excel_delovni_list.cell(row=i,column=stolpec + 2).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        
        if i_varovalke not in stolpec1:
            indeks_ujemajoce_varovalke = 0
            slovar_problematicnih_meritev[9] = rdeca
        else:
            indeks_ujemajoce_varovalke = stolpec1.index(i_varovalke)            
        
    if tip_varovalke in ["B","D","C"]:
        excel_delovni_list = excel_delovna_datoteka["BCD"]
        
        prva_vrstica = 6
        zadnja_vrstica = 17
        
        slovar_tipov_varovalk_in_stolpcev = {"B": 2, "C": 4, "D": 6}
        stolpec = slovar_tipov_varovalk_in_stolpcev[tip_varovalke]

        stolpec1 = [excel_delovni_list.cell(row=i,column=1).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec2 = [excel_delovni_list.cell(row=i,column=stolpec).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec3 = [excel_delovni_list.cell(row=i,column=stolpec + 1).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        
        if i_varovalke not in stolpec1:
            indeks_ujemajoce_varovalke = 0
            slovar_problematicnih_meritev[9] = rdeca
        else:
            indeks_ujemajoce_varovalke = stolpec1.index(i_varovalke)
        
    if ik1 == "X":
        slovar_problematicnih_meritev[11] = modra
    elif ik2 == "X":
        slovar_problematicnih_meritev[12] = modra
    elif t_varovalke_je_ustrezen:
        if ik1 < stolpec2[indeks_ujemajoce_varovalke]: 
            slovar_problematicnih_meritev[11] = rdeca
        elif ik1 <= stolpec2[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_tok: 
            slovar_problematicnih_meritev[11] = oranzna
        
        if ik2 < stolpec2[indeks_ujemajoce_varovalke]:
            slovar_problematicnih_meritev[12] = rdeca
        elif ik2 == stolpec2[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_tok:
            slovar_problematicnih_meritev[12] = oranzna
    
    if zs == "X":
        slovar_problematicnih_meritev[11] = modra
    elif zl == "X":
        slovar_problematicnih_meritev[12] = modra
    elif du == "X":
        slovar_problematicnih_meritev[12] = modra
    elif t_varovalke_je_ustrezen:
        if zl > stolpec3[indeks_ujemajoce_varovalke]:
            slovar_problematicnih_meritev[12] = rdeca
        elif zl >= stolpec3[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_upornost:
            if slovar_problematicnih_meritev.get(12, "") != rdeca:
                slovar_problematicnih_meritev[12] = oranzna   
            
            
        if zs > stolpec3[indeks_ujemajoce_varovalke]:
            slovar_problematicnih_meritev[11] = rdeca
        elif zs >= stolpec3[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_upornost:
            if slovar_problematicnih_meritev.get(11, "") != rdeca:
                slovar_problematicnih_meritev[11] = oranzna
            
        if du > meja_du:
            slovar_problematicnih_meritev[12] = rdeca
        elif du >= meja_du * faktor_za_oranzno_barvo_upornost:
            if slovar_problematicnih_meritev.get(12, "") != rdeca:
                slovar_problematicnih_meritev[12] = oranzna
    
    return slovar_problematicnih_meritev

def preveri_meje_RLOW4(seznam, trafo = True):
    
    slovar_problematicnih_meritev = dict()
    r = seznam[1].replace(",",".")
    
    if r != "":
        if ">" in r:
            slovar_problematicnih_meritev[1] = rdeca
        else:
            r = float(r) if r != "X" else "X"
            
            if r == "X":
                slovar_problematicnih_meritev[1] = modra
            elif r > 1:
                slovar_problematicnih_meritev[1] = rdeca
            elif r > 0.8: 
                slovar_problematicnih_meritev[1] = oranzna
            
    return slovar_problematicnih_meritev