# datoteka za branje podatkov z datoteke

import re
from datetime import datetime

#obstaja 7 vrst meritev: AUTO TN, Zloop mΩ, Z LINE, RCD Auto, R low 4, Varistor, R iso
seznam_vrst_meritev = ["AUTO TN", "Zloop mΩ", "Z LINE", "RCD Auto", "R low 4", "Varistor", "R iso"]

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


with open("Podatki_z_merjenj.txt", encoding="utf-8") as podatki:
    vse_besedilo =  podatki.read()
    loceno_besedilo_na_kocke_teksta = vse_besedilo.split("Posamezne meritve")
    
    
    """
    Tukaj moramo pogledati vse datume iz datoteke, dobimo jih lahko tako, da pogledamo .2021
    """
    
    loceno_besedilo_po_presledkih = vse_besedilo.split()
    seznam_stringov_z_datumi = []
    for i in loceno_besedilo_po_presledkih:
        # \d\d\.\d\d\.\d\d\d\d je pravi regex expression
        if re.search(r"\d{2}\.\d{2}\.\d{4}", i): #".2021" in i or ".2022" in i:
            # vsi datumi so pravilne oblike, zato je upravičeno tole
            string_datuma = i[9:]
            #print(string_datuma)
            datum = datetime.strptime(string_datuma, '%d.%m.%Y')
            # tukaj je treba ustrezno pretvoriti datum v datetime obliko
            seznam_stringov_z_datumi.append(datum)
    seznam_stringov_z_datumi = sorted(seznam_stringov_z_datumi)
    print("Meritve so bile opravljene od:", seznam_stringov_z_datumi[0], "do:", seznam_stringov_z_datumi[-1])
    
    # vsaka meritev je spodnje oblike 
    # Posamezne meritve ___________ Serijsko
    # (ni res, ker se vmes lahko skriva več posameznih meritev. Morala bova bolje ločiti med njimi)
    
    # beseda prazno se lahko pojavi največ 1-krat na posamezno meritev // ni res
    # če se pojavi 'prazno', je meritev zavržena // to bo treba še popraviti
    
    
    
    
    # od Page dalje do serijskega lahko vse discardamo
    # odvrževa brezvezne meritve
    

    
    loceno_besedilo = []
    dolzine = []
    
    
    # vprašanje, če je to v redu, ker dejansko so v tabelicah skupaj zlepljene posamezne meritve...
    # verjentno bo treba v razredu Meritev ločiti med seboj posamezne meritve...
    # je pa spodnja koda kar uporabna za to
    for kocka_teksta in loceno_besedilo_na_kocke_teksta:
        slovar_meritev = {i:0 for i in seznam_vrst_meritev}
        for vrsta_meritve in seznam_vrst_meritev:
            if vrsta_meritve in kocka_teksta:
                slovar_meritev[vrsta_meritve] = kocka_teksta.count(vrsta_meritve)
                vsota_meritev = sum(slovar_meritev.values())
                dolzine.append(vsota_meritev)
                if vsota_meritev == 1:
                    # v tem primeru ni problemov, saj je meritev itak ustrezna
                    loceno_besedilo.append(vrsta_meritve)
                else:
                    # v tem primeru pa se moramo še malo potruditi
                    seznam_indeksov = []
                    for key in slovar_meritev:
                        seznam_indeksov += [m.start() for m in re.finditer(key, kocka_teksta)]
                    seznam_indeksov.sort()
                    loceno_besedilo += [kocka_teksta[i:j] for i,j in zip(seznam_indeksov, seznam_indeksov[1:]+[None])]
                    # print(seznam_indeksov)
                    # print(slovar_meritev)
                    
    
    
    # Treba je še dodati pot in datum vse meritvam, ki niso na sredini (poglej, če imajo vse datum!)
    
    # print(len(loceno_besedilo))
    # print(max(dolzine), len(dolzine), sum(dolzine))
    # for i in range(20):
    #     print(loceno_besedilo[i] + "\n\n")
    
    loceno_besedilo_discardane_prazne = [i.replace("\n"," ") for i in loceno_besedilo_na_kocke_teksta if i.count("prazno") == 0]
    
    matrika_vseh_merjenj = [posamezna_meritev.split(", ") for posamezna_meritev in loceno_besedilo_discardane_prazne]


class Meritev():
    def __init__(self, besedilo_meritve):
        self.besedilo = besedilo_meritve
        self.besedilo_po_elementih = [i.replace("Pot:", "Pot: ").strip() for i in besedilo_meritve.split(", ")]
        
        self.vrsta_meritve = self.doloci_vrsto_meritve
        
    def doloci_vrsto_meritve(self):
        if "AUTO TN" in self.besedilo:
            return True
        else:
            return False
    
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
    def najdi_pot(self):
        string_skupaj_s_page = self.najdi_element('Pot:')[0]
        if "Page" in string_skupaj_s_page:
            idx = string_skupaj_s_page.find("Page")
            # poanta je v temu, da so spredaj odvečne črke
            return [string_skupaj_s_page[4:idx]]
        else:
            return [string_skupaj_s_page[4:]]
        
        
    
    
mnozica_vseh_objektov_meritev = [Meritev(i) for i in loceno_besedilo_discardane_prazne]   
#print(mnozica_vseh_objektov_meritev[10].besedilo_po_elementih)


# with open("poenostavljeni_podatki.txt", "w", encoding="utf-8") as f:
#     for j,i in enumerate(mnozica_vseh_objektov_meritev):
#     #print(i.besedilo_po_elementih)
#         f.write("Številka meritve"+ " " + str(j + 1))
#         f.write("\n")
#         # spodnji elementi veljajop za meritve, ki se začnejo z AUTO TN
#         f.write(str(i.najdi_tip_varovalke()))
#         f.write("\n")
#         f.write(str(i.najdi_I_varovalke()))
#         f.write("\n")
#         f.write(str(i.najdi_t_varovalke()))
#         f.write("\n")
#         f.write(str(i.najdi_Isc_faktor()))
#         f.write("\n")
#         f.write(str(i.najdi_dU()))
#         f.write("\n")
#         f.write(str(i.najdi_Z_LPE()))
#         f.write("\n")
#         f.write(str(i.najdi_I_preizkusa()))
#         f.write("\n")
#         f.write(str(i.najdi_Ipsc_LPE()))
#         f.write("\n")
#         f.write(str(i.najdi_Uln()))
#         f.write("\n")
#         f.write(str(i.najdi_R()))
#         f.write("\n")
#         f.write(str(i.najdi_Zref()))
#         f.write("\n")
#         f.write(str(i.najdi_meja_dU()))
#         f.write("\n")
#         f.write(str(i.najdi_pot()))
#         # spodnje meritve so za meritve ki se začnejo z Zloop in Z LINE 
#         f.write("\n")
#         f.write(str(i.najdi_Merilno_breme()))
#         f.write("\n")
#         f.write(str(i.najdi_Povprečje()))
#         f.write("\n")
#         f.write(str(i.najdi_Toleranca()))
#         f.write("\n")
#         f.write(str(i.najdi_Ipsc()))
#         f.write("\n")
#         f.write(str(i.najdi_Z()))
#         f.write("\n")
#         f.write(str(i.najdi_XL()))
#         f.write("\n")
#         f.write(str(i.najdi_IscMax()))
#         f.write("\n")
#         f.write(str(i.najdi_IscMin()))
#         f.write("\n")
#         f.write(str(i.najdi_Ia_Ipsc()))
#         f.write("\n")
#         f.write("\n----------------------------------------------------------------------------------------------------\n")


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
#     print(i.najdi_pot())
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

    

najin_objekt = mnozica_vseh_objektov_meritev[35]
# print(najin_objekt.najdi_Isc_faktor())
# print(najin_objekt.najdi_Ozemljitveni_sistem())
# print(najin_objekt.doloci_vrsto_meritve())
# print(najin_objekt.najdi_pot())
print("-----------------------------------------------------------------")
# print(najin_objekt.besedilo_po_elementih)

#P-Ustrezno F-Neustrezno, E-Prazno, N-Ne obstaja
# to ubistu pomeni isto kot ustrezno, prazno, narobe ki je pojavi na začetku vsakega sklopa meritev samo da tukaj se pojavi za vsako meritvijo, kar pomeni da lahko na ta način ločiva meritve eno od druge