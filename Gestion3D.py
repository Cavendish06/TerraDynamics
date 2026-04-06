#Projet : TerraDynamics
#Auteurs : Baptiste Dieu, Macéo Mestrallet
"""
Ce module gère l'affichage graphique de la sphère. 
Ses fonctionnalités incluent:
    - La transformation des poins de latitude et longitude obtenu via l'API en coordonnées carthésienne
    - La création d'un modèle de terre avec texture
    - La gestion de l'affichage selon le type de demande
"""
import pyvista as pv
import numpy as np
import API as ap
import matplotlib.colors as mcolors

colors = [ # Définit un spectre personalisé des couleurs celui-ci est inspiré de météo France
    (-60, "#0a0a2a"),   # noir-violet très froid
    (-50, "#1a0a4a"),
    (-40, "#2b0080"),   # violet foncé
    (-35, "#4b0096"),
    (-30, "#6600b4"),
    (-25, "#8000c8"),   # violet
    (-23, "#a000d0"),
    (-20, "#c000d8"),   # magenta foncé
    (-18, "#d400c8"),
    (-15, "#e600a0"),   # rose
    (-13, "#f00080"),
    (-10, "#0000ff"),   # bleu vif
    (-8,  "#0040ff"),
    (-6,  "#0080ff"),
    (-4,  "#00aaff"),   # bleu clair
    (-2,  "#00ccff"),
    (0,   "#00eeff"),   # cyan
    (2,   "#00ffcc"),
    (4,   "#00ff80"),   # vert-cyan
    (6,   "#00ff40"),
    (8,   "#00ff00"),   # vert
    (10,  "#40ff00"),
    (12,  "#80ff00"),
    (14,  "#aaff00"),   # vert-jaune
    (16,  "#ccff00"),
    (18,  "#eeff00"),
    (20,  "#ffff00"),   # jaune
    (22,  "#ffdd00"),
    (24,  "#ffbb00"),
    (26,  "#ff9900"),   # orange
    (28,  "#ff7700"),
    (30,  "#ff5500"),
    (32,  "#ff3300"),   # orange-rouge
    (34,  "#ff1100"),
    (36,  "#ee0000"),   # rouge
    (38,  "#cc0000"),
    (40,  "#aa0000"),
    (42,  "#880000"),   # rouge foncé
    (44,  "#660000"),
    (46,  "#440000"),
    (48,  "#330000"),
    (50,  "#1a0000"),   # brun très foncé
]

temps = [c[0] for c in colors]
cols  = [c[1] for c in colors]

t_min, t_max = temps[0], temps[-1]
nodes = [(t - t_min) / (t_max - t_min) for t in temps]

cmap = mcolors.LinearSegmentedColormap.from_list(
    "meteo_fr",
    list(zip(nodes, cols))
)

def conversion_en_carth(gridco, rayon=1.01): #Cette fonction convertit des oordonnées géographiques en carthésienne.
    rad=np.radians(gridco)
    lat=rad[:, 0] # toutes les latitudes  en radians
    lon=rad[:, 1] # toutes les longitudes en radians

    gridco = np.c_[
        np.cos(lat)*np.cos(lon)*rayon,   # x
        np.cos(lat)*np.sin(lon)*rayon,   # y
        np.sin(lat)*rayon,   # z
    ]
    return gridco

def _sphere_with_texture_map(radius=1.0, lat_resolution=90, lon_resolution=360): #Création de la sphère
    theta, phi = np.mgrid[0 : np.pi : lat_resolution * 1j, 0 : 2 * np.pi : lon_resolution * 1j]  # type: ignore[misc]
    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)
    sphere = pv.StructuredGrid(x, y, z)
    texture_coords = np.empty((sphere.n_points, 2))
    texture_coords[:, 0] = phi.ravel('F') / phi.max()
    texture_coords[:, 1] = theta[::-1, :].ravel('F') / theta.max()
    sphere.active_texture_coordinates = texture_coords
    return sphere.extract_surface(algorithm=None, pass_pointid=False, pass_cellid=False)

def Terre(radius=1.0, lat_resolution=50, lon_resolution=100): # Génération de la Terre avec sa texture
    return _sphere_with_texture_map(
        radius=radius,
        lat_resolution=lat_resolution,
        lon_resolution=lon_resolution,
    )

def afficher_globe_total(resolution, heure): # Affichage pour une demande des données mondiales
    grid_lat_lon, temp= ap.requete_monde(resolution, heure)
    pv.close_all()
    gridcart= conversion_en_carth(grid_lat_lon)
    nuage=pv.PolyData(gridcart)

    espace=pv.Plotter()
    mesh = Terre()
    mesh.rotate_z(180,inplace=True)
    texture = pv.examples.load_globe_texture()

    espace.add_mesh(mesh, texture=texture)
    espace.add_mesh(nuage, scalars=temp, opacity=0.2, point_size=3, cmap=cmap, clim=[-60, 50])
    espace.show_axes()
    espace.show()

def afficher_globe_ville(ville): # Affichage pour une demande de ville
    grid_lat_lon, temp, donnees=ap.requete_ville(ville)
    gridcart= conversion_en_carth(grid_lat_lon)
    nuage=pv.PolyData(gridcart)
    texte = (
        f"{'Température'}: {donnees['temperature']:.1f} C\n"
        f"{'Humidité'}: {donnees['humidite']:.0f} %\n"
        f"{'Nuages'}: {donnees['nuages']:.0f} %\n"
        f"{'Direction du vent'}: {donnees['vent_direction']:.0f} deg\n"
        f"{'Vitesse du vent'}: {donnees['vent_vitesse']:.1f} km/h\n"
        f"{'Précipitations'}: {donnees['precipitation']:.1f} mm\n"
        f"{'Probabilité pluie'}: {donnees['proba_pluie']:.0f} %\n"
        f"{'Visibilité'}: {donnees['visibilite']:.0f} m"
    )

    espace=pv.Plotter()
    espace.add_text(text=texte,position="upper_right",font_size=11,color="black",font="arial",shadow=True)
    mesh = Terre()
    mesh.rotate_z(180,inplace=True) #Inspace ?
    texture = pv.examples.load_globe_texture()

    espace.add_mesh(mesh, texture=texture)
    espace.add_mesh(nuage, scalars=temp, opacity=1, point_size=11, cmap="RdBu_r",clim=[-15, 40],render_points_as_spheres=True)
    espace.show_axes()
    espace.show()
