# MarioCarte

![midjourney](https://github.com/nicohmje/MarioCarte/blob/main/textures/splash_screen.jpg)



# --------------- READ ME ------------------------

# 1. Le fichier Kart.py contient deux booleans TEXT,
#    FINISH_EXIT et SPLASH SCREEN. Le premier 
#    determine l'affichage du meilleur temps pendant 
#    la partie. Le deuxieme definit si on doit quitter 
#    le jeu lorsqu'on arrive au bout de la carte, ou 
#    simplement reset a la position de depart. Finalement
#    le dernier decide de l'affichage ou non de l'ecran
#    d'acceuil (voir 3.) 
#
# 2. L'IA utilise un algorithme A*, et necessite donc 
#    d'un peu de temps pour trouver le chemin ideal. 
#    Ainsi, si l'on modifie le circuit, il faudra 
#    attendre un peu que le chemin et les commandes soient
#    calcules. Le programme enregistre ces donnees et 
#    ne les calcule que si le circuit change. 
#
# 3. Le jeu a un ecran d'acceuil, qui permet de lancer
#    le jeu apres un input (la barre espace). Cet ecran
#    d'acceuil peut etre desacive en mettant SPLASH_SCREEN
#    a False dans kart.py. Cependant, il est tres beau,
#    et le defaut est donc True. 
#
# 4. L'IA fut codee de maniere a etre robuste, et peut
#    donc etre plus lente dans certains scenarios. 
#    Cependant, elle est capable de resoudre des circuits
#    plus compliques. 
#
# 5. Le jeu supporte plusieurs Karts (1 humain + N ai).
#
#   Merci, bon jeu, bonne annee. 
#
#   Benjamin Pineau et Nicolas Hammje (Master SAR)
#
#   mariocarte.nicolashammje.com
