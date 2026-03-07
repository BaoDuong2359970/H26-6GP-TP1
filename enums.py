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