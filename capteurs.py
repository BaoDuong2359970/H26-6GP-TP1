import tkinter as tk

class CapteursManager:
    def __init__(self, app):
        self.app = app

    def creer_donnees(self):
        donnees_frame = self.app.left_frame
        donnees_frame = tk.Frame(donnees_frame, bg="white")
        donnees_frame.pack(pady=20)

        # Température
        temp_row = tk.Frame(donnees_frame, bg="white")
        temp_row.pack(anchor="w")

        tk.Label(
            temp_row,
            text="Température interne ambiante:",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left")

        tk.Label(
            temp_row,
            textvariable=self.app.temperature_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left")

        # Luminosité
        lumi_row = tk.Frame(donnees_frame, bg="white")
        lumi_row.pack(anchor="w")

        tk.Label(
            lumi_row,
            text="Intensité lumineuse à l'interne:",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left")

        tk.Label(
            lumi_row,
            textvariable=self.app.luminosite_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left")

        # Ouverture
        ouvert_row = tk.Frame(donnees_frame, bg="white")
        ouvert_row.pack(anchor="w")

        tk.Label(
            ouvert_row,
            text="Ouverture de la porte automatique:",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left")

        tk.Label(
            ouvert_row,
            textvariable=self.app.ouverture_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left")

    def calculer_ouverture(self, temperature, luminosite):
        # Délai
        k = 0.5

        # Ouverture basé sur température
        ouverture = 5 * (temperature - 20)
        ouverture = max(0, min(100, ouverture)) # Assurer valeur entre 0% et 100%

        # Ouverture avec luminosité
        if luminosite > 60:
            facteur = 1 - k * (luminosite - 60) / 40
            ouverture *= facteur

        ouverture = max(0, min(100, ouverture))

        return ouverture

    def update_donnees(self):
        temperature = 30
        luminosite = 80

        self.app.temperature_var.set(f"{temperature} °C")
        self.app.luminosite_var.set(f"{luminosite} (0-100)")

        if self.app.mode.name == "AUTOMATIQUE":
            self.app.ouverture_actuelle = self.calculer_ouverture(temperature, luminosite)

        self.app.ouverture_var.set(f"{self.app.ouverture_actuelle:.1f} %")
        self.app.dessiner_ouverture(self.app.ouverture_actuelle)

        self.app.parent.after(1000, self.update_donnees)


    # -------- Lire les données --------
    # def lire_temperature():

    # def lire_luminosite():