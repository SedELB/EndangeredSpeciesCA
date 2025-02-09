import tkinter as tk
from tkinter import ttk
import pandas as pd

# Charger ton dataframe
df = pd.read_csv('animals.csv', encoding='ISO-8859-1', skiprows=2)
df = df.rename(columns={"Groupe d'espèces" : "Groupe espece"})

# Fonction qui filtre la combobox en fonction de l'entrée de l'utilisateur
def filter_combobox(event):
    search_term = combo.get().lower()
    filtered_items = [item for item in df['Nom commun'] if search_term in str(item).lower()]
    combo['values'] = filtered_items


# Fonction pour gérer la sélection d'un animal
def on_select(event):
    selected_animal = combo.get()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Recherche d'animaux")

# Entrée pour la recherche avec un filtre dynamique
search_label = tk.Label(root, text="Tapez le nom commun d'un animal:")
search_label.pack(pady=10)


# Liaison de l'événement de frappe dans le champ de recherche pour filtrer la combobox


# Combobox pour afficher la liste des noms communs
combo = ttk.Combobox(root, width=20, state="normal")
listeNomsCommuns = df['Nom commun'].tolist()
combo['values'] = listeNomsCommuns  # Ajouter tous les noms communs à la combobox
combo.pack(pady=10)

combo.bind('<KeyRelease>', filter_combobox)
# Lier l'événement de sélection de l'animal dans la combobox
combo.bind('<<ComboboxSelected>>', on_select)

# Démarrer l'interface graphique
root.mainloop()
