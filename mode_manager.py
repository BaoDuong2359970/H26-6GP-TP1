import tkinter as tk
from enums import Mode, Moteur

class ModeManager:
    def __init__(self, app):
        self.app = app

    # En haut de la section manuelle
    def creer_mode(self):
        mode_frame = tk.Frame(self.app.left_frame, bg="white")
        mode_frame.pack(pady=10)

        tk.Label(
            mode_frame,
            text="Contrôle :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=10)

        tk.Label(
            mode_frame,
            textvariable=self.app.mode_var,
            font=("Arial", 15),
            relief="solid",
            padx=10,
            pady=5,
            bg="white"
        ).pack(side="left")

    # En haut de l'image de l'ouverture
    def creer_mode_boutons(self):
        mode_boutons_frame = tk.Frame(self.app.right_frame, bg="white")
        mode_boutons_frame.pack(pady=10)

        tk.Label(
            mode_boutons_frame,
            text="Mode :",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.app.btn_manuelle = tk.Button(
            mode_boutons_frame,
            text="Manuelle",
            font=("Arial", 12, "bold"),
            command=lambda: self.switch_mode(Mode.MANUELLE),
            bg="white"
        )
        self.app.btn_manuelle.pack(side="left", padx=5)

        tk.Label(
            mode_boutons_frame,
            text="|",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side="left", padx=5)

        self.app.btn_automatique = tk.Button(
            mode_boutons_frame,
            text="Automatique",
            font=("Arial", 12, "bold"),
            command=lambda: self.switch_mode(Mode.AUTOMATIQUE),
            bg="white"
        )
        self.app.btn_automatique.pack(side="left", padx=5)

    # Changer de mode entre manuelle et auto
    def switch_mode(self, mode):
        # Arrêter le moteur quand on change de mode temporairement
        self.app.etat_moteur = Moteur.ARRET
        self.app.infos_manager.update_etat_moteur()

        self.app.mode = mode
        self.app.mode_var.set(mode.value)

        if mode == Mode.MANUELLE:
            self.app.btn_manuelle.config(bg="#E4E5FF")
            self.app.btn_automatique.config(bg="#F4F4F4")
        else:
            self.app.btn_automatique.config(bg="#E4E5FF")
            self.app.btn_manuelle.config(bg="#F4F4F4")

        self.app.manuelle_manager.update_controle()