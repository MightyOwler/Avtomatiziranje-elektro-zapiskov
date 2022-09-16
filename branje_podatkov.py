# datoteka za branje podatkov z datoteke in generiranje ustrezne csv datoteke
import model
import re

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

    seznam_vseh_meritev_brez_poti_na_koncu = []
    seznam_ustreznih_poti_do_kock = []
    
    def ustvari_seznam_vseh_meritev():
        seznam_vseh_meritev = []
        
        for kocka_teksta in loceno_besedilo_na_kocke_teksta:
            slovar_meritev = {i:0 for i in seznam_vrst_meritev}
            pot_do_druzine_meritev = model.najdi_pot_izven_razreda_Meritev(kocka_teksta)
            idx_poti = kocka_teksta.find("Pot:")
            kocka_teksta = kocka_teksta[:idx_poti]

            
            for vrsta_meritve in seznam_vrst_meritev:
                if vrsta_meritve in kocka_teksta:
                    slovar_meritev[vrsta_meritve] = kocka_teksta.count(vrsta_meritve)
                    
            stevilo_meritev_v_trenutni_kocki = sum(slovar_meritev.values())
            if stevilo_meritev_v_trenutni_kocki == 1:
                # v primeru, da je v kocki teksta samo ena meritev, ni problemov, saj je meritev kar celotna kocka
                if kocka_teksta.count("p//") == 0:
                    seznam_vseh_meritev.append([model.Meritev(kocka_teksta.replace("\n", " ").replace("\r\n", " ").strip())])
                    seznam_ustreznih_poti_do_kock.append(pot_do_druzine_meritev)
                
            else:
                # sicer pa se moramo še malo potruditi
                seznam_indeksov_posameznih_meritev = []
                seznam_vseh_meritev_brez_poti_na_koncu = []
                for key in slovar_meritev:  
                    seznam_indeksov_posameznih_meritev += [m.start() for m in re.finditer(key, kocka_teksta)]
                seznam_indeksov_posameznih_meritev.sort()    
                seznam_vseh_meritev_brez_poti_na_koncu += [kocka_teksta[i:j] for i,j in zip(seznam_indeksov_posameznih_meritev, seznam_indeksov_posameznih_meritev[1:]+[None])]
                loceno_besedilo_zacasno = []
                for meritev in seznam_vseh_meritev_brez_poti_na_koncu:
                    if meritev.count("p//") == 0:
                        loceno_besedilo_zacasno.append(model.Meritev(meritev.replace("\n", " ").replace("\r\n", " ").strip()))
                if loceno_besedilo_zacasno:
                    seznam_vseh_meritev.append(loceno_besedilo_zacasno)
                    seznam_ustreznih_poti_do_kock.append(pot_do_druzine_meritev)

        return seznam_vseh_meritev
    
    # seznam_vseh_meritev so vse meritve, ne glede na kocke (v eni kocki je lahko več meritev)
    seznam_vseh_meritev = ustvari_seznam_vseh_meritev()
    slovar_kock_in_ustreznih_poti = dict(zip(range(len(seznam_vseh_meritev)), seznam_ustreznih_poti_do_kock))
    print("Število vseh meritev:", len(seznam_vseh_meritev), "\nŠtevilo ustreznih poti do meritev:", len(seznam_ustreznih_poti_do_kock))
    
    with open("csv_za_excel_datoteko.csv", "w", encoding='utf-8', newline='') as csvfile:
        csvfile.close()
    for kocka in seznam_vseh_meritev:
        model.zapisi_kocko_meritev_v_excel(kocka, seznam_vseh_meritev, slovar_kock_in_ustreznih_poti)

print("-----------------------------------------------------------------")


