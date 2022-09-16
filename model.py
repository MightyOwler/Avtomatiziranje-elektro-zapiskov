import re
from datetime import datetime
import csv

# R low je kvečem 1 na kocko, se vpiše po celotni vrstici

seznam_vrst_meritev = ["AUTO TN", "Zloop", "Z LINE", "RCD Auto", "R low 4", "Varistor", "R iso", "Padec napetosti"]
seznam_enot_za_pretvorbe = ["V", "A", "Ω"]
seznam_predpon_za_pretvorbe = ["m","k"]

def pretvori_v_osnovne_enote(besedilo_ki_ga_pretvarjamo):
    """
    Funkcija, ki pretvarja iz mili ali kilo enot v osnovne
    """
    
    for predpona in seznam_predpon_za_pretvorbe:
        for enota in seznam_enot_za_pretvorbe:
            if predpona + enota in besedilo_ki_ga_pretvarjamo:
                besedilo_ki_ga_pretvarjamo = besedilo_ki_ga_pretvarjamo.replace(" " + predpona + enota, "").replace(",", ".")
                besedilo_ki_ga_pretvarjamo = float(besedilo_ki_ga_pretvarjamo)
                if predpona == "m":
                    besedilo_ki_ga_pretvarjamo /= 1000
                    besedilo_ki_ga_pretvarjamo = round(besedilo_ki_ga_pretvarjamo, 3)
                else:
                    besedilo_ki_ga_pretvarjamo *= 1000
                    besedilo_ki_ga_pretvarjamo = round(besedilo_ki_ga_pretvarjamo, 3)
                
                return f"{besedilo_ki_ga_pretvarjamo}".replace(".",",")
    for enota in seznam_enot_za_pretvorbe:
        if enota in besedilo_ki_ga_pretvarjamo:
            return f"{besedilo_ki_ga_pretvarjamo}".replace(" " + enota, "").replace(".",",")
                     
    
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


class Meritev():
    def __init__(self, besedilo_meritve):
        self.besedilo = besedilo_meritve
        self.besedilo_po_elementih = [i.replace("Pot:", "Pot: ").strip() for i in besedilo_meritve.split(", ")]
        
        self.vrsta_meritve = self.doloci_vrsto_meritve
        
    def doloci_vrsto_meritve(self):
        #seznam_vrst = [] ## če bo vse v redu, bi to moralo biti povsod 1
        for vrsta_meritve in seznam_vrst_meritev:
            if vrsta_meritve in self.besedilo:
                #seznam_vrst.append(vrsta_meritve)
                return vrsta_meritve
        #return seznam_vrst
        
    def najdi_komentar(self):
        if "Comment:" in self.besedilo:
            st_pojavitev = self.besedilo.count("Comment:")
            idx_komentarja = find_nth(self.besedilo, "Comment:", st_pojavitev)
            komentar = self.besedilo[idx_komentarja:]
            return komentar.replace("Comment:","").replace("//","").strip()
        else:
            return ""
            
    
    # ta definicija v resnici ni najboljša, saj vedno gleda samo posamezno meritev
    # če nama uspe pravilno razdeliti že prej, potem bo pa ok
    def najdi_element(self, ime_elementa, pretvori_v_osnovne = True):
        element = ""
        for i in self.besedilo_po_elementih:
            if ime_elementa in i:
                element = i[len(ime_elementa) + 1:]
                if pretvori_v_osnovne:
                    return pretvori_v_osnovne_enote(element)
                else:
                    return element
                #Pomembno: treba je preveriti, da program pravilno zaokrožuje stvari!
                #tole obdrži prave enote
                
                
                
        # sicer returna prazno
        return element        

    #spodnji elementi so za meritve, ki se začnejo z AUTO TN
    #to bo treba še bolje definirati
    
    def najdi_pot(self):
        return self.najdi_element('Pot:', pretvori_v_osnovne = False)
        
    def najdi_tip_varovalke(self):
        return self.najdi_element('Tip varov.:', pretvori_v_osnovne = False)
    
    def najdi_I_varovalke(self):
        return self.najdi_element('I varovalke:')
    
    # tukaj je vedno v sekundah?
    def najdi_t_varovalke(self):
        return self.najdi_element('t varovalke:', pretvori_v_osnovne = False)
    
    def najdi_Isc_faktor(self):
        return self.najdi_element('Isc faktor:', pretvori_v_osnovne = False)
    
    def najdi_I_preizkusa(self):
        return self.najdi_element('I preizkusa:')
    
    def najdi_Uln(self):
        return self.najdi_element('Uln:')
    
    def najdi_dU(self):
        return self.najdi_element('dU:')
    
    def najdi_Z_LPE(self):
        return self.najdi_element('Z (LPE):')
    
    def najdi_Z_LN(self):
        return self.najdi_element('Z (LN):')
    
    def najdi_Ipsc_LN(self):
        return self.najdi_element('Ipsc (LN):')
    
    def najdi_Ipsc_LPE(self):
        return self.najdi_element('Ipsc (LPE):')
    
    def najdi_R(self):
        return self.najdi_element('R:')
    
    def najdi_Zref(self):
        return self.najdi_element('Zref:')
    
    def najdi_meja_dU(self):
        return self.najdi_element('Meja(dU):')

    #spodnje meritve so za meritve, ki se začnejo z Zloop in Z LINE
    #to bo treba še bolje definirati

    def najdi_Merilno_breme(self):
        return self.najdi_element('Merilno breme:')

    def najdi_Povprečje(self):
        return self.najdi_element('Povprečje:', pretvori_v_osnovne = False)

    def najdi_Toleranca(self):
        return self.najdi_element('Toleranca:')

    def najdi_Ipsc(self):
        return self.najdi_element('Ipsc:')

    def najdi_Z(self):
        return self.najdi_element('Z:')

    def najdi_XL(self):
        return self.najdi_element('XL:')

    def najdi_IscMax(self):
        return self.najdi_element('IscMax:')

    def najdi_IscMin(self):
        return self.najdi_element('IscMin:')

    def najdi_Ia_Ipsc(self):
        return self.najdi_element('Ia(Ipsc):')
    
    def najdi_Un(self):
        return self.najdi_element('Un:')

    #spodnji elementi so za meritve ki se začnejo z RCD Auto
    #to bo treba še bolje definirati

    def najdi_Uporaba(self):
        return self.najdi_element('Uporaba:', pretvori_v_osnovne = False)

    def najdi_I_dN(self):
        return self.najdi_element('Tip:', pretvori_v_osnovne = False)

    def najdi_Tip(self):
        return self.najdi_element('I dN:')

    def najdi_Preizkus(self):
        return self.najdi_element('Preizkus:')

    def najdi_RCD_standard(self):
        return self.najdi_element('RCD standard:')

    def najdi_Ozemljitveni_sistem(self):
        return self.najdi_element('Ozemljitveni sistem:')

    def najdi_t_IΔN_x1_plus(self):
        return self.najdi_element('t IΔN x1, (+):', pretvori_v_osnovne = False) # pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna

    def najdi_t_IΔN_x1_minus(self):
        return self.najdi_element('t IΔN x1, (-):', pretvori_v_osnovne = False)# pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat

    def najdi_t_IΔN_x5_plus(self):
        return self.najdi_element('t IΔN x5, (+):', pretvori_v_osnovne = False)# pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna

    def najdi_t_IΔN_x5_minus(self):
        return self.najdi_element('t IΔN x5, (-):', pretvori_v_osnovne = False)# pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat

    def najdi_t_IΔN_x05_plus(self):
        return self.najdi_element('t IΔN x0.5, (+):', pretvori_v_osnovne = False)# pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna

    def najdi_t_IΔN_x05_minus(self):
        return self.najdi_element('t IΔN x0.5, (-):', pretvori_v_osnovne = False)# pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat

    def najdi_IΔ_plus(self):
        return self.najdi_element('IΔ, (+):')# pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna

    def najdi_IΔ_minus(self):
        return self.najdi_element('IΔ, (-):')# pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat

    def najdi_Uc(self):
        return self.najdi_element('Uc:')

    def najdi_Meja_Uc_Uc_(self):
        return self.najdi_element('Meja(Uc)(Uc):')
        
        # vsi spodnji elementi so za meritve, ki se začnejo z R low 4

    def najdi_Povezava(self):
        return self.najdi_element('Povezava:', pretvori_v_osnovne = False)

    
    def najdi_R_pozitivno(self):
        return self.najdi_element('R+:')

    def najdi_R_negativno(self):
        return self.najdi_element('R-:')

    def najdi_Meja_R(self):
        return self.najdi_element('Meja(R):')

        #vsi spodnji elementi so za meritve, ki se začnejo z Varistor

    def najdi_I_lim(self):
        return self.najdi_element('I lim:')

    def najdi_Sistem(self):
        return self.najdi_element('Sistem:', pretvori_v_osnovne = False)

    def najdi_Obmocje(self):
        return self.najdi_element('Območje:', pretvori_v_osnovne = False)

    def najdi_Uac(self):
        return self.najdi_element('Uac:')

    def najdi_Udc(self):
        return self.najdi_element('Udc:')

    def najdi_Spodnja_meja_Uac(self):
        return self.najdi_element('Spodnja meja(Uac):')

    def najdi_Zgornja_meja_Uac(self):
        return self.najdi_element('Zgornja meja(Uac):')

        #vsi spodnji elementi so za meritve ki se začnejo z R iso

    def najdi_Uizo(self):
        return self.najdi_element('Uizo:')

    def najdi_Rln(self):
        return self.najdi_element('Rln:')

    def najdi_Rlpe(self):
        return self.najdi_element('Rlpe:')

    def najdi_Rnpe(self):
        return self.najdi_element('Rnpe:')

    def najdi_Umln(self):
        return self.najdi_element('Umln:')

    def najdi_Umlpe(self):
        return self.najdi_element('Umlpe:')

    def najdi_Umnpe(self):
        return self.najdi_element('Umnpe:')

    def najdi_MejaRln_Rlpe_Rnpe(self):
        return self.najdi_element('Meja(Rln, Rlpe, Rnpe):')


def zapisi_kocko_meritev_v_excel(kocka, loceno_besedilo, slovar_kock_in_ustreznih_poti):
    """
    Zapiše meritev v csv datoteko, ki je primerna za obdelavo v csv-ju
    
    Args: kocka, loceno_besedilo, slovar_kock_in_ustreznih_poti
    """
    
    uln, ZL, ipsc_ln, ipsc_lpe = "","","", ""
    dU, ZS, glavna_izenac_povezava = "","",""
    ia_psc_navidezni_stolpec, maxRplusRminus, tip_varovalke = "","",""
    I_varovalke, t_varovalke, isc_faktor = "","",""
    komentar = ""
    
    pot = slovar_kock_in_ustreznih_poti[loceno_besedilo.index(kocka)]
    # Za vsak slučaj preverimo, ali pot ne obstaja
    if pot is None:
        print("Ni poti, oz prišlo je do napake")
    
    vrste_meritev = [meritev.doloci_vrsto_meritve() for meritev in kocka]
    slovar_vrst_meritev = {i:vrste_meritev.count(i) for i in seznam_vrst_meritev}
    
    if slovar_vrst_meritev["R low 4"] > 1:
        print("Napaka: Imamo 2 ali več R low 4 meritvi v eni kocki!")
    
    # najprej določimo R low 4 ter padec napetosti
    
    for meritev in kocka:
        vrsta_meritve = meritev.doloci_vrsto_meritve()
        if vrsta_meritve == "R low 4":
            
            glavna_izenac_povezava = meritev.najdi_R().replace(" Ω", "")
            R_pozitivno_int = int(meritev.najdi_R_pozitivno().replace(" Ω", "").replace(">", ""))
            R_negativno_int = int(meritev.najdi_R_negativno().replace(" Ω", "").replace(">", ""))
            if ">1999" in meritev.najdi_R_pozitivno()[0] or ">1999" in meritev.najdi_R_negativno()[0]:
                maxRplusRminus = ">1999"
            else:
                R_pozitivno_int = int(meritev.najdi_R_pozitivno().replace(" Ω", "").replace(">", ""))
                R_negativno_int = int(meritev.najdi_R_negativno().replace(" Ω", "").replace(">", ""))
                maxRplusRminus = f"{max(R_negativno_int, R_pozitivno_int)}"
    
            maxRplusRminus = f"{max(R_pozitivno_int, R_negativno_int)}"
        
        if vrsta_meritve == "Padec napetosti":
            dU = meritev.najdi_dU()
            
    # najprej odpravimo AUTO TN
    
    for meritev in kocka:
        vrsta_meritve = meritev.doloci_vrsto_meritve()
        if vrsta_meritve == "AUTO TN":
            with open("csv_za_excel_datoteko.csv", "a", encoding='utf-8', newline='') as csvfile:
        
                writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                uln = meritev.najdi_Uln()
                ZL = meritev.najdi_Z_LN()
                ipsc_ln = meritev.najdi_Ipsc_LN()
                ipsc_lpe = meritev.najdi_Ipsc_LPE()
                if not dU:
                    dU = meritev.najdi_dU()
                ZS = meritev.najdi_Z_LPE()
                ia_psc_navidezni_stolpec = meritev.najdi_Ia_Ipsc()
                tip_varovalke = meritev.najdi_tip_varovalke()
                I_varovalke = meritev.najdi_I_varovalke()
                t_varovalke = meritev.najdi_t_varovalke()
                isc_faktor = meritev.najdi_Isc_faktor()
                komentar = meritev.najdi_komentar()
                
                array_ki_gre_v_csv = [uln, ZL, ipsc_ln, dU, ZS, ipsc_lpe, glavna_izenac_povezava,  maxRplusRminus, tip_varovalke, I_varovalke, t_varovalke, isc_faktor, ia_psc_navidezni_stolpec, komentar]
                writer.writerow(array_ki_gre_v_csv)
                csvfile.close()
                
    # nato odpravimo Zloop / Zine
    
    if "Zloop" in vrste_meritev or "Z LINE" in vrste_meritev:
        ustrezni_zline_3 = []
        ustrezni_zloop_3 = []
        for meritev in kocka:
            vrsta_meritve = meritev.doloci_vrsto_meritve()
            if vrsta_meritve == "Zloop":
                ustrezni_zloop_3.append(meritev)
            if vrsta_meritve == "Z LINE":
                if "400" == meritev.najdi_Un():
                    ustrezni_zline_3.append(meritev)

                    
        if len(ustrezni_zline_3) != len(ustrezni_zloop_3) or len(ustrezni_zline_3) != 3 or len(ustrezni_zloop_3) != 3:
            print("\nNapaka: Nekaj ni v redu s številom zloop/zlinov")
            print("Pot problematične meritve:", pot.strip())
            print("Dolžina zloop", len(ustrezni_zloop_3))
            print("Dolžina zline", len(ustrezni_zline_3))

        else:
            for i in range(3):
                with open("csv_za_excel_datoteko.csv", "a", encoding='utf-8', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    
                    uln = ustrezni_zloop_3[i].najdi_Uln()
                    ipsc = ustrezni_zline_3[i].najdi_Ipsc()
                    z = ustrezni_zline_3[i].najdi_Z()
                    ipsc_lpe = ustrezni_zloop_3[i].najdi_Ipsc_LPE()
                    
                    ZS = ustrezni_zloop_3[i].najdi_Z_LPE()
                    ia_psc_navidezni_stolpec = ustrezni_zloop_3[i].najdi_Ia_Ipsc()
                    tip_varovalke = ustrezni_zloop_3[i].najdi_tip_varovalke()
                    I_varovalke = ustrezni_zloop_3[i].najdi_I_varovalke()
                    t_varovalke = ustrezni_zloop_3[i].najdi_t_varovalke()
                    isc_faktor = ustrezni_zloop_3[i].najdi_Isc_faktor()
                    komentar = ustrezni_zloop_3[i].najdi_komentar()
                    
                    array_ki_gre_v_csv = [uln, ipsc, z, dU, ZS, ipsc_lpe, glavna_izenac_povezava, maxRplusRminus, tip_varovalke, I_varovalke, t_varovalke, isc_faktor, ia_psc_navidezni_stolpec, komentar]
                    writer.writerow(array_ki_gre_v_csv)
                    csvfile.close()

def najdi_seznam_datumov(vse_besedilo):
        loceno_besedilo_po_presledkih = vse_besedilo.split()
        seznam_stringov_z_datumi = []
        for i in loceno_besedilo_po_presledkih:
            # \d\d\.\d\d\.\d\d\d\d je pravi regex expression za to obliko datuma
            if re.search(r"\d{2}\.\d{2}\.\d{4}", i): #".2021" in i or ".2022" in i:
                # vsi datumi so pravilne oblike, zato je upravičeno tole
                string_datuma = i[9:]
                datum = datetime.strptime(string_datuma, '%d.%m.%Y')
                seznam_stringov_z_datumi.append(datum)
        return sorted(seznam_stringov_z_datumi)
    
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



            

    
    
    
