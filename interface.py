import tkinter as tk

from enums import Mode, Moteur, Direction
from capteurs import CapteursManager
from mode_manager import ModeManager
from manuelle_manager import ManuelleManager
from infos import InfosManager
from display_manager import DisplayManager


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

        # Variables
        self.temperature_var = tk.StringVar()
        self.luminosite_var = tk.StringVar()
        self.ouverture_var = tk.StringVar()
        self.ouverture_actuelle = 0.0
        self.ouverture_reelle = 0.0
        self.humidite = None

        self.distance_var = tk.StringVar()
        self.manuelle_input_var = tk.StringVar(value="0")

        # Enums
        self.mode = Mode.AUTOMATIQUE
        self.mode_var = tk.StringVar(value=self.mode.value)

        self.etat_moteur = Moteur.ARRET
        self.direction = Direction.GAUCHE

        # Managers
        self.capteurs_manager = CapteursManager(self)
        self.mode_manager = ModeManager(self)
        self.manuelle_manager = ManuelleManager(self)
        self.infos_manager = InfosManager(self)
        self.display_manager = DisplayManager(self)

        # Interface
        self.capteurs_manager.creer_donnees()
        self.mode_manager.creer_mode()
        self.mode_manager.creer_mode_boutons()
        self.manuelle_manager.creer_manuelle()
        self.creer_ouverture_visuelle()
        self.infos_manager.creer_infos()

        self.mode_manager.switch_mode(self.mode)
        self.infos_manager.update_etat_moteur()
        self.infos_manager.update_direction()

        # Updates
        self.capteurs_manager.update_donnees()
        self.infos_manager.update_infos()
        self.display_manager.update_display()

    def creer_titre(self):
        titre = tk.Label(
            self.parent,
            text="Contrôle d'une porte d'aération d'une serre",
            font=("Arial", 18, "bold"),
            bg="white"
        )
        titre.pack(pady=20)

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

        x1, y1 = 30, 20
        x2, y2 = 110, 200

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
            top = y1 + margin + i * hauteur_par_barre
            bottom = top + hauteur_par_barre

            if i < barres_remplies:
                couleur = "#C4C6F9"
            else:
                couleur = "#E8E8E8"

            self.canvas_porte.create_rectangle(
                x1 + 5,
                top + 2,
                x2 - 5,
                bottom - 2,
                fill=couleur,
                outline=""
            )
