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
            temp = self.app.temperature_var.get()
            dist = self.app.distance_var.get()
            openp = self.app.ouverture_var.get()
            mode = self.app.mode.value
 
            if self.page == 0:
 
                self.lcd.clear()
                self.lcd.write_string(f"Ouverture:{openp}")
 
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(f"Mode:{mode}")
 
            elif self.page == 1:
 
                self.lcd.clear()
                self.lcd.write_string(f"Distance:{dist}")
 
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(f"Temperature:{temp}")
 
            self.page += 1
 
            if self.page > 1:
                self.page = 0
 
        except Exception:
            pass
 
        self.app.parent.after(2000, self.update_display)
 