import pygame
import numpy as np
import track
import logging

logger = logging.getLogger('MariooCarteLogger')

class Grass():  

    __surface_type = 0.2
    __color = (255, 0, 132)
    nbr_of_grass = 0 

    track_texture = None
    grass_texture = None
    sound = None

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type
        
    def __init__(self, x, y):
        self.__rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.__grass_nbr = np.copy(Grass.nbr_of_grass)
        if (not Grass.nbr_of_grass):
            pass
        Grass.nbr_of_grass += 1
        
        pass
    
    def draw(self, screen):
        if (self.__grass_nbr == 0 and not (Grass.track_texture is None)):
            screen.blit(Grass.track_texture, (0,0))
            return
        
        if (Grass.grass_texture is None):
            Grass.grass_texture = pygame.image.load("textures/grass_five.png").convert()
            Grass.grass_texture = pygame.transform.scale(Grass.grass_texture, (track.BLOCK_SIZE, track.BLOCK_SIZE))

        if (Grass.track_texture is None):
            screen.blit(Grass.grass_texture, self.__rect)
            Grass.sound = pygame.mixer.Sound("sounds/grass.wav")
            # pygame.draw.rect(screen, self.color, self.rect)    
            pass

    
        if (self.__grass_nbr == Grass.nbr_of_grass-1 and Grass.track_texture is None): 
            screen.blit(Grass.grass_texture, self.__rect) 
            #pygame.draw.rect(screen, self.color, self.rect)   
            pygame.image.save(screen, "textures/track.png")
            logger.info("Saved track")
            # time.sleep(0.02)
            Grass.track_texture = pygame.image.load("textures/track.png").convert()
            screen.blit(Grass.track_texture, (0,0))
            self.__color = (255,255,255)
            pass

        pass
    
    # A completer