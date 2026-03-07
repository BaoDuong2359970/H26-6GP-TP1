# Function pour limiter ouverture de la porte entre 0% et 100%
def limiter(ouverture):
    if ouverture < 0:
        return 0
    if ouverture > 100:
        return 100
    return ouverture


# Retardement pour luminosité
k = 0.5

# Entrée des données
Temp = float(input("Entrez le température (°C): "))
Lumi = float(input("Entrez la luminosité (%): "))

# Calcul température (par prof)
# 20C = 0%
# 40C = 100%
Ouverture = 5 * (Temp - 20) # chaque degré au-dessus de 20 ajoute 5%

# Limiter entre 0 et 100 après température
Ouverture = limiter(Ouverture)


# Calcul luminosité (seul si > 60%)
if Lumi > 60:
    facteur = 1 - k * (Lumi - 60) / 40 #formule par prof
    Ouverture = Ouverture * facteur #formule final par prof

# Limiter entre 0 et 100 après luminosité
Ouverture = limiter(Ouverture)

# Résultat (2 chiffres après virgule)
print(f"Ouverture de la porte: {Ouverture:.2f} %")