# datoteka za branje podatkov z datoteke in generiranje ustrezne csv datoteke
import model
import Meritev
from colorama import Fore
from meje import *
import re
import os

from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment


# Če hočeš vklopiti debugganje, daš debug_mode na True
debug_mode = True

# obstaja 7 osnovnih vrst meritev: AUTO TN, Zloop mΩ, Z LINE, RCD Auto, R low 4, Varistor, R iso, R IZO, ZLOOP 4W, Zline 4W

trafo_postaja = bool(
    input("Ali je trafo postaja? Če je, napiši karkoli, če ni, pusti prazno! ")
)
if trafo_postaja:
    print(Fore.GREEN + "--------------------------------------")
    print("|| Objekt ima svojo trafo postajo. || ")
    print("--------------------------------------" + Fore.WHITE)

else:
    print(Fore.RED + "--------------------------------------")
    print("|| Objekt nima svoje trafo postaje. || ")
    print("--------------------------------------" + Fore.WHITE)

seznam_vrst_meritev = model.SEZNAM_VRST_MERITEV

with open("Podatki_z_merjenj.txt", encoding="utf-8") as podatki:
    celotno_besedilo_z_merjenj = (
        podatki.read()
        .replace(", (+)", ",(+)")
        .replace(", (-)", ",(-)")
        .replace(";", "-")
        .replace("\n", " ")
        .replace("Z loop 4W", "ZLOOP 4W")
        .replace("Z line 4W", "ZLINE 4W")
    )

    loceno_besedilo_na_kocke_teksta = celotno_besedilo_z_merjenj.split(
        "Posamezne meritve"
    )

    seznam_datumov_po_vrstnem_redu = model.najdi_po_vrsti_urejen_seznam_datumov(
        celotno_besedilo_z_merjenj
    )

# tukaj se da še polepšati zapis datuma
print(
    Fore.YELLOW + "Meritve so bile opravljene od:",
    seznam_datumov_po_vrstnem_redu[0],
    "do:",
    seznam_datumov_po_vrstnem_redu[-1],
)

seznam_vseh_meritev_brez_poti_na_koncu = []
seznam_ustreznih_poti_do_kock = []

# Tole je treba prenesti v model!


def ustvari_seznam_vseh_meritev():
    seznam_vseh_meritev = []

    for kocka_teksta in loceno_besedilo_na_kocke_teksta:
        slovar_meritev = {i: 0 for i in seznam_vrst_meritev}
        pot_do_druzine_meritev = model.najdi_pot_izven_razreda_Meritev(kocka_teksta)
        idx_poti = kocka_teksta.find("Pot:")
        kocka_teksta = kocka_teksta[:idx_poti]

        for vrsta_meritve in seznam_vrst_meritev:
            if vrsta_meritve in kocka_teksta:
                slovar_meritev[vrsta_meritve] = kocka_teksta.count(vrsta_meritve)

        stevilo_meritev_v_trenutni_kocki = sum(slovar_meritev.values())
        if stevilo_meritev_v_trenutni_kocki == 1:
            # Ločimo primere glede na število meritev v kocki
            if kocka_teksta.count("p//") == 0:
                seznam_vseh_meritev.append(
                    [
                        Meritev.Meritev(
                            # Tukaj je skoraj sigurno nekaj preveč v replaceu
                            kocka_teksta.replace("\n", " ")
                            .replace("\r\n", " ")
                            .strip()
                        )
                    ]
                )
                seznam_ustreznih_poti_do_kock.append(pot_do_druzine_meritev)

        else:
            seznam_indeksov_posameznih_meritev = []
            seznam_vseh_meritev_brez_poti_na_koncu = []
            for key in slovar_meritev:
                seznam_indeksov_posameznih_meritev += [
                    m.start() for m in re.finditer(key, kocka_teksta)
                ]
            seznam_indeksov_posameznih_meritev.sort()
            seznam_vseh_meritev_brez_poti_na_koncu += [
                kocka_teksta[i:j]
                for i, j in zip(
                    seznam_indeksov_posameznih_meritev,
                    seznam_indeksov_posameznih_meritev[1:] + [None],
                )
            ]
            # TODO izboljšaj tole z regexom
            loceno_besedilo_zacasno = []
            for meritev in seznam_vseh_meritev_brez_poti_na_koncu:
                if meritev.count("p//") == 0:
                    loceno_besedilo_zacasno.append(
                        Meritev.Meritev(
                            meritev.replace("\n", " ").replace("\r\n", " ").strip()
                        )
                    )
                # To zna biti malenkost nevarno, ampak se zdi da deluje
                elif meritev.count("p//") > 0 and meritev.count("Z LINE") > 0:
                    loceno_besedilo_zacasno.append(
                        Meritev.Meritev(
                            meritev.replace("\n", " ").replace("\r\n", " ").strip()
                        )
                    )

            if loceno_besedilo_zacasno:
                seznam_vseh_meritev.append(loceno_besedilo_zacasno)
                seznam_ustreznih_poti_do_kock.append(pot_do_druzine_meritev)

    return seznam_vseh_meritev


# seznam_vseh_meritev so vse meritve,
# vsaki kocki lahko priprada 1 ali več meritev
seznam_vseh_meritev = ustvari_seznam_vseh_meritev()
slovar_kock_in_ustreznih_poti = dict(
    zip(range(len(seznam_vseh_meritev)), seznam_ustreznih_poti_do_kock)
)
print(
    "Število vseh meritev:",
    len(seznam_vseh_meritev),
    "\nŠtevilo ustreznih poti do meritev:",
    len(seznam_ustreznih_poti_do_kock),
    "" + Fore.WHITE,
)

VSE_PRIPONE_DATOTEK = ["osnovne", "RCD", "RLOW4", "VARISTOR"]

for pripona in VSE_PRIPONE_DATOTEK:
    with open(
        os.path.join("Csvji", f"csv_za_excel_datoteko_{pripona}.csv"),
        "w",
        encoding="utf-8",
        newline="",
    ) as csvfile:
        csvfile.close()

    excel_delovna_datoteka = load_workbook(
        os.path.join("Templati", f"template_za_{pripona}_meritve.xlsx")
    )
    excel_delovna_datoteka.save(
        os.path.join("Porocila", f"excel_datoteka_{pripona}.xlsx")
    )
    excel_delovna_datoteka.close()

for kocka in seznam_vseh_meritev:
    model.zapisi_kocko_meritev_v_excel(
        kocka, seznam_vseh_meritev, slovar_kock_in_ustreznih_poti
    )

for pripona in VSE_PRIPONE_DATOTEK:
    with open(
        os.path.join("Csvji", f"csv_za_excel_datoteko_{pripona}.csv"),
        "r",
        encoding="utf-8",
        newline="",
    ) as csvfile:
        vrstice = csvfile.readlines()

    excel_delovna_datoteka = load_workbook(
        os.path.join("Porocila", f"excel_datoteka_{pripona}.xlsx")
    )
    excel_delovni_list = excel_delovna_datoteka.active
    dolzina_templata = excel_delovni_list.max_column
    visina_templata = excel_delovni_list.max_row

    sekcija = ""
    seznam_sekcij = []

    for i, vrstica in enumerate(vrstice):
        pot_locena_na_elemente = vrstica.replace("\n", " ").strip().split("//")
        for element in pot_locena_na_elemente:
            if "Sekcija: " in element.strip():
                sekcija = element[
                    element.index("Sekcija:") + len("Sekcija:") :
                ].replace("Sekcija: ", "")

            if sekcija != "" and sekcija not in seznam_sekcij:
                seznam_sekcij.append(sekcija)
                excel_delovni_list.append([f"{sekcija}"])
                excel_delovni_list.merge_cells(
                    start_row=i + visina_templata + len(seznam_sekcij),
                    start_column=1,
                    end_row=i + visina_templata + len(seznam_sekcij),
                    end_column=dolzina_templata,
                )
                top_cell = excel_delovni_list[
                    f"A{i  + visina_templata + len(seznam_sekcij)}"
                ]
                top_cell.alignment = Alignment(horizontal="center", vertical="center")
                top_cell.font = Font(b=True)
                top_cell.fill = PatternFill(
                    start_color="F5C77E", end_color="F5C77E", fill_type="solid"
                )
        excel_delovni_list.append(vrstica.split(";"))

        # avtomatično barvanje je samo v primeru, ko ni VARISTOR
        if pripona not in ["RCD", "VARISTOR"]:
            napake = ""
            str_napake = f'napake = preveri_meje_{pripona}(vrstica.split(";"), trafo=trafo_postaja)'
            if debug_mode:  # Zelo uporabno pri debugganju.
                print(pot_locena_na_elemente)
            exec(str_napake)
            if napake:
                for indeks, barva in napake.items():
                    excel_delovni_list.cell(
                        i + visina_templata + len(seznam_sekcij) + 1, indeks + 1
                    ).fill = PatternFill(
                        start_color=barva, end_color=barva, fill_type="solid"
                    )

    excel_delovna_datoteka.save(
        os.path.join("Porocila", f"excel_datoteka_{pripona}.xlsx")
    )

print("-----------------------------------------------------------------")
