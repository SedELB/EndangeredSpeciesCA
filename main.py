import tkinter as tk
from PIL import Image, ImageTk

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

root = tk.Tk()
root.title("Ma fenêtre Tkinter")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

label1 = tk.Label(root, text="Whispers of the Vanishing", font=("algerian", 25, "bold italic"))
label1.pack(padx=10, pady=50)

image = Image.open("assets/PandaHackaton.jpg")
image = image.resize((int((WINDOW_WIDTH)/2), int((WINDOW_HEIGHT)/2)))
image_pandas_homepage = ImageTk.PhotoImage(image)
label_image = tk.Label(root, image=image_pandas_homepage )
label_image.pack(side="left")

label_texte = tk.Label(root, text="Entrezle nom de l'animal que vous voulez explorer", font=("Consolas", 12))
label_texte.pack(side="left")
zone_texte = tk.Entry(textvariable="allo")
zone_texte.pack()

root.mainloop()
