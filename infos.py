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
        ouverture_reelle = getattr(self.app, "ouverture_reelle", None)
        ouverture_cible = self.app.ouverture_actuelle

        if ouverture_reelle is None:
            self.set_etat_moteur(Moteur.ARRET)
        else:
            ecart = ouverture_cible - ouverture_reelle

            if abs(ecart) <= 3:
                self.set_etat_moteur(Moteur.ARRET)
            else:
                self.set_etat_moteur(Moteur.MARCHE)

                if ecart > 0:
                    self.set_direction(Direction.DROITE)
                else:
                    self.set_direction(Direction.GAUCHE)

        self.app.parent.after(1000, self.update_infos)

    def update_etat_moteur(self):
        if self.app.etat_moteur == Moteur.MARCHE:
            self.app.label_moteur_marche.config(bg="#DAF7DB")
            self.app.label_moteur_arret.config(bg="white")
        else:
            self.app.label_moteur_marche.config(bg="white")
            self.app.label_moteur_arret.config(bg="#FFDBDF")

    def set_etat_moteur(self, etat):
        self.app.etat_moteur = etat
        self.update_etat_moteur()

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

    def set_direction(self, direction):
        self.app.direction = direction
        self.update_direction()
