import math
import pygame
import time
from radar import AI_PARSE

MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50

class AI():
    
    def __init__(self, string, pos_ini, angle_ini):
        self.kart = None
        self.ai = AI_PARSE(string,pos_ini, angle_ini)
        if (AI_PARSE.need_to_map):
            self.ai.parse()
        self.step = 0

    def reset(self):
        self.step = 0

    def move(self, string):
        self.step += 1
        time.sleep(0.02)
        return self.ai.move(self.step)



    # def move(self, string):
    #     """
    #     Cette methode contient une implementation d'IA tres basique.
    #     L'IA identifie la position du prochain checkpoint et se dirige dans sa direction.

    #     :param string: La chaine de caractere decrivant le circuit
    #     :param screen: L'affichage du jeu
    #     :param position: La position [x, y] actuelle du kart
    #     :param angle: L'angle actuel du kart
    #     :param velocity: La vitesse [vx, vy] actuelle du kart
    #     :param next_checkpoint_id: Un entier indiquant le prochain checkpoint a atteindre
    #     :returns: un tableau de 4 boolean decrivant quelles touches [UP, DOWN, LEFT, RIGHT] activer
    #     """

    #     # =================================================
    #     # D'abord trouver la position du checkpoint
    #     # =================================================
    #     if self.kart.next_checkpoint_id == 0:
    #         char = 'C'
    #     elif self.kart.next_checkpoint_id == 1:
    #         char = 'D'
    #     elif self.kart.next_checkpoint_id == 2:
    #         char = 'E'
    #     elif self.kart.next_checkpoint_id == 3:
    #         char = 'F'

    #     # On utilise x et y pour decrire les coordonnees dans la chaine de caractere
    #     # x indique le numero de colonne
    #     # y indique le numero de ligne
    #     x, y = 0, 0
    #     for c in string:

    #         # Si on trouve le caractere correpsondant au checkpoint, on s'arrete
    #         if c == char:
    #             break

    #         # Si on trouve le caractere de retour a la ligne "\n" on incremente y et on remet x a 0
    #         # Sinon on incremente x
    #         if c == "\n":
    #             y += 1
    #             x = 0
    #         else:
    #             x += 1

    #     next_checkpoint_position = [x * BLOCK_SIZE + .5 * BLOCK_SIZE, y * BLOCK_SIZE + .5 * BLOCK_SIZE]

    #     # =================================================
    #     # Ensuite, trouver l'angle vers le checkpoint
    #     # =================================================
    #     relative_x = next_checkpoint_position[0] - self.kart.position[0]
    #     relative_y = next_checkpoint_position[1] - self.kart.position[1]
        
    #     # On utilise la fonction arctangente pour calculer l'angle du vecteur [relative_x, relative_y]
    #     next_checkpoint_angle = math.atan2(relative_y, relative_x)
        
    #     # L'angle relatif correspond a la rotation que doit faire le kart pour se trouver face au checkpoint
    #     # On applique l'operation (a + pi) % (2*pi) - pi pour obtenir un angle entre -pi et pi
    #     relative_angle = (next_checkpoint_angle - self.kart.angle + math.pi) % (2 * math.pi) - math.pi
        
    #     # =================================================
    #     # Enfin, commander le kart en fonction de l'angle
    #     # =================================================
    #     if relative_angle > MAX_ANGLE_VELOCITY:
    #         # On tourne a droite
    #         command = [False, False, False, True]
    #     elif relative_angle < -MAX_ANGLE_VELOCITY:
    #         # On tourne a gauche
    #         command = [False, False, True, False]
    #     else:
    #         # On avance
    #         command = [True, False, False, False]
            
    #     key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
    #     keys = {key: command[i] for i, key in enumerate(key_list)}
    #     return keys