# datoteka za branje podatkov z datoteke

from ast import Return


with open("Podatki_z_merjenj.txt", encoding="utf-8") as podatki:
    vse_besedilo =  podatki.read()
    loceno_besedilo = vse_besedilo.split("Posamezne meritve")
    
    # pot je točno tolikokrat kot posamezne meritve kot serijsko!!!
    # vsaka meritev je spodnje oblike
    # Posamezne meritve ___________ Serijsko
    # beseda prazno se lahko pojavi največ 1-krat na posamezno meritev
    # če se pojavi 'prazno', je meritev zavržena
    # od Page dalje do serijskega lahko vse discardamo
    
    # odvrževa brezvezne meritve
    loceno_besedilo_discardane_prazne = [i.replace("\n"," ") for i in loceno_besedilo if i.count("prazno") == 0]
    
    matrika_vseh_merjenj = [posamezna_meritev.split(", ") for posamezna_meritev in loceno_besedilo_discardane_prazne]


class Meritev():
    def __init__(self, besedilo_meritve):
        self.besedilo = besedilo_meritve
        self.besedilo_po_elementih = besedilo_meritve.split(", ")
    
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

    #spodnji lelementi so za meritve ki se začnejo z RCD Auto

    def najdi_Uporaba(self):
        return self.najdi_element('Uporaba:')

    def najdi_I_dN(self):
        return self.najdi_element('Tip:')

    def najdi_Tip(self):
        return self.najdi_element('I dN:')

    def najdi_Preizkus(self):
        return self.najdi_element('Preizkus):')

    def najdi_RCD_standard(self):
        return self.najdi_element('RCD standard):')

    def najdi_Ozemljitveni_sistem(self):
        return self.najdi_element('Ozemljitveni sistem):')

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


    
    
    # to ni popolno, saj ne odstrani Page
    # tole je treba malo popraviti
    def najdi_pot(self):
        return ["P" + self.najdi_element('Pot:')[0]]
    
    
mnozica_vseh_objektov_meritev = [Meritev(i) for i in loceno_besedilo_discardane_prazne]   
#print(mnozica_vseh_objektov_meritev[10].besedilo_po_elementih)


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
        f.write(str(i.najdi_pot()))
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

for j,i in enumerate(mnozica_vseh_objektov_meritev):
    #print(i.besedilo_po_elementih)
    print("Številka meritve", j+1)
    # print(i.AUTO_TN())
    # print(i.Zloop())
    # print(i.Z_LINE)
    print(i.najdi_tip_varovalke())
    print(i.najdi_I_varovalke())
    print(i.najdi_t_varovalke())
    print(i.najdi_Isc_faktor())
    print(i.najdi_dU())
    print(i.najdi_Z_LPE())
    print(i.najdi_I_preizkusa())
    print(i.najdi_Ipsc_LPE())
    print(i.najdi_Uln())
    print(i.najdi_R())
    print(i.najdi_Zref())
    print(i.najdi_meja_dU())
    print(i.najdi_pot())
    #spodnji veljajo za meritve, ki se začnejo z Zloop in Z LINE
    print(i.najdi_Merilno_breme())
    print(i.najdi_Povprečje())
    print(i.najdi_Toleranca())
    print(i.najdi_Ipsc())
    print(i.najdi_Z())
    print(i.najdi_XL())
    print(i.najdi_IscMax())
    print(i.najdi_IscMin())
    print(i.najdi_Ia_Ipsc())
    #spodnje veljajo za meritve ki se začnejo z RCD Auto
    print(i.najdi_Uporaba())
    print(i.najdi_Tip())
    print(i.najdi_I_dN())
    print(i.najdi_Preizkus())
    print(i.najdi_RCD_standard())
    print(i.najdi_Ozemljitveni_sistem())
    print(i.najdi_t_IΔN_x1_plus())
    print(i.najdi_t_IΔN_x1_minus())
    print(i.najdi_t_IΔN_x5_plus())
    print(i.najdi_t_IΔN_x5_minus())
    print(i.najdi_t_IΔN_x05_plus())
    print(i.najdi_t_IΔN_x05_minus())
    print(i.najdi_IΔ_plus())
    print(i.najdi_IΔ_minus())
    print(i.najdi_Uc())
    print(i.najdi_Meja_Uc_Uc_())
    print("------------------")
    
    # pod potjo se sedaj napišejo se ostali elementi ( niso pa še vsi)

    

najin_objekt = mnozica_vseh_objektov_meritev[10]
print(najin_objekt.najdi_Isc_faktor())
# print(najin_objekt.besedilo_po_elementih)

#P-Ustrezno F-Neustrezno, E-Prazno, N-Ne obstaja
# to ubistu pomeni isto kot ustrezno, prazno, narobe ki je pojavi na začetku vsakega sklopa meritev samo da tukaj se pojavi za vsako meritvijo, kar pomeni da lahko na ta način ločiva meritve eno od druge