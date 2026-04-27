import tkinter as tk
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
from gpiozero import OutputDevice
from enums import Mode, Moteur
from infos import InfosManager
from azure.iot.device import IoTHubDeviceClient, Message
import json, uuid, time
import mysql.connector

class CapteursManager:

    def __init__(self, app):
        self.app = app

        # Connection  internet hub
        self.conn_str = "HostName=internetobjethub.azure-devices.net;DeviceId=collecteur_temp;SharedAccessKey=qIL8KPAdSPBGenuV15iSpZX62T4K1zHzvGGFy9/SGmY="
        self.client = IoTHubDeviceClient.create_from_connection_string(self.conn_str)
        self.client.connect()
        self.client.on_message_received = self.on_message_received

        #Connection local database 
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="iotdb"
        )

        self.cursor = self.db.cursor()

        # Pins utilisés
        self.DHT_PIN = board.D4
        self.LDR_PIN = 12
        self.TRIG_PIN = 23
        self.ECHO_PIN = 24

        # Moteur pas à pas
        self.motor_pins = (6, 27, 5, 25)
        self.motors = [OutputDevice(pin) for pin in self.motor_pins]
        self.seq = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]

        # Alerts
        self.ALERT_TOLERANCE_PERCENT = 5
        self.ANOMALY_DELAY_SECONDS = 2
        self.deviation_since = None
        self.last_action = "STOP"

        # Réglages moteur
        self.STEP_DELAY = 0.002
        self.STEPS_PER_CYCLE = 40

        self.TOLERANCE_CM = 0.5

        self.AUTO_DISTANCE_CLOSED = 2.1
        self.AUTO_DISTANCE_OPEN = 11.0

        # Manuelle: 2.1 = 0% et 10.5 = 100%
        self.MANUAL_DISTANCE_CLOSED = 2.1
        self.MANUAL_DISTANCE_OPEN = 10.5

        self.LDR_DARK = 5000
        self.LDR_BRIGHT = 50

        self.dht = adafruit_dht.DHT11(self.DHT_PIN, use_pulseio=False)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
        GPIO.output(self.TRIG_PIN, False)

        time.sleep(1)

    def on_message_received(self, message):
        print("Commande reçue:", message.data)

        try:
            data = json.loads(message.data.decode())

            if data["command"] == "open":
                self.app.parent.after(0, lambda: self.move_to_manual_percent(100))

            elif data["command"] == "close":
                self.app.parent.after(0, lambda: self.move_to_manual_percent(0))

            elif data["command"] == "set":
                value = data.get("value", 0)
                self.app.parent.after(0, lambda: self.move_to_manual_percent(value))

        except Exception as e:
            print("Erreur commande:", e)

    def creer_donnees(self):
        frame = tk.Frame(self.app.left_frame, bg="white")
        frame.pack(pady=20)

        tk.Label(frame, text="Température interne ambiante:", font=("Arial", 15, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame, textvariable=self.app.temperature_var, font=("Arial", 15), bg="white").pack(anchor="w")

        tk.Label(frame, text="Intensité lumineuse:", font=("Arial", 15, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame, textvariable=self.app.luminosite_var, font=("Arial", 15), bg="white").pack(anchor="w")

        tk.Label(frame, text="Ouverture automatique:", font=("Arial", 15, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame, textvariable=self.app.ouverture_auto_var, font=("Arial", 15), bg="white").pack(anchor="w")

    def clamp(self, value, vmin, vmax):
        return max(vmin, min(value, vmax))

    def map_value(self, x, in_min, in_max, out_min, out_max):
        if in_max == in_min:
            return out_min
        return out_min + (x - in_min) * (out_max - out_min) / (in_max - in_min)

    def lire_temperature_humidite(self):
        try:
            return self.dht.temperature, self.dht.humidity
        except Exception:
            return None, None

    def lire_luminosite_brute(self):
        count = 0

        GPIO.setup(self.LDR_PIN, GPIO.OUT)
        GPIO.output(self.LDR_PIN, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(self.LDR_PIN, GPIO.IN)

        timeout = time.time() + 0.2
        while GPIO.input(self.LDR_PIN) == GPIO.LOW:
            count += 1
            if time.time() > timeout:
                break

        return count

    def lire_luminosite(self):
        raw = self.lire_luminosite_brute()

        if self.LDR_DARK == self.LDR_BRIGHT:
            return 0.0

        pct = (self.LDR_DARK - raw) * 100.0 / (self.LDR_DARK - self.LDR_BRIGHT)
        return round(self.clamp(pct, 0, 100), 1)

    def lire_distance(self):
        values = []

        for _ in range(5):
            GPIO.output(self.TRIG_PIN, True)
            time.sleep(0.00001)
            GPIO.output(self.TRIG_PIN, False)

            start = time.time()
            end = time.time()

            timeout = time.time() + 0.03
            while GPIO.input(self.ECHO_PIN) == 0:
                start = time.time()
                if start > timeout:
                    return None

            timeout = time.time() + 0.03
            while GPIO.input(self.ECHO_PIN) == 1:
                end = time.time()
                if end > timeout:
                    return None

            distance = (end - start) * 17150
            values.append(distance)
            time.sleep(0.01)

        return round(sum(values) / len(values), 1)

    # MOTEUR
    def set_step(self, step):
        for i in range(4):
            if step[i]:
                self.motors[i].on()
            else:
                self.motors[i].off()

    def motor_off(self):
        self.app.etat_moteur = Moteur.ARRET
        self.app.infos_manager.update_etat_moteur()

        for motor in self.motors:
            motor.off()

    def rotate_open(self):
        self.app.etat_moteur = Moteur.MARCHE
        self.app.infos_manager.update_etat_moteur()

        for cycle in range(self.STEPS_PER_CYCLE):
            for step in self.seq:
                self.set_step(step)
                time.sleep(self.STEP_DELAY)

    def rotate_close(self):
        self.app.etat_moteur = Moteur.MARCHE
        self.app.infos_manager.update_etat_moteur()

        for _ in range(self.STEPS_PER_CYCLE):
            for step in reversed(self.seq):
                self.set_step(step)
                time.sleep(self.STEP_DELAY)

    def control_once(self, target_distance, current_distance):
        if current_distance is None:
            self.motor_off()
            return "STOP"

        if current_distance < target_distance - self.TOLERANCE_CM:
            self.rotate_open()
            self.motor_off()
            return "OPEN"
        elif current_distance > target_distance + self.TOLERANCE_CM:
            self.rotate_close()
            self.motor_off()
            return "CLOSE"
        else:
            self.motor_off()
            return "STOP"

    # ALGO AUTO
    def calculer_ouverture(self, temperature, luminosite):
        k = 0.5
        ouverture = 5 * (temperature - 20)
        ouverture = self.clamp(ouverture, 0, 100)

        if luminosite > 60:
            ouverture = ouverture * (1 - k * (luminosite - 60) / 40)

        return self.clamp(ouverture, 0, 100)

    def percent_to_auto_distance(self, percent):
        return self.AUTO_DISTANCE_CLOSED + (percent / 100.0) * (
            self.AUTO_DISTANCE_OPEN - self.AUTO_DISTANCE_CLOSED
        )

    # ALGO MANUEL
    def percent_to_manual_distance(self, percent):
        percent = self.clamp(percent, 0, 100)
        return self.MANUAL_DISTANCE_CLOSED + (percent / 100.0) * (
            self.MANUAL_DISTANCE_OPEN - self.MANUAL_DISTANCE_CLOSED
        )

    def move_to_manual_percent(self, target_percent):
        target_percent = self.clamp(target_percent, 0, 100)
        target_distance = self.percent_to_manual_distance(target_percent)

        self.app.ouverture_actuelle = target_percent
        self.app.ouverture_var.set(f"{self.app.ouverture_actuelle:.1f} %")
        self.app.dessiner_ouverture(self.app.ouverture_actuelle)

        while True:
            distance = self.lire_distance()

            if distance is None:
                self.motor_off()
                return

            action = self.control_once(target_distance, distance)
            self.last_action = action

            self.app.distance_var.set(f"{distance} cm")
            self.app.ouverture_var.set(f"{self.app.ouverture_actuelle:.1f} %")
            self.app.dessiner_ouverture(self.app.ouverture_actuelle)
            self.app.parent.update_idletasks()

            print("--------------------------------")
            print("Current distance:", distance, "cm")
            print("Target distance :", round(target_distance, 2), "cm")
            print("Motor           :", action)

            if action == "STOP":
                return

            time.sleep(0.1)

    def calculer_pourcentage_ouverture_reelle(self, distance):
        if distance is None:
            return self.app.ouverture_actuelle

        if self.app.mode == Mode.MANUELLE:
            closed = self.MANUAL_DISTANCE_CLOSED
            opened = self.MANUAL_DISTANCE_OPEN
        else:
            closed = self.AUTO_DISTANCE_CLOSED
            opened = self.AUTO_DISTANCE_OPEN

        pct = self.map_value(distance, closed, opened, 0, 100)
        return round(self.clamp(pct, 0, 100), 1)

    def nettoyer(self):
        self.motor_off()
        GPIO.cleanup()

    def update_donnees(self):
        temperature, humidite = self.lire_temperature_humidite()
        luminosite = self.lire_luminosite()
        distance = self.lire_distance()
        status_moteur = "En arrêt"

        # Alerts
        action = self.last_action

        if temperature is not None:
            self.app.temperature_var.set(f"{temperature} °C")
        else:
            self.app.temperature_var.set("-- °C")

        self.app.luminosite_var.set(f"{luminosite:.1f} (0-100)")
        self.app.distance_var.set(f"{distance} cm" if distance is not None else "-- cm")
        self.app.humidite = humidite

        ouverture_reelle = self.calculer_pourcentage_ouverture_reelle(distance)
        self.app.ouverture_reelle = ouverture_reelle

        if self.app.mode == Mode.AUTOMATIQUE and temperature is not None and distance is not None:
            cible = self.calculer_ouverture(temperature, luminosite)
            target_distance = self.percent_to_auto_distance(cible)

            self.app.ouverture_actuelle = cible
            self.app.ouverture_auto_var.set(f"{self.app.ouverture_actuelle:.1f} %")
            
            action = self.control_once(target_distance, distance)
            self.last_action = action

            if action == "OPEN" or action == "CLOSE":
                status_moteur = "En marche"
            else:
                status_moteur = "En arrêt"

            self.gerer_alerte_porte(
                cible,
                ouverture_reelle,
                action
            )
        
        if self.app.mode == Mode.MANUELLE:
            self.gerer_alerte_porte(
                self.app.ouverture_actuelle,
                ouverture_reelle,
                action
            )

        self.app.ouverture_var.set(f"{self.app.ouverture_actuelle:.1f} %")
        self.app.dessiner_ouverture(self.app.ouverture_actuelle)

        data = {
            "id_message": str(uuid.uuid4()),
            "id_objet": "objectId123",
            "date": int(time.time()),
            "status": status_moteur,
            "temperature": temperature,
            "luminosite": luminosite,
            "ouverture_auto": self.app.ouverture_actuelle,
            "mode": self.app.mode.value,
            "ouverture_reelle": ouverture_reelle,
<<<<<<< HEAD
            "distance": distance
=======
            "distance": distance,
            "erreur": "non",
            "avertissement": ""
>>>>>>> 24af00279b4d6a5133830f26c7005cfdb6824056
        }

        msg = Message(json.dumps(data))
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"

        self.client.send_message(msg)
        print("envoyé :", data)

        self.cursor.execute("""
        INSERT INTO data (temperature, luminosite, ouverture, mode, status, date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            temperature,
            luminosite,
            self.app.ouverture_actuelle,
            self.app.mode.value,
            status_moteur,
            int(time.time())
        ))

        self.db.commit()
        self.app.parent.after(300, self.update_donnees)

    def gerer_alerte_porte(self, ouverture_cible, ouverture_reelle, action):
        ecart = abs(ouverture_cible - ouverture_reelle)

        if ecart <= self.ALERT_TOLERANCE_PERCENT:
            self.deviation_since = None
            self.app.cacher_alerte()
            return "non", ""

        if self.deviation_since is None:
            self.deviation_since = time.time()

        anomalie = (
            action in ["OPEN", "CLOSE"]
            and time.time() - self.deviation_since >= self.ANOMALY_DELAY_SECONDS
        )

        message = (
            f"Écart entre l'ouverture calculée ({ouverture_cible:.1f} %) "
            f"et l'ouverture réelle ({ouverture_reelle:.1f} %)."
        )

        if anomalie:
            message += f" La porte est ouverte plus que nécessaire, elle doit être ouverte à {ouverture_cible:.1f}%"

        self.app.afficher_alerte(message, clignote=anomalie)

        return "oui" if anomalie else "non", message