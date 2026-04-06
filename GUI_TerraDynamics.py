#Projet : TerraDynamics
#Auteurs : Baptiste Dieu, Macéo Mestrallet

import tkinter as tk
import re
from datetime import datetime

date_confirmee = None
ville_confirmee = None

capitales = [
        "Kaboul", "Pretoria", "Tirana", "Alger", "Berlin", "Andorre-la-Vieille",
        "Luanda", "Saint-Jean", "Riyad", "Buenos Aires", "Erevan", "Canberra",
        "Vienne", "Bakou", "Nassau", "Manama", "Dacca", "Bridgetown", "Bruxelles",
        "Belmopan", "Porto-Novo", "Thimphou", "Minsk", "Naypyidaw", "Sucre",
        "Sarajevo", "Gaborone", "Brasilia", "Bandar Seri Begawan", "Sofia",
        "Ouagadougou", "Gitega", "Phnom Penh", "Yaoundé", "Ottawa", "Praia",
        "Bangui", "Santiago", "Pékin", "Nicosie", "Bogota", "Moroni", "Brazzaville",
        "Kinshasa", "Pyongyang", "Séoul", "San José", "Yamoussoukro", "Zagreb",
        "La Havane", "Copenhague", "Djibouti", "Roseau", "Le Caire", "Abou Dabi",
        "Quito", "Asmara", "Madrid", "Mbabane", "Tallinn", "Addis-Abeba", "Suva",
        "Helsinki", "Paris", "Libreville", "Banjul", "Tbilissi", "Accra", "Athènes",
        "Saint-Georges", "Guatemala City", "Conakry", "Bissau", "Malabo",
        "Georgetown", "Port-au-Prince", "Tegucigalpa", "Budapest", "New Delhi",
        "Jakarta", "Bagdad", "Téhéran", "Dublin", "Reykjavik", "Jérusalem", "Rome",
        "Kingston", "Tokyo", "Amman", "Astana", "Nairobi", "Bichkek", "Tarawa",
        "Pristina", "Koweït City", "Vientiane", "Maseru", "Riga", "Beyrouth",
        "Monrovia", "Tripoli", "Vaduz", "Vilnius", "Luxembourg", "Skopje",
        "Antananarivo", "Kuala Lumpur", "Lilongwe", "Malé", "Bamako", "La Valette",
        "Rabat", "Majuro", "Port-Louis", "Nouakchott", "Mexico", "Palikir",
        "Chișinău", "Monaco", "Oulan-Bator", "Podgorica", "Maputo", "Windhoek",
        "Yaren", "Katmandou", "Managua", "Niamey", "Abuja", "Oslo", "Wellington",
        "Mascate", "Kampala", "Tachkent", "Islamabad", "Ngerulmud", "Ramallah",
        "Panama City", "Port Moresby", "Asunción", "Amsterdam", "Lima", "Manille",
        "Varsovie", "Lisbonne", "Doha", "Saint-Domingue", "Prague", "Bucarest",
        "Londres", "Moscou", "Kigali", "Basseterre", "Saint-Marin", "Kingstown",
        "Castries", "Honiara", "San Salvador", "Apia", "São Tomé", "Dakar",
        "Belgrade", "Victoria", "Freetown", "Singapour", "Bratislava", "Ljubljana",
        "Mogadiscio", "Khartoum", "Djouba", "Sri Jayawardenepura Kotte", "Stockholm",
        "Berne", "Paramaribo", "Damas", "Douchanbé", "Dodoma", "N'Djamena",
        "Bangkok", "Dili", "Lomé", "Nuku'alofa", "Port of Spain", "Tunis",
        "Achgabat", "Ankara", "Funafuti", "Kiev", "Montevideo", "Port-Vila",
        "Vatican", "Caracas", "Hanoï", "Sanaa", "Lusaka", "Harare"
    ]

lb = None

def verif_date(var, fenetre): # fonction inutile à l'heure actuelle mais garder pour réduire soucis, sera utile pour concours académique
    global date_confirmee
    date_a_verif = var.get()
    if date_a_verif == "":
        date_confirmee = datetime.now().strftime("%Y-%m-%d") # récupère la date d'aujourd'hui
        fenetre.destroy()
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_a_verif):  # vérification que la réponse est au bon format
        annee, mois, jour = map(int, date_a_verif.split("-"))
        try:
            datetime(annee, mois, jour)
            date_confirmee = date_a_verif
            fenetre.destroy()
        except ValueError:
            print("Erreur : date invalide")
    else:
        print("Erreur : format invalide (attendu aaaa-mm-dd)")

def fenetre_monde(): # fonction permettant la configuration pour l'affichage de la vision mondiale
    root = tk.Tk()
    root.geometry("600x500")
    root.configure(bg="#33392E")
    root.title("TerraDynamics")

    titre = tk.Label(root, text="TerraDynamics", bg=root.cget("bg"), font=("Arial",18, "bold underline"), fg="White")
    titre.pack(pady=(20,10))

    texte1 = tk.Label(root, text="Sélectionner la résolution", bg=root.cget("bg"), font=("Arial",12), fg="White")
    texte1.pack(pady=(20,10)) 

    choix_resolution = tk.StringVar(value="0.5")
    menu = tk.OptionMenu(root, choix_resolution, "0.25", "0.5")
    menu.pack(pady=(10,0))

    #fonctionnalité à finir (pour concours académique)
    """
    texte2 = tk.Label(root, text="Saisir la date au format aaaa-mm-jj", bg=root.cget("bg"), font=("Arial",12), fg="White")
    texte2.pack(pady=(20,10))
    """
    date = tk.StringVar()
    """
    saisir_date = tk.Entry(root, textvariable=date, width=12)
    saisir_date.pack(pady=(10,0))
    """

    texte3 = tk.Label(root, text="Choisir la temporalité", bg=root.cget("bg"), font=("Arial",12), fg="White")
    texte3.pack(pady=(20,10))

    choix_heure = tk.StringVar(value="Aujourd'hui")
    menu2 = tk.OptionMenu(root, choix_heure, "Aujourd'hui", "Demain")
    menu2.pack(pady=(10,0))

    btn2 = tk.Button(root, text="CONFIRMER", font=('Arial', 18), bg="white",fg="black", width=12, height=1, command=lambda: verif_date(date, root))
    btn2.pack(pady=(10,0))

    root.mainloop()
    return choix_resolution.get(),choix_heure
    
def chek_clé(event): # fonction permettant de proposer les villes correspondant à la recherche
    valeur = event.widget.get()
    if valeur == '':
        data = capitales
    else:
        data = []
        for item in capitales:
            if item.lower().startswith(valeur.lower()):
                data.append(item)
    update(data)

def update(data): # fonction permettant la mise à jour de la listbox des villes
    lb.delete(0, 'end')
    for item in data:
        lb.insert('end', item)

def selection(event): # fonction permettant de récupérer le nom de la ville sélectionner
    global ville_confirmee
    ville_confirmee = lb.get(lb.curselection())

def fenetre_ville(): # fonction de la fenêtre permettant la sélection de la ville
    global lb
    root = tk.Tk()
    root.geometry("600x500")
    root.configure(bg="#33392E")
    root.title("TerraDynamics")

    titre = tk.Label(root, text="TerraDynamics", bg=root.cget("bg"), font=("Arial",18, "bold underline"), fg="White")
    titre.pack(pady=(20,10))

    e = tk.Entry(root)
    e.pack(pady=(10,0))
    e.bind('<KeyRelease>', chek_clé)

    lb = tk.Listbox(root, height=6)
    lb.pack()
    lb.bind('<<ListboxSelect>>', selection)
    update(capitales)

    btn = tk.Button(root, text="CONFIRMER", font=('Arial', 18), bg="white",fg="black", width=12, height=1, command=lambda: root.destroy())
    btn.pack(pady=(10,0))

    root.mainloop()
    return ville_confirmee

def lancer_ville(fenetre): # fonction de lancement de la fenêtre ville
    fenetre.destroy()
    ville = fenetre_ville()
    return ville

def lancer_monde(fenetre): # fonction de lancement de la fenêtre monde
    fenetre.destroy()
    resolution, heure = fenetre_monde()
    return resolution, heure