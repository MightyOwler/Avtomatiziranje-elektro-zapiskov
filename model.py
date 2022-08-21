import re
from datetime import datetime

seznam_vrst_meritev = ["AUTO TN", "Zloop mΩ", "Z LINE", "RCD Auto", "R low 4", "Varistor", "R iso"]

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
    def najdi_element(self, ime_elementa):
        element = []
        for i in self.besedilo_po_elementih:
            if ime_elementa in i:
                element.append(i[len(ime_elementa) + 1:])
                #tole bo zraven napisalo še ime
                #element.append(i)
        
        if element:
            return element
        else:
            return "/"

    #spodnji elementi so za meritve, ki se začnejo z AUTO TN
    #to bo treba še bolje definirati
    
    def najdi_pot(self):
        return self.najdi_element('Pot:')
        
    def najdi_tip_varovalke(self):
        return self.najdi_element('Tip varov.:')
    
    def najdi_I_varovalke(self):
        return self.najdi_element('I varovalke:')
    
    def najdi_t_varovalke(self):
        return self.najdi_element('t varovalke:')
    
    def najdi_Isc_faktor(self):
        return self.najdi_element('Isc faktor:')
    
    def najdi_I_preizkusa(self):
        return self.najdi_element('I preizkusa:')
    
    def najdi_Uln(self):
        return self.najdi_element('Uln:')
    
    def najdi_dU(self):
        return self.najdi_element('dU:')
    
    def najdi_Z_LPE(self):
        return self.najdi_element('Z (LPE):')
    
    def najdi_I_preizkusa(self):
        return self.najdi_element('Z (LN):')
    
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
        return self.najdi_element('Povprečje:')

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

    #spodnji elementi so za meritve ki se začnejo z RCD Auto
    #to bo treba še bolje definirati

    def najdi_Uporaba(self):
        return self.najdi_element('Uporaba:')

    def najdi_I_dN(self):
        return self.najdi_element('Tip:')

    def najdi_Tip(self):
        return self.najdi_element('I dN:')

    def najdi_Preizkus(self):
        return self.najdi_element('Preizkus:')

    def najdi_RCD_standard(self):
        return self.najdi_element('RCD standard:')

    def najdi_Ozemljitveni_sistem(self):
        return self.najdi_element('Ozemljitveni sistem:')

    def najdi_t_IΔN_x1_plus(self):
        return self.najdi_element('t IΔN x1, (+):') # pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna

    def najdi_t_IΔN_x1_minus(self):
        return self.najdi_element('t IΔN x1, (-):')# pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat

    def najdi_t_IΔN_x5_plus(self):
        return self.najdi_element('t IΔN x5, (+):')# pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna

    def najdi_t_IΔN_x5_minus(self):
        return self.najdi_element('t IΔN x5, (-):')# pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat

    def najdi_t_IΔN_x05_plus(self):
        return self.najdi_element('t IΔN x0.5, (+):')# pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna

    def najdi_t_IΔN_x05_minus(self):
        return self.najdi_element('t IΔN x0.5, (-):')# pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat

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
        return self.najdi_element('Povezava:')

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
        return self.najdi_element('Sistem:')

    def najdi_Obmocje(self):
        return self.najdi_element('Območje:')

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


    # tole bi znalo biti nekoliko moteče, ker ne vem, ali moram meritve z iste poti obravnavati skupaj
    # če ja, potem bo sicer to ok, vendar bo treba biti precej previden
    def zapisi_meritev_v_latex(self):
        """
        Zapiše meritev v latex datoteko
        """
        pass
    
    def zapisi_meritev_v_excel(self):
        """
        Zapiše meritev v excel datoteko
        """
        pass


    
    # to ni popolno, saj v primeru, da obstaja comment, ne deluje kot bi moralo
def najdi_seznam_datumov(vse_besedilo):
        loceno_besedilo_po_presledkih = vse_besedilo.split()
        seznam_stringov_z_datumi = []
        for i in loceno_besedilo_po_presledkih:
            # \d\d\.\d\d\.\d\d\d\d je pravi regex expression
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
            # poanta je v temu, da so spredaj odvečne črke
            string_ki_ga_obdelujemo = string_ki_ga_obdelujemo[:idx]
        return string_ki_ga_obdelujemo


def ustvari_datoteko_s_poenostavljenimi_podatki(mnozica_vseh_objektov_meritev):
    with open("poenostavljeni_podatki.txt", "w", encoding="utf-8") as f:
        for j,i in enumerate(mnozica_vseh_objektov_meritev):
        #print(i.besedilo_po_elementih)
            f.write("Številka meritve"+ " " + str(j + 1))
            f.write("\n")
            # spodnji elementi veljajop za meritve, ki se začnejo z AUTO TN
            f.write(str(i.najdi_tip_varovalke()))
            f.write("\n")
            f.write(str(i.najdi_I_varovalke()))
            f.write("\n")
            f.write(str(i.najdi_t_varovalke()))
            f.write("\n")
            f.write(str(i.najdi_Isc_faktor()))
            f.write("\n")
            f.write(str(i.najdi_dU()))
            f.write("\n")
            f.write(str(i.najdi_Z_LPE()))
            f.write("\n")
            f.write(str(i.najdi_I_preizkusa()))
            f.write("\n")
            f.write(str(i.najdi_Ipsc_LPE()))
            f.write("\n")
            f.write(str(i.najdi_Uln()))
            f.write("\n")
            f.write(str(i.najdi_R()))
            f.write("\n")
            f.write(str(i.najdi_Zref()))
            f.write("\n")
            f.write(str(i.najdi_meja_dU()))
            f.write("\n")
            #f.write(str(i.najdi_pot()))
            # spodnje meritve so za meritve ki se začnejo z Zloop in Z LINE 
            f.write("\n")
            f.write(str(i.najdi_Merilno_breme()))
            f.write("\n")
            f.write(str(i.najdi_Povprečje()))
            f.write("\n")
            f.write(str(i.najdi_Toleranca()))
            f.write("\n")
            f.write(str(i.najdi_Ipsc()))
            f.write("\n")
            f.write(str(i.najdi_Z()))
            f.write("\n")
            f.write(str(i.najdi_XL()))
            f.write("\n")
            f.write(str(i.najdi_IscMax()))
            f.write("\n")
            f.write(str(i.najdi_IscMin()))
            f.write("\n")
            f.write(str(i.najdi_Ia_Ipsc()))
            f.write("\n")
            f.write("\n----------------------------------------------------------------------------------------------------\n")
            
            
            
            
            
            
# nekoliko odvečne stvari
#-----------------------------------------------------------------------------------------------------

# mnozica_vseh_objektov_meritev = [Meritev(i) for i in loceno_besedilo_discardane_prazne]
# tam kjer je napisano, da so spodnji elementi za x vrsto meritve pomeni da so te meritve take, da se pojavijo samo pri teh meritvah, ni pa naštetih tistih meritev, ki se ponovijo!!!!
# for j,i in enumerate(mnozica_vseh_objektov_meritev):
#     #print(i.besedilo_po_elementih)
#     print("Številka meritve", j+1)
#     # print(i.AUTO_TN())
#     # print(i.Zloop())
#     # print(i.Z_LINE)
#     print(i.najdi_tip_varovalke())
#     print(i.najdi_I_varovalke())
#     print(i.najdi_t_varovalke())
#     print(i.najdi_Isc_faktor())
#     print(i.najdi_dU())
#     print(i.najdi_Z_LPE())
#     print(i.najdi_I_preizkusa())
#     print(i.najdi_Ipsc_LPE())
#     print(i.najdi_Uln())
#     print(i.najdi_R())
#     print(i.najdi_Zref())
#     print(i.najdi_meja_dU())
#     #print(i.najdi_pot())
#     #spodnji veljajo za meritve, ki se začnejo z Zloop in Z LINE
#     print(i.najdi_Merilno_breme())
#     print(i.najdi_Povprečje())
#     print(i.najdi_Toleranca())
#     print(i.najdi_Ipsc())
#     print(i.najdi_Z())
#     print(i.najdi_XL())
#     print(i.najdi_IscMax())
#     print(i.najdi_IscMin())
#     print(i.najdi_Ia_Ipsc())
#     #spodnje veljajo za meritve ki se začnejo z RCD Auto
#     print(i.najdi_Uporaba())
#     print(i.najdi_Tip())
#     print(i.najdi_I_dN())
#     print(i.najdi_Preizkus())
#     print(i.najdi_RCD_standard())
#     print(i.najdi_Ozemljitveni_sistem())
#     print(i.najdi_t_IΔN_x1_plus())
#     print(i.najdi_t_IΔN_x1_minus())
#     print(i.najdi_t_IΔN_x5_plus())
#     print(i.najdi_t_IΔN_x5_minus())
#     print(i.najdi_t_IΔN_x05_plus())
#     print(i.najdi_t_IΔN_x05_minus())
#     print(i.najdi_IΔ_plus())
#     print(i.najdi_IΔ_minus())
#     print(i.najdi_Uc())
#     print(i.najdi_Meja_Uc_Uc_())
# # spodnji veljajo za meritve, ki se začnejo z R low 4
#     print(i.najdi_Povezava())
#     print(i.najdi_R_pozitivno())
#     print(i.najdi_R_negativno())
#     print(i.najdi_Meja_R())
# # spodnji veljajo za elemente, ki se začnjejo z Varistor
#     print(i.najdi_I_lim())
#     print(i.najdi_Sistem())
#     print(i.najdi_Obmocje())
#     print(i.najdi_Uac())
#     print(i.najdi_Udc())
#     print(i.najdi_Spodnja_meja_Uac())
#     print(i.najdi_Zgornja_meja_Uac())
# # spodnji veljajo za meritve, ki se začnjejo z R iso
#     print(i.najdi_Uizo())
#     print(i.najdi_Rln())
#     print(i.najdi_Rlpe())
#     print(i.najdi_Rnpe())
#     print(i.najdi_Umln())
#     print(i.najdi_Umlpe())
#     print(i.najdi_Umnpe())
#     print(i.najdi_MejaRln_Rlpe_Rnpe())

#     print("------------------")
    
    # pod potjo se sedaj napišejo se ostali elementi ( niso pa še vsi)
    
    
    
