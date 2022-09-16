# datoteka za branje podatkov z datoteke
import model
import re

# neprazne meritve
# AUTO TN: 434
# Zloop mΩ: 66
# Z LINE: 106
# RCD Auto: 33
# R low 4: 0
# Varistor: 0
# Padec napetosti: 1
# R iso: 0doloci_vrsto_meritve

# kot vidimo zgoraj, je nepraznih zline meritev 106 namesto 108 (ker sta 2 prazni!!)

#problem je v tem, da ne loči še med AUTO TN in AUTO TN (RCD)
#to ni velik problem: AUTO TN (RCD) --> Auto Tn (RCD) bo rešilo problem
#obstaja 7 vrst meritev: AUTO TN, Zloop mΩ, Z LINE, RCD Auto, R low 4, Varistor, R iso


seznam_vrst_meritev = model.seznam_vrst_meritev


with open("Podatki_z_merjenj.txt", encoding="utf-8") as podatki:
    vse_besedilo =  podatki.read()
    loceno_besedilo_na_kocke_teksta = vse_besedilo.split("Posamezne meritve")
    
    
    seznam_datumov_po_vrstnem_redu = model.najdi_seznam_datumov(vse_besedilo)
    #tukaj se da še polepšati zapis datuma
    print("Meritve so bile opravljene od:", seznam_datumov_po_vrstnem_redu[0], "do:", seznam_datumov_po_vrstnem_redu[-1])

    loceno_besedilo_brez_poti_na_koncu = []
    dolzine = []
    seznam_ustreznih_poti_do_kock = []
    
    def ustvari_seznam_vseh_meritev():
        loceno_besedilo = []
        
        for kocka_teksta in loceno_besedilo_na_kocke_teksta:
            slovar_meritev = {i:0 for i in seznam_vrst_meritev}
            pot_do_druzine_meritev = model.najdi_pot_izven_razreda_Meritev(kocka_teksta)
            idx_poti = kocka_teksta.find("Pot:")
            kocka_teksta = kocka_teksta[:idx_poti]

            
            for vrsta_meritve in seznam_vrst_meritev:
                if vrsta_meritve in kocka_teksta:
                    slovar_meritev[vrsta_meritve] = kocka_teksta.count(vrsta_meritve)
                    
            vsota_meritev = sum(slovar_meritev.values())
            #to je zato, da lahko preverimo, koliko meritev obstaja 
            dolzine.append(vsota_meritev)
            if vsota_meritev == 1:
                # v primeru, da je v kocki teksta samo ena meritev ni problemov, saj je meritev kar celotna kocka
                if kocka_teksta.count("p//") == 0:
                    loceno_besedilo.append([model.Meritev(kocka_teksta.replace("\n", " ").replace("\r\n", " ").strip())])
                    seznam_ustreznih_poti_do_kock.append(pot_do_druzine_meritev)
                
            else:
                # sicer pa se moramo še malo potruditi
                seznam_indeksov = []
                loceno_besedilo_brez_poti_na_koncu = []
                for key in slovar_meritev:  
                    seznam_indeksov += [m.start() for m in re.finditer(key, kocka_teksta)]
                seznam_indeksov.sort()    
                loceno_besedilo_brez_poti_na_koncu += [kocka_teksta[i:j] for i,j in zip(seznam_indeksov, seznam_indeksov[1:]+[None])]
                loceno_besedilo_zacasno = []
                for meritev in loceno_besedilo_brez_poti_na_koncu:
                    if meritev.count("p//") == 0:
                        loceno_besedilo_zacasno.append(model.Meritev(meritev.replace("\n", " ").replace("\r\n", " ").strip()))
                if loceno_besedilo_zacasno:
                    loceno_besedilo.append(loceno_besedilo_zacasno)
                    seznam_ustreznih_poti_do_kock.append(pot_do_druzine_meritev)

                
             
        return loceno_besedilo
    
    # loceno_besedilo so meritve, vse meritve, ne glede na kocke (v eni kocki je lahko več meritev)
    loceno_besedilo = ustvari_seznam_vseh_meritev()
    slovar_kock_in_ustreznih_poti = dict(zip(range(len(loceno_besedilo)), seznam_ustreznih_poti_do_kock))
    
    
    print(len(loceno_besedilo), len(seznam_ustreznih_poti_do_kock))
    
    with open("csv_za_excel_datoteko.csv", "w", encoding='utf-8', newline='') as csvfile:
        csvfile.close()
    for kocka in loceno_besedilo:
        model.zapisi_kocko_meritev_v_excel(kocka, loceno_besedilo, slovar_kock_in_ustreznih_poti)
    
    


print("-----------------------------------------------------------------")


#P-Ustrezno F-Neustrezno, E-Prazno, N-Ne obstaja
# to ubistu pomeni isto kot ustrezno, prazno, narobe ki je pojavi na začetku vsakega sklopa meritev samo da tukaj se pojavi za vsako meritvijo, kar pomeni da lahko na ta način ločiva meritve eno od druge

# vsi elementi v posameznih vrstah meritev

#AUTO TN----Tip varov, I varovalke, t varovalke, Isc faktor, Uln, dU, R, Z (LPE), Z (LN), Ipsc (LN), Ipsc (LPE), Zref, Meja(dU), Meja(R), Ia(Ipsc (LN), Ipsc (LPE))

#Zloop-----Tip varov, I varovalke, t varovalke, Preizkus, Un, Merilno breme, Povprečje, Isc faktor, Toleranca, Ipsc, Z, XL, R, IscMax, IscMin, Ia(Ipsc)

#Z LINE-----Tip varov, I varovalke, t varovalke, Preizkus, Un, Merilno breme, Povprečje, Isc faktor, Toleranca, Ipsc, Z, XL, R, IscMax, IscMin, Ia(Ipsc)

#RCD AUTO---Uporaba, Tip, I dN, Preizkus, RCD standard, Ozemljitveni sistem, t IΔN x1, (+), t IΔN x1, (-), t IΔN x5, (+), t IΔN x5, (-), t IΔN x0.5, (+), t IΔN x0.5, (-), IΔ, (+), IΔ, (-), Uc, Meja(Uc)(Uc)

#R low 4W---Povezava, R, R+, R-, Meja(R)

#Varistor---I lim, Sistem, Območje, Uac, Udc, Spodnja meja(Uac), Zgornja meja(Uac), 

#R iso------Uizo, Rln, Rlpe, Rnpe, Umln, Umlpe, Umnpe, Meja(Rln, Rlpe, Rnpe)