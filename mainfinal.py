import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import pandas as pd
from pygbif import species
from pygbif import occurrences
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import contextily as ctx

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
global index
index = 0


df = pd.read_csv('animals.csv', encoding='ISO-8859-1', skiprows=2)
df = df.rename(columns={"Groupe d'espèces": "Groupe espece"})
df = df.rename(columns={"Désignation de la Loi sur les espèces en péril": "Statut"})
df = df.rename(columns={"Données sur les espèces": "funfact"})


def obtenir_carte(index):
    nom_scientifique = df['Nom scientifique'].iloc[index]
    
    taxon = species.name_backbone(name=nom_scientifique)
    taxon_id = taxon.get("usageKey", None)
    
    if not taxon_id:
        print(f"Taxon pour {nom_scientifique} non trouvé.")
        return
    
    obs = occurrences.search(taxonKey=taxon_id, country="CA", limit=100)
    
    df_observations = pd.DataFrame(obs["results"])
    
    if df_observations.empty:
        messagebox.showinfo("Aucune observation", f"Aucune observation trouvée pour {nom_scientifique}.")
        return
    
    geometry = [Point(xy) for xy in zip(df_observations['decimalLongitude'], df_observations['decimalLatitude'])]
    
    gdf = gpd.GeoDataFrame(df_observations, geometry=geometry, crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.5e7, -0.5e7)
    ax.set_ylim(5e6, 1.2e7)
    
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=4)
    gdf.plot(ax=ax, marker='o', markersize=50, alpha=0.7, color='red')
    ax.set_title(f"Observations de {nom_scientifique} au Canada")
    ax.set_axis_off()
    plt.show()


def open_animal_info():
    global index
    species_name = combo.get()
    if species_name in df["Nom commun"].values:
        animal_info = df[df["Nom commun"] == species_name].iloc[0]
        index = df[df["Nom commun"] == species_name].index[0]

        new_window = tk.Toplevel(root)
        new_window.title("Informations sur l'animal")
        new_window.geometry("500x400")

        frame = ttk.Frame(new_window, padding=20)
        frame.pack(expand=True)

        NStext = f"""Nom scientifique: {animal_info['Nom scientifique']}"""
        NCtext = f"""Nom commun: {animal_info['Nom commun']}"""
        StatusText = f"""Statut de conservation: {animal_info['Statut']}"""
        DataText = f"""Données sur l'espèce: {animal_info['funfact']}"""
        SourceText = f"""Source: Gouvernement du Canada"""

        ttk.Label(frame, text=NStext, font=("Arial", 12, "bold")).pack(pady=5)
        ttk.Label(frame, text=NCtext, font=("Arial", 12)).pack(pady=5)
        ttk.Label(frame, text=StatusText, font=("Arial", 12, "italic")).pack(pady=5)
        ttk.Label(frame, text=DataText, font=("Arial", 11), wraplength=450, justify="center").pack(pady=10)
        ttk.Label(frame, text=SourceText, font=("Arial", 10, "italic")).pack(pady=5)

        ttk.Button(frame, text="Fermer", command=new_window.destroy).pack(pady=10)
        ttk.Button(frame, text="Voir la carte", command=lambda: obtenir_carte(index)).pack(pady=10)
    else:
        print("Animal non trouvé")

def filter_combobox(event):
    search_term = combo.get().lower()
    if search_term:
        filtered_items = [item for item in df['Nom commun'] if search_term in str(item).lower()]
        combo['values'] = filtered_items
    else:
        combo['values'] = df['Nom commun'].dropna().tolist()

root = tk.Tk()
root.title("Whispers of the Vanishing")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")


image = Image.open("PandaHackaton.jpg")
image = image.resize((WINDOW_WIDTH, WINDOW_HEIGHT))
bg_image = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

label1 = tk.Label(root, text="Whispers of the Vanishing", font=("Algerian", 25, "bold italic"))
label1.pack(pady=100, ipadx=10)

label_texte = tk.Label(root, text="Entrez le nom commun de l'animal", font=("Consolas", 12, "bold"))
label_texte.pack(pady=10)


combo = ttk.Combobox(root, width=40, font=(12))
combo['values'] = df['Nom commun'].tolist()
combo.pack(pady=10, ipady=5)


combo.bind('<KeyRelease>', filter_combobox)

searchbtn = tk.Button(root, 
                   text="Search", 
                   command=open_animal_info,
                   font=("Consolas", 14, "bold"),
                   fg="white",
                   bg="black",
                   activebackground="darkblue",
                   activeforeground="yellow",
                   padx=20, pady=10,
                   relief="raised",
                   bd=5)
searchbtn.pack()

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