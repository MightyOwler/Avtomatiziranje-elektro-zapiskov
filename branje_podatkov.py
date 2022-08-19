# datoteka za branje podatkov z datoteke

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
    print(len(loceno_besedilo_discardane_prazne))
    
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
    
    # to ni popolno, saj ne odstrani Page
    def najdi_pot(self):
        return ["P" + self.najdi_element('Pot:')[0]]
    
    
mnozica_vseh_objektov_meritev = [Meritev(i) for i in loceno_besedilo_discardane_prazne]   
#print(mnozica_vseh_objektov_meritev[10].besedilo_po_elementih)


with open("poenostavljeni_podatki.txt", "w", encoding="utf-8") as f:
    for j,i in enumerate(mnozica_vseh_objektov_meritev):
    #print(i.besedilo_po_elementih)
        f.write("Številka meritve"+ " " + str(j + 1))
        f.write("\n")
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
        f.write("\n----------------------------------------------------------------------------------------------------\n")

for j,i in enumerate(mnozica_vseh_objektov_meritev):
    #print(i.besedilo_po_elementih)
    print("Številka meritve", j+1)
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
    print("------------------")

    

najin_objekt = mnozica_vseh_objektov_meritev[85]
print(najin_objekt.besedilo)
print(najin_objekt.besedilo_po_elementih)