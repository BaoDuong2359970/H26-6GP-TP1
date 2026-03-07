import tkinter as tk
from enum import Enum

class Mode(Enum):
    AUTOMATIQUE = "Automatique"
    MANUELLE = "Manuelle"

class Moteur(Enum):
    MARCHE = "En marche"
    ARRET = "En arrêt"

class Direction(Enum):
    GAUCHE = "Gauche"
    DROITE = "Droite"

class Application:
    def __init__(self, racine):
        self.parent = racine
        self.creer_titre()

        self.main_frame = tk.Frame(self.parent, bg="white")
        self.main_frame.pack()

        self.left_frame = tk.Frame(self.main_frame, bg="white")
        self.left_frame.pack(side="left", padx=20)

        self.right_frame = tk.Frame(self.main_frame, bg="white")
        self.right_frame.pack(side="left", padx=20)

        # Données des capteurs
        self.temperature_var = tk.StringVar()
        self.luminosite_var = tk.StringVar()
        self.ouverture_var = tk.StringVar()
        self.ouverture_actuelle = 0.0

        # Informations
        self.etat_moteur = Moteur.ARRET
        self.direction = Direction.GAUCHE
        self.distance_var = tk.StringVar()
        self.vitesse_var = tk.StringVar()

        self.creer_donnees()

        # Mode de la porte
        self.mode = Mode.AUTOMATIQUE # Commence en mode auto
        self.mode_var = tk.StringVar()
        self.mode_var.set(self.mode.value)
        self.creer_mode()
        self.creer_mode_boutons()

        # Manuelle
        self.manuelle_input_var = tk.StringVar()
        self.manuelle_input_var.set("0")
        self.creer_manuelle()
        self.switch_mode(self.mode)

        # Dessin de la porte
        self.creer_ouverture_visuelle()
        self.update_donnees()

        # Infos
        self.creer_infos()
        self.update_etat_moteur()
        self.update_direction()
        self.update_infos()


    # -------- Title frame --------
    def creer_titre(self):
        titre = tk.Label(
            self.parent,
            text="Contrôle d'une porte d'aération d'une serre",
            font=("Arial", 18, "bold"),
            bg="white"
        )
        titre.pack(pady=20)


    # -------- Données des capteurs frame --------
    def creer_donnees(self):
        donnees_frame = tk.Frame(self.left_frame, bg="white")
        donnees_frame.pack(pady=20)

        # Température
        temp_row = tk.Frame(donnees_frame)
        temp_row.pack(anchor="w")

        tk.Label(
            temp_row,
            text="Température interne ambiante:",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left")

        tk.Label(
            temp_row,
            textvariable=self.temperature_var,
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
            textvariable=self.luminosite_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left")


        # Ouverture de la porte
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
            textvariable=self.ouverture_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left")


    # -------- Mode de l'app --------
    def creer_mode(self):
        mode_frame = tk.Frame(self.left_frame, bg="white")
        mode_frame.pack(pady=10)

        tk.Label(
            mode_frame,
            text="Contrôle :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=10)

        tk.Label(
            mode_frame,
            textvariable=self.mode_var,
            font=("Arial", 15),
            relief="solid",
            padx=10,
            pady=5,
            bg="white"
        ).pack(side="left")


    def creer_mode_boutons(self):
        mode_boutons_frame = tk.Frame(self.right_frame, bg="white")
        mode_boutons_frame.pack(pady=10)

        tk.Label(
            mode_boutons_frame,
            text="Mode :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.btn_manuelle = tk.Button(
            mode_boutons_frame,
            text="Manuelle",
            font=("Arial", 12, "bold"),
            command=lambda: self.switch_mode(Mode.MANUELLE),
            bg="white"
        )
        self.btn_manuelle.pack(side="left", padx=5)

        tk.Label(
            mode_boutons_frame,
            text="|",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.btn_automatique = tk.Button(
            mode_boutons_frame,
            text="Automatique",
            font=("Arial", 12, "bold"),
            command=lambda: self.switch_mode(Mode.AUTOMATIQUE),
            bg="white"
        )
        self.btn_automatique.pack(side="left", padx=5)


    # -------- Section Manuelle --------
    def creer_manuelle(self):
        manuelle_frame = tk.Frame(
            self.left_frame,
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

        self.entry_manuelle = tk.Entry(
            top_row,
            textvariable=self.manuelle_input_var,
            font=("Arial", 15),
            width=5
        )
        self.entry_manuelle.pack(side="left", padx=10)

        tk.Label(
            top_row,
            bg="white",
            text="%",
            font=("Arial", 15)
        ).pack(side="left")

        # Bouttons pour manuelle
        self.btn_ouvrir = tk.Button(
            bottom_row,
            text="Ouvrir la porte",
            command=self.ouvrir_porte_manuelle,
            font=("Arial", 12),
            bg="#DAF7DB",
            padx=20,
            pady=5
        )
        self.btn_ouvrir.pack(side="left", padx=10)

        self.btn_fermer = tk.Button(
            bottom_row,
            text="Fermer la porte",
            command=self.fermer_porte_manuelle,
            font=("Arial", 12),
            bg="#FFDBDF",
            padx=20,
            pady=5
        )
        self.btn_fermer.pack(side="left", padx=10)
        
    def ouvrir_porte_manuelle(self):
        if self.mode != Mode.MANUELLE:
            return
        
        valeur = self.lire_valeur_manuelle()
        if valeur is not None:
            self.ouverture_actuelle = valeur
            self.ouverture_var.set(f"{self.ouverture_actuelle:.1f} %")
            self.dessiner_ouverture(self.ouverture_actuelle)


    def fermer_porte_manuelle(self):
        if self.mode != Mode.MANUELLE:
            return
        
        self.ouverture_actuelle = 0
        self.ouverture_var.set(f"{self.ouverture_actuelle:.1f} %")
        self.dessiner_ouverture(self.ouverture_actuelle)


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
        
    # Si pas mode manuelle, disable le entry et les boutons pour manuelle
    def update_controle(self):
        if self.mode == Mode.MANUELLE:
            self.entry_manuelle.config(state="normal")
            self.btn_ouvrir.config(state="normal")
            self.btn_fermer.config(state="normal")
        else:
            self.entry_manuelle.config(state="disabled")
            self.btn_ouvrir.config(state="disabled")
            self.btn_fermer.config(state="disabled")

    # Changer de mode entre manuelle et auto
    def switch_mode(self, mode):
        self.mode = mode
        self.mode_var.set(mode.value)

        if mode == Mode.MANUELLE:
            self.btn_manuelle.config(bg="#E4E5FF")
            self.btn_automatique.config(bg="#F4F4F4")

        else:
            self.btn_automatique.config(bg="#E4E5FF")
            self.btn_manuelle.config(bg="#F4F4F4")

        self.update_controle()

    # -------- Données des capteurs --------
    def update_donnees(self):
        temperature = 30 # lire_temperature()
        luminosite = 80 # lite_luminosite()

        self.temperature_var.set(f"{temperature} C")
        self.luminosite_var.set(f"{luminosite} (0-100)")

        if self.mode == Mode.AUTOMATIQUE:
            ouverture = self.calculer_ouverture(temperature, luminosite)

        self.ouverture_var.set(f"{self.ouverture_actuelle:.1f} %")
        self.dessiner_ouverture(self.ouverture_actuelle)

        # Update à chaque secondes
        self.parent.after(1000, self.update_donnees)

    def calculer_ouverture(self, temperature, luminosite):
        # Délai
        k = 0.5

        # Ouverture basé sur température
        ouverture = 5 * (temperature - 20)
        ouverture = max(0, min(100, ouverture)) # Assurer valeur entre 0% et 100%

        # Ouverture avec luminosité
        if luminosite > 60:
            facteur = 1 - k * (luminosite - 60) / 40
            ouverture = ouverture * facteur

        ouverture = max(0, min(100, ouverture))

        return ouverture

    # -------- Lire les données --------
    # def lire_temperature():

    # def lire_luminosite():
    
    # def calculer_ouverture(temperature, luminosite):

    def creer_infos(self):
        self.infos_frame = tk.Frame(self.parent, bg="white")
        self.infos_frame.pack(pady=30)

        self.left_infos = tk.Frame(self.infos_frame, bg="white")
        self.left_infos.pack(side="left", padx=30)

        self.right_infos = tk.Frame(self.infos_frame, bg="white")
        self.right_infos.pack(side="left", padx=30)

        # Moteur
        moteur_frame = tk.Frame(self.left_infos, bg="white")
        moteur_frame.pack(anchor="w")

        tk.Label(
            moteur_frame,
            text="Moteur :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.label_moteur_marche = tk.Label(
            moteur_frame,
            text=Moteur.MARCHE.value,
            font=("Arial", 15),
            bg="white"
        )
        self.label_moteur_marche.pack(side="left", padx=5)

        tk.Label(
            moteur_frame,
            text="|",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.label_moteur_arret = tk.Label(
            moteur_frame,
            text=Moteur.ARRET.value,
            font=("Arial", 15),
            bg="white"
        )
        self.label_moteur_arret.pack(side="left", padx=5)

        # Direction
        direction_frame = tk.Frame(self.left_infos, bg="white")
        direction_frame.pack(anchor="w", pady=5)

        tk.Label(
            direction_frame,
            text="Direction :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.label_direction_gauche = tk.Label(
            direction_frame,
            text=Direction.GAUCHE.value,
            font=("Arial", 15),
            bg="white"
        )
        self.label_direction_gauche.pack(side="left", padx=5)

        tk.Label(
            direction_frame,
            text="|",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.label_direction_droite = tk.Label(
            direction_frame,
            text=Direction.DROITE.value,
            font=("Arial", 15),
            bg="white"
        )
        self.label_direction_droite.pack(side="left", padx=5)

        # Distance
        distance_frame = tk.Frame(self.right_infos, bg="white")
        distance_frame.pack(anchor="w")

        tk.Label(
            distance_frame,
            text="Détecteur de distance :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        tk.Label(
            distance_frame,
            textvariable=self.distance_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left", padx=5)

        # Vitesse
        vitesse_frame = tk.Frame(self.right_infos, bg="white")
        vitesse_frame.pack(anchor="w", pady=5)

        tk.Label(
            vitesse_frame,
            text="Vitesse :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        tk.Label(
            vitesse_frame,
            textvariable=self.vitesse_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left", padx=5)

    # === DISTANCE & VITESSE ===
    def update_infos(self):
        distance = 22 # lire_distance()
        vitesse = 20 # lire_vitesse()

        self.distance_var.set(f"{distance} cm")
        self.vitesse_var.set(f"{vitesse} tour/min")

        # Update à chaque secondes
        self.parent.after(1000, self.update_infos)


    # === ETAT MOTEUR ===
    def update_etat_moteur(self):
        # En Marche
        if self.etat_moteur == Moteur.MARCHE:
            self.label_moteur_marche.config(bg="#DAF7DB")
            self.label_moteur_arret.config(bg="white")
        # En Arrêt
        else:
            self.label_moteur_marche.config(bg="white")
            self.label_moteur_arret.config(bg="#FFDBDF")

    # Pour utiliser: self.set_etat_moteur(Moteur.MARCHE)
    def set_etat_moteur(self, etat):
        self.etat_moteur = etat
        self.update_etat_moteur()


    # === DIRECTION ===
    def update_direction(self):
        if self.etat_moteur == Moteur.ARRET:
            self.label_direction_gauche.config(bg="white")
            self.label_direction_droite.config(bg="white")
            
        # Gauche
        elif self.direction == Direction.GAUCHE:
            self.label_direction_gauche.config(bg="#E4E5FF")
            self.label_direction_droite.config(bg="white")
        # Droite
        else:
            self.label_direction_gauche.config(bg="white")
            self.label_direction_droite.config(bg="#E4E5FF")

    # Pour utiliser: self.set_direction(Direction.GAUCHE)
    def set_direction(self, direction):
        self.direction = direction
        self.update_direction()

    # def lire_distance(self):

    # def lire_vitesse(self):


    # ------------------- Dessin de la porte -------------------
    def creer_ouverture_visuelle(self):
        self.canvas_porte = tk.Canvas(
            self.right_frame,
            width=150,
            height=210,
            bg="white",
            highlightthickness=0
        )
        self.canvas_porte.pack(pady=10)

        ouverture_frame = tk.Frame(self.right_frame, bg="white")
        ouverture_frame.pack()

        tk.Label(
            ouverture_frame,
            text="Ouverture : ",
            bg="white",
            font=("Arial", 18, "bold")
        ).pack(side="left")

        tk.Label(
            ouverture_frame,
            textvariable=self.ouverture_var,
            font=("Arial", 18),
            bg="white"
        ).pack(side="left")


    def dessiner_ouverture(self, pourcentage):
        self.canvas_porte.delete("all")

        pourcentage = max(0, min(100, pourcentage))

        # Coordonnées du rectangle de la porte
        x1, y1 = 30, 20 # top left
        x2, y2 = 110, 200 # bottom right

        # Dessiner la bordure
        self.canvas_porte.create_rectangle(
            x1, y1, x2, y2,
            outline="black",
            width=3
        )

        nb_sections = 10
        margin = 5

        hauteur_utilisable = (y2 - y1) - (2 * margin)
        barres_remplies = round((pourcentage / 100) * nb_sections)

        hauteur_par_barre = hauteur_utilisable / nb_sections

        for i in range(nb_sections):
            top = y1 + margin + i * hauteur_par_barre # start of the bar (top of door + margin + position)
            bottom = top + hauteur_par_barre # bottom of the bar

            if i < barres_remplies:
                couleur = "#C4C6F9"
            else:
                couleur = "#E8E8E8"

            self.canvas_porte.create_rectangle(
                x1 + 5, # left
                top + 2, # top
                x2 - 5, # right
                bottom -2, # bottom
                fill=couleur,
                outline=""
            )



if __name__ == "__main__":
    racine = tk.Tk()
    racine.title("TP1 par Alicia Achour & Elena Duong")
    racine.geometry("900x600")
    racine.configure(bg="white")

    app = Application(racine)
    racine.mainloop()