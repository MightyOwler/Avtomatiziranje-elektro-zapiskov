import tkinter as tk
from tkinter import simpledialog


class CustomDialogUstrezenListGledeNaTip(simpledialog.Dialog):
    def __init__(self, parent, lst, **kwargs):
        self.lst = lst
        super().__init__(parent, **kwargs)

    def body(self, master):
        vrednosti = self.lst
        self.vrednost = tk.StringVar()
        self.vrednost.set(vrednosti[0])

        tk.Label(master, text="Izberi ustrezen I_varovalke:").grid(row=3)
        tk.OptionMenu(master, self.vrednost, *vrednosti).grid(row=3, column=1)

        return self.vrednost

    def apply(self):
        try:
            global I_varovalke_stroji_neprekinjenost

            I_varovalke_stroji_neprekinjenost = float(self.vrednost.get())

            root.destroy()
        except ValueError:
            print("Napačne vrednosti")


class CustomDialogElektricnaOmara(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Prevajanje v angleščino:").grid(row=0)
        self.v_anglescino = tk.BooleanVar()
        tk.Checkbutton(master, variable=self.v_anglescino).grid(row=0, column=1)

        tk.Label(master, text="Vnesi spodnjo mejo izolacijske upornosti:").grid(row=1)
        self.spodnja_meja = tk.Entry(master)
        self.spodnja_meja.grid(row=1, column=1)

        tk.Label(master, text="Vnesi zgornjo mejo izolacijske upornosti:").grid(row=2)
        self.zgornja_meja = tk.Entry(master)
        self.zgornja_meja.grid(row=2, column=1)

        return self.v_anglescino, self.spodnja_meja, self.zgornja_meja

    def apply(self):
        try:
            global meja_izolacijske_upornosti_stroji_riso_rdeca
            global meja_izolacijske_upornosti_stroji_riso_oranzna
            global prevedi_v_anglescino

            meja_izolacijske_upornosti_stroji_riso_rdeca = float(
                self.spodnja_meja.get()
            )
            meja_izolacijske_upornosti_stroji_riso_oranzna = float(
                self.zgornja_meja.get()
            )
            prevedi_v_anglescino = bool(self.v_anglescino.get())

            root.destroy()
        except ValueError:
            print("Napačne vrednosti")


class CustomDialogIstalacija(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Select a boolean value for trafo:").grid(row=0)
        self.trafo = tk.BooleanVar()
        tk.Checkbutton(master, variable=self.trafo).grid(row=0, column=1)

        return self.trafo

    def apply(self):
        try:
            global trafo_postaja
            trafo_postaja = self.trafo.get()

            root.destroy()
        except ValueError:
            print("Napačne vrednosti")


class CustomDialogStroj(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Prevajanje v angleščino:").grid(row=0)
        self.v_anglescino = tk.BooleanVar()
        tk.Checkbutton(master, variable=self.v_anglescino).grid(row=0, column=1)

        tip_varovalke_values = ["NV", "gG", "gL", "B", "C", "D", "K"]
        self.tip_varovalke = tk.StringVar()
        self.tip_varovalke.set(tip_varovalke_values[0])

        tk.Label(master, text="Vnesi tip varovalke:").grid(row=3)
        tk.OptionMenu(master, self.tip_varovalke, *tip_varovalke_values).grid(
            row=3, column=1
        )

        t_varovalke_values = [0.1, 0.2, 0.4, 5.0]
        self.t_varovalke = tk.StringVar()
        self.t_varovalke.set(t_varovalke_values[0])

        tk.Label(master, text="Izberi t_varovalke:").grid(row=4)
        tk.OptionMenu(master, self.t_varovalke, *t_varovalke_values).grid(
            row=4, column=1
        )

        tk.Label(master, text="Vnesi spodnjo mejo izolacijske upornosti:").grid(row=5)
        self.spodnja_meja = tk.Entry(master)
        self.spodnja_meja.grid(row=5, column=1)

        tk.Label(master, text="Vnesi zgornjo mejo izolacijske upornosti:").grid(row=6)
        self.zgornja_meja = tk.Entry(master)
        self.zgornja_meja.grid(row=6, column=1)

        napetost_dotika_values = [15, 25, 50]
        self.napetost_dotika = tk.StringVar()
        self.napetost_dotika.set(napetost_dotika_values[0])

        tk.Label(master, text="Vnesi napetost dotika:").grid(row=7)
        tk.OptionMenu(master, self.napetost_dotika, *napetost_dotika_values).grid(
            row=7, column=1
        )
        return self.v_anglescino, self.t_varovalke

    def apply(self):
        try:
            global t_varovalke_stroji_neprekinjenost
            global tip_varovalke_stroji_neprekinjenost
            global tip_varovalke_stroji_neprekinjenost
            global prevedi_v_anglescino
            global meja_izolacijske_upornosti_stroji_riso_rdeca
            global meja_izolacijske_upornosti_stroji_riso_oranzna
            global napetost_dotika

            meja_izolacijske_upornosti_stroji_riso_rdeca = float(
                self.spodnja_meja.get()
            )
            meja_izolacijske_upornosti_stroji_riso_oranzna = float(
                self.zgornja_meja.get()
            )

            napetost_dotika = int(self.napetost_dotika.get())

            t_varovalke_stroji_neprekinjenost = float(self.t_varovalke.get())
            tip_varovalke_stroji_neprekinjenost = self.tip_varovalke.get()

            prevedi_v_anglescino = bool(self.v_anglescino.get())

            ustrezen_list_NVgGgL = (
                [
                    2,
                    4,
                    6,
                    10,
                    16,
                    20,
                    25,
                    32,
                    35,
                    40,
                    50,
                    63,
                    80,
                    100,
                    125,
                    160,
                    200,
                    224,
                    250,
                    315,
                    355,
                    400,
                    500,
                    560,
                    630,
                ]
                if t_varovalke_stroji_neprekinjenost == 0.1
                else [
                    2,
                    4,
                    6,
                    10,
                    16,
                    20,
                    25,
                    32,
                    35,
                    40,
                    50,
                    63,
                    80,
                    100,
                    125,
                    160,
                    200,
                    224,
                    250,
                    315,
                    355,
                    400,
                    500,
                    560,
                    630,
                    710,
                    800,
                    1000,
                    1250,
                ]
            )

            match tip_varovalke_stroji_neprekinjenost:
                case "NV" | "gG" | "gL":
                    CustomDialogUstrezenListGledeNaTip(
                        root,
                        ustrezen_list_NVgGgL,
                    )
                case "B" | "C" | "D":
                    CustomDialogUstrezenListGledeNaTip(
                        root,
                        [2, 4, 6, 10, 16, 20, 25, 32, 35, 40, 50, 63],
                    )
                case "K":
                    CustomDialogUstrezenListGledeNaTip(
                        root,
                        [
                            0.5,
                            1.0,
                            1.6,
                            2.0,
                            4.0,
                            6.0,
                            10.0,
                            13.0,
                            15.0,
                            16.0,
                            20.0,
                            25.0,
                            32.0,
                        ],
                    )

            root.destroy()
        except ValueError:
            print("Napačne vrednosti")


def vnesi_vrsto_meritev():
    vrsta_merjenj = str(option_var.get())

    global vrsta_stroja
    vrsta_stroja = vrsta_merjenj

    if vrsta_merjenj == "električna omara":
        CustomDialogElektricnaOmara(root)
    elif vrsta_merjenj == "inštalacija":
        CustomDialogIstalacija(root)
    elif vrsta_merjenj == "stroj":
        CustomDialogStroj(root)

    root.destroy()


# Create the main application window
root = tk.Tk()
root.title("Input Program")

# Create and pack the widgets
options = ["električna omara", "inštalacija", "stroj", "strelovod"]

option_var = tk.StringVar()
option_var.set(options[0])

option_menu = tk.OptionMenu(root, option_var, *options)
option_menu.pack()

button_submit = tk.Button(root, text="V redu", command=vnesi_vrsto_meritev)
button_submit.pack()

# Start the main event loop
root.mainloop()
