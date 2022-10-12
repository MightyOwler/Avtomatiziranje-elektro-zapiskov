import re
from datetime import datetime
import csv
from Meritev import Meritev, pretvori_v_osnovne_enote
from meje import *

# R low je kvečjem 1 na kocko, se vpiše po celotni vrstici

seznam_vrst_meritev = ["AUTO TN", "Zloop", "Z LINE",
                       "RCD Auto", "R low 4", "Varistor", "R iso", "Padec napetosti", "R IZO", "ZLOOP 4W", "ZLINE 4W"]
seznam_enot_za_pretvorbe = ["V", "A", "Ω", "s"]
seznam_predpon_za_pretvorbe = ["m", "k"]

st_vnesenih_meritev = 0
st_vnesenih_meritev_RCD = 0

def pretvori_string_milisekund_v_ustrezen_format(string):
    # tole je pomembno, če hočemo string pretvoriti v float
    return string.replace(",", ".").replace(" ms", "").replace(">", "")

def velikost_stringa(s):
    """
    Funkcija, ki nam omogoča da razvrstimo meritve po velikosti kljub znaku > (to je konkretno pomembno pri RISO in RLOW4)
    """
    if ">" in s:
        return 1000000000000
    else:
        return pretvori_v_osnovne_enote(s.replace(",","."))


def zapisi_kocko_meritev_v_excel(kocka, loceno_besedilo, slovar_kock_in_ustreznih_poti):
    """
    Zapiše meritev v csv datoteko, ki je primerna za obdelavo v csv-ju

    Args: kocka, loceno_besedilo, slovar_kock_in_ustreznih_poti
    """
    
    global st_vnesenih_meritev
    global st_vnesenih_meritev_RCD
    
    prazno = " "
    uln, zln, ipsc_ln, ipsc_lpe = "X", "X", "X", "X"
    rlpe, dU, zlpe, glavna_izenac_povezava = "X", "X", "X", "X"
    ia_psc_navidezni_stolpec, maxRplusRminus, tip_varovalke = "X", "X", "X"
    I_varovalke, t_varovalke, isc_faktor = "X", "X", "X"
    I_dN, t1x, t5x, Uc,  = "X", "X", "X", "X"
    komentar = ""
    ime = "X"
    pot = slovar_kock_in_ustreznih_poti[loceno_besedilo.index(
        kocka)].replace("\n", " ").strip()
    pot_locena_na_elemente = pot.replace("\n", " ").strip().split("//")

    # Ta spodnja kocka zahteva, da se v vsaki poti Dist. Board pojavi natanko 2x !!
    # Program ne določi sekcije tukaj, ampak v branje_podatkov.py. Zato sem izbrisal spremenljivko sekcija
    
    stevec_dist_board = 0
    for element in pot_locena_na_elemente:
        if "Imenovanje: " in element.strip():
            ime = element.replace("Imenovanje: ", "")
            if "Circuit F" in ime:
                ime = ime.replace("Circuit ", "")
            elif re.search("Circuit\d", ime):
                ime = ime.replace("Circuit", "F")
            
        # To je stara verzija, kjer se določa stvari glede na Dist. Board
            
        # elif "Dist. Board" in element.strip() and "Dist. Board DOVOD" not in element.strip() and "Dist. Board OBREMENILNI PREIZKUS" not in element.strip():
        #     if stevec_dist_board == 1:
        #         ime = element.replace("Dist. Board ", "")
        #         if "Circuit F" in ime:
        #             ime = ime.replace("Circuit ", "")
        #         elif re.search("Circuit\d", ime):
        #             ime = ime.replace("Circuit", "F")
        #     stevec_dist_board += 1
                
        # if stevec_dist_board != 2:
        #     print(f"Napaka: V poti **{pot}** se 'Dist. Board (brez DOVOD)' ne pojavi dvakrat, ampak {stevec_dist_board}-krat!")          
    
    
    if not ime:
        ime = "X"
        
    # Za vsak slučaj preverimo, ali pot ne obstaja
    if pot is None:
        pot = "X"
        print("Napaka: Ni poti v slovarju poti", slovar_kock_in_ustreznih_poti)

    vrste_meritev_v_kocki = [meritev.doloci_vrsto_meritve()
                             for meritev in kocka]
    slovar_vrst_meritev = {i: vrste_meritev_v_kocki.count(
        i) for i in seznam_vrst_meritev}

    
    # tale spodnja kocka kode je zaenkrat še ne testirana, oziroma je možno, da bi se nahajal kak bug!!
    # znal bi biti kak problem z zapisovanjem ali kaj podobnega
    if slovar_vrst_meritev["R iso"]  + slovar_vrst_meritev["R IZO"] > 1:
        nova_kocka = []
        seznam_riso_meritev = []
        for meritev in kocka:
            if meritev.doloci_vrsto_meritve() in ["R iso", "R IZO"]:
                # inšturment vedno izpiše v MΩ
                seznam_riso_meritev.append(meritev.najdi_Rlpe().replace(" MΩ", "").replace(",","."))
        seznam_riso_meritev.sort(key = lambda x: velikost_stringa(x))
        riso_meritev_z_minimalno = seznam_riso_meritev[0]
        for idx, meritev in enumerate(kocka):
            if meritev.doloci_vrsto_meritve() in ["R iso", "R IZO"]:
                if idx == seznam_riso_meritev.index(riso_meritev_z_minimalno):
                    nova_kocka.append(meritev)            
            else:
                nova_kocka.append(meritev)
                
        # na tej točki se je treba vprašati, ali je res smiselno ustvariti novo kocko (izbirsati nekatere RISO meritve)
        kocka = nova_kocka

    
    if slovar_vrst_meritev["R low 4"] > 0:
        with open("Csvji//csv_za_excel_datoteko_RLOW4.csv", "a", encoding='utf-8', newline='') as csvfile:

            writer = csv.writer(csvfile, delimiter=';',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
            seznam_rlow4_meritev = []
            
            for meritev in kocka:                
                if meritev.doloci_vrsto_meritve() == "R low 4":
                    seznam_rlow4_meritev.append(meritev.najdi_R())
                    if ">1999" in meritev.najdi_R_pozitivno() or ">1999" in meritev.najdi_R_negativno():
                        maxRplusRminus = ">1999"
                    else:
                        R_pozitivno_int = meritev.najdi_R_pozitivno().replace(
                            ",", ".").replace(" Ω", "").replace(">", "")
                        if R_pozitivno_int != "X":
                            R_pozitivno_int = float(R_pozitivno_int)
                            
                        R_negativno_int = meritev.najdi_R_negativno().replace(
                            ",", ".").replace(" Ω", "").replace(">", "")
                        if R_negativno_int != "X":
                            R_negativno_int = float(R_negativno_int)
                            
                        # Pri kateri velikosti spremenimo v int?
                        if R_negativno_int == "X" or R_pozitivno_int == "X":
                            maxRplusRminus = "X"
                        else:
                            if max(R_negativno_int, R_pozitivno_int) >= 100:
                                maxRplusRminus = f"{int(max(R_negativno_int, R_pozitivno_int))}"
                            else:
                                maxRplusRminus = f"{max(R_negativno_int, R_pozitivno_int)}"
                    R = meritev.najdi_R()
                    vrsta_meritve = meritev.doloci_vrsto_meritve()
                    array_ki_ga_zapisemo_v_csv = [ime, R, maxRplusRminus, komentar, vrsta_meritve, pot]
                    writer.writerow(array_ki_ga_zapisemo_v_csv)
            csvfile.close()
            seznam_rlow4_meritev.sort(key = lambda x: float(velikost_stringa(x)))
            rlow4_meritev_z_minimalno = seznam_rlow4_meritev[0]
        
        if slovar_vrst_meritev["RCD Auto"] > 1:
            print("Napaka: Imamo 2 ali več RCD Auto meritvi v eni kocki!")
        
        for idx, vrednost_meritve in enumerate(seznam_rlow4_meritev):
            if idx == seznam_rlow4_meritev.index(rlow4_meritev_z_minimalno):
                # glavno izenačitveno povezavo potrebujemo samo pri eni meritvi
                glavna_izenac_povezava = vrednost_meritve
                break
    
    
    for meritev in kocka:
        vrsta_meritve = meritev.doloci_vrsto_meritve()

        if vrsta_meritve == "R iso":
            rlpe = meritev.najdi_Rlpe().replace(" MΩ", "")
                
        if vrsta_meritve == "Padec napetosti":
            dU = meritev.najdi_dU()
            
        if vrsta_meritve == "RCD Auto":
            Uc = meritev.najdi_Uc()
            I_dN = meritev.najdi_I_dN()
            t1x_plus = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x1_plus())
            t1x_neg = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x1_minus())
            t5x_plus = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x5_plus())
            t5x_neg = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x5_minus())

            # V primeru, da vse količine obstajajo
            if t1x_plus != "X" and t1x_neg != "X" and t5x_plus != "X" and t1x_neg != "X":
                t1x_plus = float(t1x_plus)
                t1x_neg = float(t1x_neg)
                t5x_plus = float(t5x_plus)
                t5x_neg = float(t5x_neg)

                # Pri kateri velikosti spremenimo v int? Ideja je okoli 100
                if max(t1x_plus, t1x_neg) >= 100:
                    t1x = f"{int(max(t1x_plus, t1x_neg))}".replace(
                        ".", ",")
                else:
                    t1x = f"{max(t1x_plus, t1x_neg)}".replace(".", ",")

                # Pri kateri velikosti spremenimo v int?
                if max(t5x_plus, t5x_neg) >= 100:
                    t5x = f"{int(max(t5x_plus, t5x_neg))}".replace(".", ",")
                else:
                    t5x = f"{max(t5x_plus, t5x_neg)}".replace(".", ",")
            else:
                t1x = "X"
                t5x = "X"
        
        if vrsta_meritve == "Varistor":
            with open("Csvji//csv_za_excel_datoteko_VARISTOR.csv", "a", encoding='utf-8', newline='') as csvfile:

                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                uac = meritev.najdi_Uac()
                udc = meritev.najdi_Udc()
                
                """
                Aljaž: uredi izpisovanje za varistor!
                """
                
                array_ki_ga_zapisemo_v_csv = [ime, uac, udc, komentar, vrsta_meritve, pot]
                writer.writerow(array_ki_ga_zapisemo_v_csv)
                csvfile.close()

    
    # Stvar je treba narediti v večih korakih, saj lahko podatki v posamezni meritvi vplivajo na celotno kocko ali kasnejše.
    # najprej odpravimo AUTO TN

    for meritev in kocka:
        vrsta_meritve = meritev.doloci_vrsto_meritve()
        
        if vrsta_meritve == "AUTO TN":
            with open("Csvji//csv_za_excel_datoteko_osnovne.csv", "a", encoding='utf-8', newline='') as csvfile:
                
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)

                uln = meritev.najdi_Uln()
                zln = meritev.najdi_Z_LN()
                ipsc_ln = meritev.najdi_Ipsc_LN()
                ipsc_lpe = meritev.najdi_Ipsc_LPE()
                dU = meritev.najdi_dU()
                zlpe = meritev.najdi_Z_LPE()
                ia_psc_navidezni_stolpec = meritev.najdi_Ia_Ipsc()
                tip_varovalke = meritev.najdi_tip_varovalke()
                I_varovalke = meritev.najdi_I_varovalke()
                t_varovalke = meritev.najdi_t_varovalke()
                isc_faktor = meritev.najdi_Isc_faktor()
                komentar = meritev.najdi_komentar()
                
                st_vnesenih_meritev += 1
                array_ki_ga_zapisemo_v_csv = [st_vnesenih_meritev, ime, prazno, prazno, prazno, glavna_izenac_povezava, prazno, rlpe, tip_varovalke, I_varovalke, t_varovalke, f"{zlpe}/{ipsc_ln}", f"{zln}/{ipsc_lpe}/{dU}", 
                                                prazno,  I_dN, prazno, t1x, t5x, Uc, prazno, komentar, vrsta_meritve, uln, maxRplusRminus, isc_faktor, ia_psc_navidezni_stolpec, pot]
                writer.writerow(array_ki_ga_zapisemo_v_csv)
                csvfile.close()

    # nato odpravimo Zloop / Zine

    if "Zloop" in vrste_meritev_v_kocki or "Z LINE" in vrste_meritev_v_kocki:
        ustrezni_zline_3 = []
        ustrezni_zloop_3 = []
        for meritev in kocka:
            vrsta_meritve = meritev.doloci_vrsto_meritve()
            if vrsta_meritve == "Zloop":
                ustrezni_zloop_3.append(meritev)
            if vrsta_meritve == "Z LINE":
                if "400" == meritev.najdi_Un():
                    ustrezni_zline_3.append(meritev)

        # Safety check v primeru, da ni treh zloop/zline elementov
        if len(ustrezni_zline_3) != len(ustrezni_zloop_3) or len(ustrezni_zline_3) != 3 or len(ustrezni_zloop_3) != 3:
            print("\nNapaka: Nekaj ni v redu s številom zloop/zlinov")
            print("Pot problematične meritve:", pot.strip())
            print("Dolžina zloop", len(ustrezni_zloop_3))
            print("Dolžina zline", len(ustrezni_zline_3))

        else:
            for i in range(3):
                with open("Csvji//csv_za_excel_datoteko_osnovne.csv", "a", encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(
                        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    if ustrezni_zline_3[i].besedilo.count("p//") > 0:
                        ipsc_zline, z_zline = "X", "X"
                    else:
                        ipsc_zline = ustrezni_zline_3[i].najdi_Ipsc()
                        z_zline = ustrezni_zline_3[i].najdi_Z()
                    
                    if ustrezni_zloop_3[i].besedilo.count("p//") > 0:
                        ipsc_zloop, z_zloop = "X", "X"
                    else:
                        ipsc_zloop = ustrezni_zloop_3[i].najdi_Ipsc()
                        z_zloop = ustrezni_zloop_3[i].najdi_Z()

                    if ustrezni_zloop_3[i].besedilo.count("p//") > 0:
                        uln, ipsc_lpe, zlpe, ia_psc_navidezni_stolpec, tip_varovalke, I_varovalke, t_varovalke, isc_faktor, komentar = "X", "X", "X", "X", "X", "X", "X", "X", "X"
                    else:
                        uln = ustrezni_zloop_3[i].najdi_Uln()
                        ipsc_lpe = ustrezni_zloop_3[i].najdi_Ipsc_LPE()
                        zlpe = ustrezni_zloop_3[i].najdi_Z_LPE()
                        ia_psc_navidezni_stolpec = ustrezni_zloop_3[i].najdi_Ia_Ipsc(
                        )
                        tip_varovalke = ustrezni_zloop_3[i].najdi_tip_varovalke(
                        )
                        I_varovalke = ustrezni_zloop_3[i].najdi_I_varovalke()
                        t_varovalke = ustrezni_zloop_3[i].najdi_t_varovalke()
                        isc_faktor = ustrezni_zloop_3[i].najdi_Isc_faktor()
                        vrsta_meritve = "ZLOOP / ZLINE"
                        komentar = ustrezni_zloop_3[i].najdi_komentar()
                        
                        if not dU:
                            dU = "X"
                        
                        st_vnesenih_meritev += 1
                        array_ki_ga_zapisemo_v_csv = [st_vnesenih_meritev, ime, prazno, prazno, prazno, glavna_izenac_povezava, prazno, rlpe, tip_varovalke, I_varovalke, t_varovalke, f"{z_zloop}/{ipsc_zloop}", f"{z_zline}/{ipsc_zline}/{dU}",
                                                     prazno, I_dN, prazno, t1x, t5x, Uc, prazno, komentar, vrsta_meritve, uln, maxRplusRminus, isc_faktor, ia_psc_navidezni_stolpec, pot]
                        writer.writerow(array_ki_ga_zapisemo_v_csv)
                        csvfile.close()

    # nato odpravimo RCD AUTO

    for meritev in kocka:
        vrsta_meritve = meritev.doloci_vrsto_meritve()
        if vrsta_meritve == "RCD Auto":
            with open("Csvji//csv_za_excel_datoteko_RCD.csv", "a", encoding='utf-8', newline='') as csvfile_RCD:
                writer = csv.writer(csvfile_RCD, delimiter=';',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                I_dN = meritev.najdi_I_dN()
                tip_rcd = meritev.najdi_Tip()
                Uc = meritev.najdi_Uc()
                ozemljitveni_sistem = meritev.najdi_Ozemljitveni_sistem()
                komentar = meritev.najdi_komentar()

                t1x_plus = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x1_plus())
                t1x_neg = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x1_minus())
                t5x_plus = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x5_plus())
                t5x_neg = pretvori_string_milisekund_v_ustrezen_format(meritev.najdi_t_IΔN_x5_minus())

                # V primeru, da vse količine obstajajo
                if t1x_plus != "X" and t1x_neg != "X" and t5x_plus != "X" and t1x_neg != "X":

                    t1x_plus = float(t1x_plus)
                    t1x_neg = float(t1x_neg)
                    t5x_plus = float(t5x_plus)
                    t5x_neg = float(t5x_neg)

                    # Pri kateri velikosti spremenimo v int?
                    if max(t1x_plus, t1x_neg) >= 100:
                        t1x = f"{int(max(t1x_plus, t1x_neg))}".replace(
                            ".", ",")
                    else:
                        t1x = f"{max(t1x_plus, t1x_neg)}".replace(".", ",")

                    if max(t5x_plus, t5x_neg) >= 100:
                        t5x = f"{int(max(t5x_plus, t5x_neg))}".replace(
                            ".", ",")
                    else:
                        t5x = f"{max(t5x_plus, t5x_neg)}".replace(".", ",")
                else:
                    print("\nNapaka: manjkajoči podatki t1x ali t5x pri", pot.strip())
                    t1x = "X"
                    t5x = "X"
                
                st_vnesenih_meritev_RCD += 1
                array_ki_ga_zapisemo_v_csv = [st_vnesenih_meritev_RCD, ime, prazno, prazno, I_dN, tip_rcd, prazno, prazno, prazno,  
                                              prazno, Uc, prazno, t1x, t5x, ozemljitveni_sistem, komentar, vrsta_meritve, pot]
                writer.writerow(array_ki_ga_zapisemo_v_csv)
                csvfile_RCD.close()

def najdi_po_vrsti_urejen_seznam_datumov(vse_besedilo):
    loceno_besedilo_po_presledkih = vse_besedilo.split()
    seznam_stringov_z_datumi = []
    for i in loceno_besedilo_po_presledkih:
        # \d\d\.\d\d\.\d\d\d\d je pravi regex expression za to obliko datuma
        if re.search(r"\d{2}\.\d{2}\.\d{4}", i):
            # vsi datumi so pravilne oblike (zraven so zapisane odvečne ničle), zato je upravičeno tole
            string_datuma = i[9:]
            datum = datetime.strptime(string_datuma, '%d.%m.%Y')
            seznam_stringov_z_datumi.append(datum)
    return [datetime.strftime(datum, '%d.%m.%Y') for datum in sorted(seznam_stringov_z_datumi)]


def najdi_pot_izven_razreda_Meritev(besedilo):
    idx = besedilo.find("Pot:")
    string_ki_ga_obdelujemo = besedilo[idx:]
    if "Page" in string_ki_ga_obdelujemo:
        idx = string_ki_ga_obdelujemo.find("Page")
        # poanta je v temu, da so spredaj odvečne črke
        string_ki_ga_obdelujemo = string_ki_ga_obdelujemo[:idx]
    if "Serijsko" in string_ki_ga_obdelujemo:
        idx = string_ki_ga_obdelujemo.find("Serijsko")
        string_ki_ga_obdelujemo = string_ki_ga_obdelujemo[:idx]
    return string_ki_ga_obdelujemo