import tkinter as tk
from enum import Enum

class Mode(Enum):
    AUTOMATIQUE = "Automatique"
    MANUELLE = "Manuelle"

class Application:
    def __init__(self, racine):
        self.parent = racine
        self.creer_titre()

        # Données des capteurs
        self.temperature_var = tk.StringVar()
        self.luminosite_var = tk.StringVar()
        self.ouverture_var = tk.StringVar()

        self.creer_donnees()
        self.update_donnees()

        # Mode de la porte
        self.mode = Mode.AUTOMATIQUE # Commence en mode auto
        self.mode_var = tk.StringVar()
        self.mode_var.set(self.mode.value)
        self.creer_mode()

        # Manuelle
        self.manuelle_input_var = tk.StringVar()
        self.manuelle_input_var.set("0")
        self.creer_manuelle()

    # -------- Title frame --------
    def creer_titre(self):
        titre_frame = tk.Frame(self.parent)
        titre_frame.pack(pady=20)

        titre = tk.Label(
            titre_frame,
            text="Contrôle d'une porte d'aération d'une serre",
            font=("Arial", 18, "bold")
        )
        titre.pack()


    # -------- Données des capteurs frame --------
    def creer_donnees(self):
        donnees_frame = tk.Frame(self.parent)
        donnees_frame.pack(pady=20)

        # Température
        temp_row = tk.Frame(donnees_frame)
        temp_row.pack(anchor="w")

        tk.Label(
            temp_row,
            text="Température interne ambiante:",
            font=("Arial", 15, "bold")
        ).pack(side="left")

        tk.Label(
            temp_row,
            textvariable=self.temperature_var,
            font=("Arial", 15)
        ).pack(side="left")


        # Luminosité
        lumi_row = tk.Frame(donnees_frame)
        lumi_row.pack(anchor="w")

        tk.Label(
            lumi_row,
            text="Intensité lumineuse à l'interne:",
            font=("Arial", 15, "bold")
        ).pack(side="left")

        tk.Label(
            lumi_row,
            textvariable=self.luminosite_var,
            font=("Arial", 15)
        ).pack(side="left")


        # Ouverture de la porte
        ouvert_row = tk.Frame(donnees_frame)
        ouvert_row.pack(anchor="w")

        tk.Label(
            ouvert_row,
            text="Ouverture de la porte automatique:",
            font=("Arial", 15, "bold")
        ).pack(side="left")

        tk.Label(
            ouvert_row,
            textvariable=self.ouverture_var,
            font=("Arial", 15)
        ).pack(side="left")


    # -------- Mode de l'app --------
    def creer_mode(self):
        mode_frame = tk.Frame(self.parent)
        mode_frame.pack(pady=10)

        tk.Label(
            mode_frame,
            text="Contrôle :",
            font=("Arial", 15, "bold")
        ).pack(side="left", padx=10)

        tk.Label(
            mode_frame,
            textvariable=self.mode_var,
            font=("Arial", 15),
            relief="solid",
            padx=10,
            pady=5
        ).pack(side="left")

        # Test for the mode button
        tk.Button(
            mode_frame,
            text="Changer mode",
            command=self.switch_mode
        ).pack(padx=10)

    def creer_manuelle(self):
        manuelle_frame = tk.Frame(
            self.parent,
            bd=2,
            relief="solid",
            padx=10,
            pady=10
        )
        manuelle_frame.pack(pady=10)

        top_row = tk.Frame(manuelle_frame)
        top_row.pack(pady=5)

        bottom_row = tk.Frame(manuelle_frame)
        bottom_row.pack(pady=10)

        tk.Label(
            top_row,
            text="Manuelle",
            font=("Arial", 15),
            relief="solid",
            padx=10,
            pady=5
        ).pack(side="left", padx=10)

        tk.Entry(
            top_row,
            textvariable=self.manuelle_input_var,
            font=("Arial", 15),
            width=5
        ).pack(side="left", padx=10)

        tk.Label(
            top_row,
            text="%",
            font=("Arial", 15)
        ).pack(side="left")

        # Bouttons pour manuelle
        tk.Button(
            bottom_row,
            text="Ouvrir la porte",
            command=self.lire_valeur_manuelle,
            font=("Arial", 12),
            bg="#DAF7DB",
            padx=20,
            pady=5
        ).pack(side="left", padx=10)

        tk.Button(
            bottom_row,
            text="Fermer la porte",
            command=self.lire_valeur_manuelle,
            font=("Arial", 12),
            bg="#FFDBDF",
            padx=20,
            pady=5
        ).pack(side="left", padx=10)
        

    def lire_valeur_manuelle(self):
        try:
            valeur = float(self.manuelle_input_var.get())

            if 0 <= valeur <= 100:
                print("valeur manuelle: ", valeur)
                return valeur
            else:
                print("La valeur doit être entre 0 et 100")
                return None
            
        except ValueError:
            print("Entrée invalide")
            return None

    # Changer de mode entre manuelle et auto
    def switch_mode(self):
        if self.mode == Mode.AUTOMATIQUE:
            self.mode = Mode.MANUELLE
        else:
            self.mode = Mode.AUTOMATIQUE
        
        self.mode_var.set(self.mode.value)



    def update_donnees(self):
        temperature = 30 # lire_temperature()
        luminosite = 80 # lite_luminosite()
        ouverture = 37.5 # calculer_ouverture(temperature, luminosite)

        self.temperature_var.set(f"{temperature} C")
        self.luminosite_var.set(f"{luminosite} (0-100)")
        self.ouverture_var.set(f"{ouverture} %")

        # Update à chaque secondes
        self.parent.after(1000, self.update_donnees)

    # -------- Lire les données des capteurs --------
    # def lire_temperature():

    # def lire_luminosite():
    
    # def calculer_ouverture(temperature, luminosite):


if __name__ == "__main__":
    racine = tk.Tk()
    racine.title("TP1 par Alicia Achour & Elena Duong")
    racine.geometry("900x600")

    app = Application(racine)
    racine.mainloop()