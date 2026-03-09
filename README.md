# H26-6GP-TP1

# Contrôle d’une porte d’aération de serre agricole

Ce projet est un logiciel qui permet de contrôler l’ouverture d’une porte d’aération d’une serre en fonction des conditions ambiantes. Le programme lit la température et la luminosité grâce à différents capteurs, puis ajuste automatiquement l’ouverture de la porte. Il est aussi possible d’utiliser un mode manuel pour choisir directement le pourcentage d’ouverture de la porte.

## Composants nécessaires

Pour utiliser ce logiciel, vous devez avoir les composants suivants :

- Raspberry Pi  
- Capteur de température et d’humidité **DHT11**  
- Capteur de luminosité **LDR**  
- Capteur de distance ultrason **Capteur distance**  
- Moteur pas à pas **28BYJ-48**  
- Driver **ULN2003** pour le moteur pas à pas  
- Écran **LCD**  
- Breadboard  
- Résistances  
- Fils électriques 

## Installation et utilisation

1. Cloner le dépôt sur votre Raspberry Pi.

2. Suivre les schémas électroniques fournis dans le projet afin de connecter correctement tous les composants aux bons GPIO du Raspberry Pi.

3. Une fois tous les branchements faits et le projet installé, lancer le programme avec la commande suivante :

```bash
python3 main.py
