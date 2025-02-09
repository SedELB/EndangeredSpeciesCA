import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import pandas as pd

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Charger les données
df = pd.read_csv('assets/animals.csv', encoding='ISO-8859-1', skiprows=2)
df = df.rename(columns={"Groupe d'espèces": "Groupe espece"})
df = df.rename(columns={"Désignation de la Loi sur les espèces en péril": "Statut"})
df = df.rename(columns={"Données sur les espèces": "funfact"})

def open_animal_info():
    species_name = combo.get()
    if species_name in df["Nom commun"].values:
        animal_info = df[df["Nom commun"] == species_name].iloc[0]

        new_window = tk.Toplevel(root)
        new_window.title("Informations sur l'animal")
        new_window.geometry("500x500")

        info_text = f"""
        Nom scientifique: {animal_info['Nom scientifique']}
        Nom commun: {animal_info['Nom commun']}
        Statut de conservation: {animal_info['Statut']}
        Données sur l'espèce: {animal_info['funfact']}
        """

        label = ttk.Label(new_window, text=info_text, font=("Arial", 12), padding=10, wraplength=400)
        label.pack()

        close_button = ttk.Button(new_window, text="Fermer", command=new_window.destroy)
        close_button.pack(pady=10)
    else:
        print("Animal non trouvé")

def filter_combobox(event):
    search_term = combo.get().lower()
    filtered_items = [item for item in df['Nom commun'] if search_term in str(item).lower()]
    combo['values'] = filtered_items

root = tk.Tk()
root.title("Whispers of the Vanishing")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# Ajouter une image de fond
image = Image.open("assets/PandaHackaton.jpg")
image = image.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
bg_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

label1 = tk.Label(root, text="Whispers of the Vanishing", font=("Algerian", 25, "bold italic"))
label1.pack(pady=100, ipadx=10)

label_texte = tk.Label(root, text="Entrez le nom commun\nou scientifique de l'animal", font=("Consolas", 12, "bold"))
label_texte.pack(pady=10)

combo = ttk.Combobox(root, width=40, state="normal", font=(12))
combo['values'] = df['Nom commun'].tolist()
combo.pack(pady=10, ipady=5)

combo.bind('<KeyRelease>', filter_combobox)

button = tk.Button(root, 
                   text="Search", 
                   command=open_animal_info,  # ✅ Correction ici
                   font=("Consolas", 14, "bold"),
                   fg="white",
                   bg="black",
                   activebackground="darkblue",
                   activeforeground="yellow",
                   padx=20, pady=10,
                   relief="raised",
                   bd=5)
button.pack()

quitbtn = tk.Button(root, 
                   text="Quit", 
                   command=root.quit,
                   font=("Consolas", 14, "bold"),
                   fg="white",
                   bg="black",
                   activebackground="darkblue",
                   activeforeground="yellow",
                   padx=20, pady=10,
                   relief="raised",
                   bd=5)      
quitbtn.pack(pady=10)

root.mainloop()
