#Projet : TerraDynamics
#Auteurs : Baptiste Dieu, Macéo Mestrallet

import GUI_TerraDynamics
import Gestion3D
import tkinter as tk

#Dénission de paramètres globaux afin d'être transmis par la suite
ville = None
resolution, heure = None, None
Flag=None #Indique le type de demande ville ou monde
heure=None

def recup_ville(fenetre):
    global ville
    global Flag
    Flag=1
    ville = GUI_TerraDynamics.lancer_ville(fenetre)

def recup_monde(fenetre):
    global resolution
    global date
    global Flag
    global heure
    Flag=0
    resolution, heure = GUI_TerraDynamics.lancer_monde(fenetre)
    if heure=="Demain":
        heure=24
    else:
        heure=0

#Fait apparaitre une première fenêtre et renvoie à lune des fonction au dessus qui font apparaitres des fenêtres spécifique au type de demande
root = tk.Tk()
root.geometry("600x600")
root.title("TerraDynamics")
root.configure(bg="#33392E")

titre = tk.Label(root, text="TerraDynamics", bg=root.cget("bg"), font=("Arial",18, "bold underline"), fg="White")
titre.pack(pady=(20,10))

explication = tk.Label(root, text="Ce projet vise à permettre la visualisation de données météorologiques sur Terre. Nous proposons actuellement deux possibilité de visualisation, une affichant la température dans une ville donnée (une capitale), l'autre affichant via une échelle de teintes la température sur toute la surface du globe.", bg= root.cget("bg"), font=("Arial", 12), fg="White", wraplength=500)
explication.pack(padx=10,pady=(10,10))

btn = tk.Button(root, text="Sélection ville", font=('Arial', 18), bg="white",fg="black", width=15, height=1, command=lambda: recup_ville(root))
btn.pack(pady=(10,0))

btn = tk.Button(root, text="Sélection monde", font=('Arial', 18), bg="white",fg="black", width=15, height=1, command=lambda: recup_monde(root))
btn.pack(pady=(10,0))

root.mainloop()

if Flag==0:
    Gestion3D.afficher_globe_total(resolution, heure)
elif Flag==1:
    Gestion3D.afficher_globe_ville(ville)

