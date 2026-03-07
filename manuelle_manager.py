import tkinter as tk
from enums import Mode


class ManuelleManager:
    def __init__(self, app):
        self.app = app

    def creer_manuelle(self):
        manuelle_frame = tk.Frame(
            self.app.left_frame,
            bd=2,
            relief="solid",
            bg="white",
            padx=10,
            pady=10
        )
        manuelle_frame.pack(pady=10)

        top_row = tk.Frame(manuelle_frame, bg="white")
        top_row.pack(pady=5)

        bottom_row = tk.Frame(manuelle_frame, bg="white")
        bottom_row.pack(pady=10)

        tk.Label(
            top_row,
            text="Manuelle",
            font=("Arial", 15),
            relief="solid",
            bg="white",
            padx=10,
            pady=5
        ).pack(side="left", padx=10)

        self.app.entry_manuelle = tk.Entry(
            top_row,
            textvariable=self.app.manuelle_input_var,
            font=("Arial", 15),
            width=5
        )
        self.app.entry_manuelle.pack(side="left", padx=10)

        tk.Label(
            top_row,
            bg="white",
            text="%",
            font=("Arial", 15)
        ).pack(side="left")

        # Message d'erreur
        self.app.label_erreur_entry = tk.Label(
            manuelle_frame,
            text="",
            fg="red",
            bg="white",
            font=("Arial", 12)
        )
        self.app.label_erreur_entry.pack()

        # Bouttons pour manuelle
        self.app.btn_ouvrir = tk.Button(
            bottom_row,
            text="Ouvrir la porte",
            command=self.ouvrir_porte_manuelle,
            font=("Arial", 12),
            bg="#DAF7DB",
            padx=20,
            pady=5
        )
        self.app.btn_ouvrir.pack(side="left", padx=10)

        self.app.btn_fermer = tk.Button(
            bottom_row,
            text="Fermer la porte",
            command=self.fermer_porte_manuelle,
            font=("Arial", 12),
            bg="#FFDBDF",
            padx=20,
            pady=5
        )
        self.app.btn_fermer.pack(side="left", padx=10)

    def lire_valeur_manuelle(self):
        texte = self.app.manuelle_input_var.get()

        try:
            valeur = float(self.app.manuelle_input_var.get())

            if 0 <= valeur <= 100:
                self.app.label_erreur_entry.config(text="")
                return valeur
            else:
                self.app.label_erreur_entry.config(text="La valeur doit être entre 0 et 100")
            return None

        except ValueError:
            self.app.label_erreur_entry.config(text="Veuillez entrer un nombre valide")
            return None

    def ouvrir_porte_manuelle(self):
        if self.app.mode != Mode.MANUELLE:
            return

        valeur = self.lire_valeur_manuelle()

        if valeur is not None:
            self.app.ouverture_actuelle = valeur
            self.app.ouverture_var.set(f"{self.app.ouverture_actuelle:.1f} %")
            self.app.dessiner_ouverture(self.app.ouverture_actuelle)

    def fermer_porte_manuelle(self):
        if self.app.mode != Mode.MANUELLE:
            return
        
        self.app.label_erreur_entry.config(text="")

        self.app.ouverture_actuelle = 0
        self.app.ouverture_var.set(f"{self.app.ouverture_actuelle:.1f} %")
        self.app.dessiner_ouverture(self.app.ouverture_actuelle)

    # Si pas mode manuelle, disable le entry et les boutons pour manuelle
    def update_controle(self):
        if self.app.mode == Mode.MANUELLE:
            self.app.entry_manuelle.config(state="normal")
            self.app.btn_ouvrir.config(state="normal")
            self.app.btn_fermer.config(state="normal")
        else:
            self.app.entry_manuelle.config(state="disabled")
            self.app.btn_ouvrir.config(state="disabled")
            self.app.btn_fermer.config(state="disabled")