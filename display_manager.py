from RPLCD.i2c import CharLCD

class DisplayManager:

    def __init__(self, app):

        self.app = app

        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=0x3F,
            port=1,
            cols=16,
            rows=2
        )

        self.page = 0

    def update_display(self):

        try:

            if self.page == 0:

                temp = self.app.temperature_var.get()

                self.lcd.clear()
                self.lcd.write_string(f"Temp:{temp}")

                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string("Greenhouse")

            elif self.page == 1:

                dist = self.app.distance_var.get()

                self.lcd.clear()
                self.lcd.write_string(f"Dist:{dist}")

                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(self.app.mode.value)

            elif self.page == 2:

                openp = self.app.ouverture_var.get()

                self.lcd.clear()
                self.lcd.write_string(f"Open:{openp}")

                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string("Ventilation")

            self.page += 1

            if self.page > 2:
                self.page = 0

        except Exception:
            pass

        self.app.parent.after(2000, self.update_display)
