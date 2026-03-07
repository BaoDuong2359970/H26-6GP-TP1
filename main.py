import tkinter as tk
from interface import Application   

racine = tk.Tk()
racine.title("TP1 par Alicia Achour & Elena Duong")
racine.geometry("900x600")
racine.configure(bg="white")

app = Application(racine)
racine.mainloop()