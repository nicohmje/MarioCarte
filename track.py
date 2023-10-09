from grass import Grass
from checkpoint import Checkpoint
from boost import Boost
from lava import Lava
from road import Road

import pygame

BLOCK_SIZE = 50
BACKGROUND_COLOR = (0, 0, 0)

class Track(object):
    """
    Classe qui gere le deroulement et l'affichage d'une partie
    
    ===================================== ATTENTION ====================================
    
    VOUS NE DEVEZ PAS MODIFIER LA DEFINITION DE CETTE CLASSE
    
    VOUS DEVEZ TRAVAILLER SUR LES AUTRES FICHIERS ET VEILLER A CE 
    QUE LE CODE QUE VOUS PRODUISEZ SOIT COMPATIBLE AVEC CETTE CLASSE
    
    (vous pouvez eventuellement reorganiser les imports en haut, mais c'est tout)
    
    ====================================================================================
    """
    
    # Ce dictionnaire permet de donner la classe et les parametres d'instanciation
    # correspondant a chaque lettre dans la chaine de caractere decrivant le circuit
    char_to_track_element = {
        'G': {
            'class': Grass,
            'params': []
        },
        'B': {
            'class': Boost,
            'params': []
        },
        'C': {
            'class': Checkpoint,  # le C indique le checkpoint d'id 0
            'params': [0]
        },
        'D': {
            'class': Checkpoint,  # Le D indique le checkpoint d'id 1
            'params': [1]
        },
        'E': {
            'class': Checkpoint,  # etc.
            'params': [2]
        },
        'F': {
            'class': Checkpoint,
            'params': [3]
        },
        'L': {
            'class': Lava,
            'params': []
        },
        'R': {
            'class': Road,
            'params': []
        }
    }
    
    def __init__(self, string, initial_position, initial_angle):
        self.string = string  # La chaine de caractere decrivant le circuit

        # Position et orientation de depart
        self.__initial_position = initial_position
        self.__initial_angle = initial_angle

        # Instanciation des objets composants le circuit
        # Au passage, on peut calculer les dimensions du circuit
        self.track_objects, self.width, self.height = self.parse_string(string)
        
        # On instancie le kart controlle par le player
        self.__karts = []
        

    @property
    def initial_position(self):
        return self.__initial_position
    
    @property
    def initial_angle(self):
        return self.__initial_angle

    @property
    def karts(self):
        return self.__karts

    def add_kart(self, kart):
        self.__karts.append(kart)

    def parse_string(self, string):
        """
        Cette methode instancie les composants et calcule les dimensions du circuit

        :param string: La chaine de caractere decrivant le circuit
        :returns: Un tuple (track_objects, width, height)
            track_objects: tableau d'objets composant le circuit
            width: largeur du circuit
            height: hauteur du circuit
        """
        track_objects = []
        width = 0
        height = 0
        
        # On utilise x et y pour decrire les coordonnees dans la chaine de caractere
        # x indique le numero de colonne
        # y indique le numero de ligne
        x = 0
        y = 0
        for c in string:
            # Pour chaque caractere on ajoute un object a track_objects
            if c in Track.char_to_track_element.keys():
                track_element = Track.char_to_track_element[c]
                track_class = track_element['class']
                track_params = [x, y] + track_element['params']
                track_objects.append(track_class(*track_params))
                x += BLOCK_SIZE
                width += BLOCK_SIZE
            elif c == '\n':
                x = 0
                y += BLOCK_SIZE
                width = 0
                height += BLOCK_SIZE
        height += BLOCK_SIZE
        return track_objects, width, height

    def play(self):
        """
        Cette methode permet de lancer la partie. Si le player est une IA, la partie va se jouer
        toute seule, si c'est un humain, il faut jouer avec le clavier.

        :param string: La chaine de caractere decrivant le circuit
        :returns: Un tuple (track_objects, width, height)
            track_objects: tableau d'objets composant le circuit
            width: largeur du circuit
            height: hauteur du circuit
        """
        # Initialisation de pygame
        pygame.init()

        # Creation de l'ecran
        screen = pygame.display.set_mode((self.width, self.height))

        # On appelle une methode qui doit replacer le kart a sa position initiale
        for kart in self.karts:
            kart.reset(self.initial_position, self.initial_angle)
        
        # Boucle while pour le deroulement de la partie
        running = True
        compteur = 0
        while running:

            # Fermeture de la fenetre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                        
            # On efface tout sur l'ecran
            screen.fill(BACKGROUND_COLOR)

            # On dessine les elements du circuit
            for track_object in self.track_objects:
                track_object.draw(screen)

            for kart in self.karts:
                # On recupere la commande du joueur (humain ou IA)
                keys = kart.controller.move(self.string)
            
                if keys[pygame.K_UP]:
                    kart.forward()
                if keys[pygame.K_DOWN]:
                    kart.backward()
                if keys[pygame.K_LEFT]:
                    kart.turn_left()
                if keys[pygame.K_RIGHT]:
                    kart.turn_right()

                # On met a jour la position et l'orientation du kart
                # Ce calcul peut se baser sur la description du circuit et/ou sur ce qui est affiche a l'ecran
                # A noter que le kart n'est pas encore affiche a l'ecran donc on peut recuperer ce qui se trouve
                # sous le kart facilement
                kart.update_position(self.string, screen)

                # On dessine les karts
                if not kart.has_finished:
                    kart.draw(screen)

            # On regarde si tous les karts ont franchi la ligne d'arrivee
            if all([k.has_finished for k in self.karts]):
                running = False

            # On met a jour l'affichage de pygame
            pygame.display.flip()
            
            # On incremente le compteur
            compteur += 1

        print("Fini en", compteur, "etapes !")

        # On ferme la fenetre a la fin du circuit
        pygame.quit()

        return compteur