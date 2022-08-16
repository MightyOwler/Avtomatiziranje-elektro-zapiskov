# datoteka za branje podatkov z datoteke

with open("Podatki_z_merjenj.txt", encoding="utf-8") as podatki:
    vse_besedilo =  podatki.read()
    loceno_besedilo = vse_besedilo.split("Posamezne meritve")
    #print(loceno_besedilo[:10])
    print(len(loceno_besedilo), vse_besedilo.count("Pot"), vse_besedilo.count("Serijsko"))
    print(vse_besedilo.count("prazno"))
    print(vse_besedilo.count("neustrezno"))
    #print(max([i.count("prazno") for i in loceno_besedilo]))
    
    # pot je točno tolikokrat kot posamezne meritve kot serijsko!!!
    # vsaka meritev je spodnje oblike
    # Posamezne meritve ___________ Serijsko
    # beseda prazno se lahko pojavi največ 1-krat na posamezno meritev
    # če se pojavi 'prazno', je meritev zavržena
    
    
    # odvrževa brezvezne meritve
    loceno_discardane_prazne = [i.replace("\n","") for i in loceno_besedilo if i.count("prazno") == 0]
    print(len(loceno_discardane_prazne))
    
    matrika_vseh_merjenj = [posamezna_meritev.split(", ") for posamezna_meritev in loceno_discardane_prazne]
    print(matrika_vseh_merjenj[10])
    #print([len(i) for i in loceno_besedilo[1:]])
    
