import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import pandas as pd

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
global search_term
search_term = ""



df = pd.read_csv('assets/animals.csv', encoding='ISO-8859-1', skiprows=2)
df = df.rename(columns={"Groupe d'espèces" : "Groupe espece"})

def filter_combobox(event):
    global search_term
    search_term = combo.get().lower()
    filtered_items = [item for item in df['Nom commun'] if search_term in str(item).lower()]
    combo['values'] = filtered_items

def on_select(event):
    global search_term
    search_term = combo.get().lower()
    filtered_items = [item for item in df['Nom commun'] if search_term in str(item).lower()]
    combo['values'] = filtered_items
    

root = tk.Tk()
root.title("Whispers of the Vanishing")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

image = Image.open("assets/PandaHackaton.jpg")
image = image.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
bg_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

label1 = tk.Label(root, text="Whispers of the Vanishing", font=("algerian", 25, "bold italic"), )
label1.pack(pady=100, ipadx=10)

label_texte = tk.Label(root, text="""Entrez le nom commun
ou scientifique de l'animal""", font=("Consolas", 12, "bold"))
label_texte.pack(pady=10)

combo = ttk.Combobox(root, width=40, state="normal", font=(12))
listeNomsCommuns = df['Nom commun'].tolist()
combo['values'] = listeNomsCommuns
combo.pack(pady=10, ipady=10)

combo.bind('<KeyRelease>', filter_combobox)
combo.bind('<<ComboboxSelected>>', on_select)




root.mainloop()
