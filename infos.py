import tkinter as tk
from enums import Moteur, Direction


class InfosManager:
    def __init__(self, app):
        self.app = app

    def creer_infos(self):
        self.app.infos_frame = tk.Frame(self.app.parent, bg="white")
        self.app.infos_frame.pack(pady=30)

        self.app.left_infos = tk.Frame(self.app.infos_frame, bg="white")
        self.app.left_infos.pack(side="left", padx=30)

        self.app.right_infos = tk.Frame(self.app.infos_frame, bg="white")
        self.app.right_infos.pack(side="left", padx=30)

        # Moteur
        moteur_frame = tk.Frame(self.app.left_infos, bg="white")
        moteur_frame.pack(anchor="w")

        tk.Label(
            moteur_frame,
            text="Moteur :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.app.label_moteur_marche = tk.Label(
            moteur_frame,
            text=Moteur.MARCHE.value,
            font=("Arial", 15),
            bg="white"
        )
        self.app.label_moteur_marche.pack(side="left", padx=5)

        tk.Label(
            moteur_frame,
            text="|",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.app.label_moteur_arret = tk.Label(
            moteur_frame,
            text=Moteur.ARRET.value,
            font=("Arial", 15),
            bg="white"
        )
        self.app.label_moteur_arret.pack(side="left", padx=5)

        # Direction
        direction_frame = tk.Frame(self.app.left_infos, bg="white")
        direction_frame.pack(anchor="w", pady=5)

        tk.Label(
            direction_frame,
            text="Direction :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.app.label_direction_gauche = tk.Label(
            direction_frame,
            text=Direction.GAUCHE.value,
            font=("Arial", 15),
            bg="white"
        )
        self.app.label_direction_gauche.pack(side="left", padx=5)

        tk.Label(
            direction_frame,
            text="|",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.app.label_direction_droite = tk.Label(
            direction_frame,
            text=Direction.DROITE.value,
            font=("Arial", 15),
            bg="white"
        )
        self.app.label_direction_droite.pack(side="left", padx=5)

        # Distance
        distance_frame = tk.Frame(self.app.right_infos, bg="white")
        distance_frame.pack(anchor="w")

        tk.Label(
            distance_frame,
            text="Détecteur de distance :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        tk.Label(
            distance_frame,
            textvariable=self.app.distance_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left", padx=5)

        # Vitesse
        vitesse_frame = tk.Frame(self.app.right_infos, bg="white")
        vitesse_frame.pack(anchor="w", pady=5)

        tk.Label(
            vitesse_frame,
            text="Vitesse :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        tk.Label(
            vitesse_frame,
            textvariable=self.app.vitesse_var,
            font=("Arial", 15),
            bg="white"
        ).pack(side="left", padx=5)

    def update_infos(self):
        distance = 22 # TODO: Remplace par données des senseurs
        vitesse = 20 # TODO: Remplace par données des senseurs

        self.app.distance_var.set(f"{distance} cm")
        self.app.vitesse_var.set(f"{vitesse} tour/min")

        self.app.parent.after(1000, self.update_infos)

    # Gestion des couleurs pour moteur
    def update_etat_moteur(self):
        if self.app.etat_moteur == Moteur.MARCHE:
            self.app.label_moteur_marche.config(bg="#DAF7DB")
            self.app.label_moteur_arret.config(bg="white")
        else:
            self.app.label_moteur_marche.config(bg="white")
            self.app.label_moteur_arret.config(bg="#FFDBDF")

    # Pour utiliser: self.set_etat_moteur(Moteur.MARCHE)
    def set_etat_moteur(self, etat):
        self.app.etat_moteur = etat
        self.update_etat_moteur()

    # Gestion des couleurs pour direction
    def update_direction(self):
        if self.app.etat_moteur == Moteur.ARRET:
            self.app.label_direction_gauche.config(bg="white")
            self.app.label_direction_droite.config(bg="white")

        elif self.app.direction == Direction.GAUCHE:
            self.app.label_direction_gauche.config(bg="#E4E5FF")
            self.app.label_direction_droite.config(bg="white")

        else:
            self.app.label_direction_gauche.config(bg="white")
            self.app.label_direction_droite.config(bg="#E4E5FF")

    # Pour utiliser: self.set_direction(Direction.GAUCHE)
    def set_direction(self, direction):
        self.app.direction = direction
        self.update_direction()