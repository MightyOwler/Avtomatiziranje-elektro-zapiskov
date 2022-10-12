from openpyxl import load_workbook

def preveri_meje_osnovne(seznam, trafo = True):
    # funkcija prejme seznam s 25 elementi, ter binarno vrendost trafo
    
    slovar_problematicnih_meritev = dict()
    
    # faktorja, ki določata občutljivost oranžne barve
    faktor_za_oranzno_barvo_tok = 1.5     #1.5 pomeni, da je barva oranžna v primeru, ko je rezultat manjši od 1.5-kratnika najnižje dovoljene meje
    faktor_za_oranzno_barvo_upornost = 0.7    #0.7 pomeni, da je barva oranžna v primeru, ko je rezultat večji od 0.7-kratnika najvišje dovoljene meje
    
    tip_varovalke = seznam[8]
    i_varovalke = float(seznam[9].replace(",","."))
    t_varovalke = float(seznam[10].replace(",","."))
    
    pot = seznam[25]
    if "lamp" in pot or "Lamp" in pot:
        # luc = True
        if trafo:
            meja_du = 0.05
        else:
            meja_du = 0.03
    else:
        if trafo:
            meja_du = 0.07
        else:
            meja_du = 0.05
        

    # tale koda je problematična (zaenkrat ne več, ker sva popravila)
    
    ik1 = float(seznam[11].split("/")[1].replace(",",".")) if seznam[11].split("/")[1] != "X" else "X"
    ik2 = float(seznam[12].split("/")[1].replace(",",".")) if seznam[12].split("/")[1] != "X" else "X"
    zs = float(seznam[11].split("/")[0].replace(",",".")) if seznam[11].split("/")[0] != "X" else "X"
    zl = float(seznam[12].split("/")[0].replace(",",".")) if seznam[12].split("/")[0] != "X" else "X"
    du = float(seznam[12].split("/")[2].replace(",",".")) / 100 if seznam[12].split("/")[2] != "X" else "X" 
    
    rlow = seznam[5]
    riso = seznam[7]
    
    if rlow != "X":
        if ">" in rlow:
            slovar_problematicnih_meritev[5] = "FF0000"
        else:
            # meja_rlow = 1
            rlow = float(rlow.replace(",","."))
            if rlow > 1:
                slovar_problematicnih_meritev[5] = "FF0000"
            elif rlow > 0.8: 
                slovar_problematicnih_meritev[5] = "FFA500"
            
    elif riso != "X":
        if not ">" in riso:
            # meja_riso = 1
            riso = float(riso.replace(",","."))
            if riso < 1:
                slovar_problematicnih_meritev[7] = "FF0000"
            elif riso < 2: 
                slovar_problematicnih_meritev[7] = "FFA500"

    excel_delovna_datoteka = load_workbook("Meje za meritve.xlsx", data_only=True)

    """
    NUJNO: narediti še za NV meritve, saj so nekoliko drugačne od ostalih
    """
    
    if tip_varovalke in ["gG", "NV", "gL"]:
        excel_delovni_list = excel_delovna_datoteka["gG"]
        prva_vrstica = 6
        zadnja_vrstica = 34
        
        if t_varovalke == 0.1:
            stolpec = 1
            zadnja_vrstica = 30
        if t_varovalke == 0.2:
            stolpec = 4
        if t_varovalke == 0.4:
            stolpec = 7 
        if t_varovalke == 5.0:
            stolpec = 10
            
        stolpec1 = [excel_delovni_list.cell(row=i,column=stolpec).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec2 = [excel_delovni_list.cell(row=i,column=stolpec + 1).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec3 = [excel_delovni_list.cell(row=i,column=stolpec + 2).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        
        if i_varovalke not in stolpec1:
            indeks_ujemajoce_varovalke = 0
            slovar_problematicnih_meritev[9] = "FF0000"
        else:
            indeks_ujemajoce_varovalke = stolpec1.index(i_varovalke)            
        
    if tip_varovalke in ["B","D","C"]:
        pass
    
        """
        Tukaj morava dodati meje ta meritve oblike C
        """
        
        excel_delovni_list = excel_delovna_datoteka["BCD"]
        
        prva_vrstica = 6
        zadnja_vrstica = 17
        
        if tip_varovalke == "B":
            stolpec = 2
        if tip_varovalke == "C":
            stolpec = 4
        if tip_varovalke == "D":
            stolpec = 6

        stolpec1 = [excel_delovni_list.cell(row=i,column=1).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec2 = [excel_delovni_list.cell(row=i,column=stolpec).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        stolpec3 = [excel_delovni_list.cell(row=i,column=stolpec + 1).value for i in range(prva_vrstica, zadnja_vrstica + 1)]
        
        if i_varovalke not in stolpec1:
            indeks_ujemajoce_varovalke = 0
            slovar_problematicnih_meritev[9] = "FF0000"
        else:
            indeks_ujemajoce_varovalke = stolpec1.index(i_varovalke)
        
    if ik1 == "X":
        slovar_problematicnih_meritev[11] = "99FFFF"
    elif ik2 == "X":
        slovar_problematicnih_meritev[12] = "99FFFF"
    else:
        if ik1 < stolpec2[indeks_ujemajoce_varovalke]: 
            slovar_problematicnih_meritev[11] = "FF0000"
        elif ik1 <= stolpec2[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_tok: 
            slovar_problematicnih_meritev[11] = "FFA500"
        
        if ik2 < stolpec2[indeks_ujemajoce_varovalke]:
            slovar_problematicnih_meritev[12] = "FF0000"
        elif ik2 == stolpec2[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_tok:
            slovar_problematicnih_meritev[12] = "FFA500"
    
    if zs == "X":
        slovar_problematicnih_meritev[11] = "99FFFF"
    elif zl == "X":
        slovar_problematicnih_meritev[12] = "99FFFF"
    elif du == "X":
        slovar_problematicnih_meritev[12] = "99FFFF"
    else:
        if zl > stolpec3[indeks_ujemajoce_varovalke]:
            slovar_problematicnih_meritev[12] = "FF0000"
        elif zl >= stolpec3[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_upornost:
            if slovar_problematicnih_meritev.get(12, "") != "FF0000":
                slovar_problematicnih_meritev[12] = "FFA500"   
            
            
        if zs > stolpec3[indeks_ujemajoce_varovalke]:
            slovar_problematicnih_meritev[11] = "FF0000"
        elif zs >= stolpec3[indeks_ujemajoce_varovalke] * faktor_za_oranzno_barvo_upornost:
            if slovar_problematicnih_meritev.get(11, "") != "FF0000":
                slovar_problematicnih_meritev[11] = "FFA500"
            
        if du > meja_du:
            slovar_problematicnih_meritev[12] = "FF0000"
        elif du >= meja_du * faktor_za_oranzno_barvo_upornost:
            if slovar_problematicnih_meritev.get(12, "") != "FF0000":
                slovar_problematicnih_meritev[12] = "FFA500"
    
    return slovar_problematicnih_meritev

def preveri_meje_RLOW4(seznam, trafo = True):
    
    slovar_problematicnih_meritev = dict()
    r = seznam[1].replace(",",".")
    
    if r != "":
        if ">" in r:
            slovar_problematicnih_meritev[1] = "FF0000"
        else:
            r = float(r) if r != "X" else "X"
            meja_rlow = 1
            
            if r == "X":
                slovar_problematicnih_meritev[1] = "99FFFF"
            elif r > 1:
                slovar_problematicnih_meritev[1] = "FF0000"
            elif r > 0.8: 
                slovar_problematicnih_meritev[1] = "FFA500"
            
    return slovar_problematicnih_meritev