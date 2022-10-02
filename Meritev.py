seznam_vrst_meritev = ["AUTO TN", "Zloop", "Z LINE",
                       "RCD Auto", "R low 4", "Varistor", "R iso", "Padec napetosti"]
seznam_enot_za_pretvorbe = ["V", "A", "Ω", "s"]
seznam_predpon_za_pretvorbe = ["m", "k"]

class Meritev():
    def __init__(self, besedilo_meritve):
        self.besedilo = besedilo_meritve
        self.besedilo_po_elementih = [
            i.replace("Pot:", "Pot: ").strip() for i in besedilo_meritve.split(", ")]

        self.vrsta_meritve = self.doloci_vrsto_meritve

    def doloci_vrsto_meritve(self):
        for vrsta_meritve in seznam_vrst_meritev:
            if vrsta_meritve in self.besedilo:
                return vrsta_meritve

    def najdi_komentar(self):
        if "Comment:" in self.besedilo:
            st_pojavitev = self.besedilo.count("Comment:")
            idx_komentarja = najdi_n_to_pojavitev_substringa(
                self.besedilo, "Comment:", st_pojavitev)
            komentar = self.besedilo[idx_komentarja:]
            return komentar.replace("Comment:", "").replace("//", "").strip()
        else:
            return ""

    def najdi_element(self, ime_elementa, pretvori_v_osnovne=True):
        element = "X"
        for i in self.besedilo_po_elementih:
            if ime_elementa in i:
                element = i[len(ime_elementa) + 1:]
                if pretvori_v_osnovne:
                    return pretvori_v_osnovne_enote(element)
                else:
                    return element
        return element

    # spodnji elementi so za meritve, ki se začnejo z AUTO TN

    def najdi_pot(self):
        return self.najdi_element('Pot:', pretvori_v_osnovne=False)

    def najdi_tip_varovalke(self):
        return self.najdi_element('Tip varov.:', pretvori_v_osnovne=False)

    def najdi_I_varovalke(self):
        return self.najdi_element('I varovalke:')

    # tukaj je vedno v sekundah?
    def najdi_t_varovalke(self):
        return self.najdi_element('t varovalke:')

    def najdi_Isc_faktor(self):
        return self.najdi_element('Isc faktor:', pretvori_v_osnovne=False)

    def najdi_I_preizkusa(self):
        return self.najdi_element('I preizkusa:')

    def najdi_Uln(self):
        return self.najdi_element('Uln:')

    def najdi_dU(self):
        return self.najdi_element('dU:', pretvori_v_osnovne=False).replace(" %", "")

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

    # spodnje meritve so za meritve, ki se začnejo z Zloop in Z LINE
    # to bo treba še bolje definirati

    def najdi_Merilno_breme(self):
        return self.najdi_element('Merilno breme:')

    def najdi_Povprečje(self):
        return self.najdi_element('Povprečje:', pretvori_v_osnovne=False)

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

    # spodnji elementi so za meritve ki se začnejo z RCD Auto

    def najdi_Uporaba(self):
        return self.najdi_element('Uporaba:', pretvori_v_osnovne=False)

    def najdi_Tip(self):
        return self.najdi_element('Tip:', pretvori_v_osnovne=False)

    def najdi_I_dN(self):
        return self.najdi_element('I dN:')

    def najdi_Preizkus(self):
        return self.najdi_element('Preizkus:')

    def najdi_RCD_standard(self):
        return self.najdi_element('RCD standard:')

    def najdi_Ozemljitveni_sistem(self):
        return self.najdi_element('Ozemljitveni sistem:')

    def najdi_t_IΔN_x1_plus(self):
        # pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna
        return self.najdi_element('t IΔN x1,(+):', pretvori_v_osnovne=False)

    def najdi_t_IΔN_x1_minus(self):
        # pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat
        return self.najdi_element('t IΔN x1,(-):', pretvori_v_osnovne=False)

    def najdi_t_IΔN_x5_plus(self):
        # pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna
        return self.najdi_element('t IΔN x5,(+):', pretvori_v_osnovne=False)

    def najdi_t_IΔN_x5_minus(self):
        # pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat
        return self.najdi_element('t IΔN x5,(-):', pretvori_v_osnovne=False)

    def najdi_t_IΔN_x05_plus(self):
        # pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna
        return self.najdi_element('t IΔN x0.5,(+):', pretvori_v_osnovne=False)

    def najdi_t_IΔN_x05_minus(self):
        # pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat
        return self.najdi_element('t IΔN x0.5,(-):', pretvori_v_osnovne=False)

    def najdi_IΔ_plus(self):
        # pri tej meritvi pogledaš za isto meritev samo da je - namesto + in pogledaš katera vrednost je večja, tista vrednost je pomembna
        return self.najdi_element('IΔ,(+):')

    def najdi_IΔ_minus(self):
        # pri tev meritvi pogledaš zgornjo, ki ima x1 (+) in pogledaš katera ot teh dveh je večja. to vrednost uporabiš kot rezultat
        return self.najdi_element('IΔ,(-):')

    def najdi_Uc(self):
        return self.najdi_element('Uc:')

    def najdi_Meja_Uc_Uc_(self):
        return self.najdi_element('Meja(Uc)(Uc):')

        # vsi spodnji elementi so za meritve, ki se začnejo z R low 4

    def najdi_Povezava(self):
        return self.najdi_element('Povezava:', pretvori_v_osnovne=False)

    def najdi_R_pozitivno(self):
        return self.najdi_element('R+:')

    def najdi_R_negativno(self):
        return self.najdi_element('R-:')

    def najdi_Meja_R(self):
        return self.najdi_element('Meja(R):')

        # vsi spodnji elementi so za meritve, ki se začnejo z Varistor

    def najdi_I_lim(self):
        return self.najdi_element('I lim:')

    def najdi_Sistem(self):
        return self.najdi_element('Sistem:', pretvori_v_osnovne=False)

    def najdi_Obmocje(self):
        return self.najdi_element('Območje:', pretvori_v_osnovne=False)

    def najdi_Uac(self):
        return self.najdi_element('Uac:')

    def najdi_Udc(self):
        return self.najdi_element('Udc:')

    def najdi_Spodnja_meja_Uac(self):
        return self.najdi_element('Spodnja meja(Uac):')

    def najdi_Zgornja_meja_Udc(self):
        return self.najdi_element('Zgornja meja(Udc):')

        # vsi spodnji elementi so za meritve ki se začnejo z R iso

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
    
    
def najdi_n_to_pojavitev_substringa(glavni_string, iskani_substring, n):
    start = glavni_string.find(iskani_substring)
    while start >= 0 and n > 1:
        start = glavni_string.find(
            iskani_substring, start+len(iskani_substring))
        n -= 1
    return start

def pretvori_v_osnovne_enote(besedilo_ki_ga_pretvarjamo):
    """
    Funkcija, ki pretvarja iz mili ali kilo enot v osnovne
    """

    for predpona in seznam_predpon_za_pretvorbe:
        for enota in seznam_enot_za_pretvorbe:
            if predpona + enota in besedilo_ki_ga_pretvarjamo:
                besedilo_ki_ga_pretvarjamo = besedilo_ki_ga_pretvarjamo.replace(
                    " " + predpona + enota, "").replace(",", ".")
                besedilo_ki_ga_pretvarjamo = float(besedilo_ki_ga_pretvarjamo)
                if predpona == "m":
                    besedilo_ki_ga_pretvarjamo /= 1000
                    besedilo_ki_ga_pretvarjamo = round(
                        besedilo_ki_ga_pretvarjamo, 3)
                else:
                    besedilo_ki_ga_pretvarjamo *= 1000
                    besedilo_ki_ga_pretvarjamo = round(
                        besedilo_ki_ga_pretvarjamo, 3)
                    if besedilo_ki_ga_pretvarjamo >= 100:
                        besedilo_ki_ga_pretvarjamo = int(besedilo_ki_ga_pretvarjamo)

                return f"{besedilo_ki_ga_pretvarjamo}".replace(".", ",")
    for enota in seznam_enot_za_pretvorbe:
        if enota in besedilo_ki_ga_pretvarjamo:
            return f"{besedilo_ki_ga_pretvarjamo}".replace(" " + enota, "").replace(".", ",")
    
    return besedilo_ki_ga_pretvarjamo