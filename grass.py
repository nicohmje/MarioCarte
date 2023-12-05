import pygame
import numpy as np
import track
import logging

logger = logging.getLogger('MariooCarteLogger')

class Grass():  

    surface_type = 0.2
    color = (0, 147, 132)
    nbr_of_grass = 0 

    track_texture = None
    grass_texture = None
    sound = None
        
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.grass_nbr = np.copy(Grass.nbr_of_grass)
        if (not Grass.nbr_of_grass):
            pass
        Grass.nbr_of_grass += 1
        
        pass
    
    def draw(self, screen):
        if (self.grass_nbr == 0 and not (Grass.track_texture is None)):

            screen.blit(Grass.track_texture, (0,0))
            return
        
        if (self.grass_texture is None):
            Grass.grass_texture = pygame.image.load("textures/grass_five.png").convert()
            Grass.grass_texture = pygame.transform.scale(Grass.grass_texture, (track.BLOCK_SIZE, track.BLOCK_SIZE))

        if (Grass.track_texture is None):
            screen.blit(Grass.grass_texture, self.rect)
            Grass.sound = pygame.mixer.Sound("sounds/grass.wav")
            # pygame.draw.rect(screen, self.color, self.rect)    
            pass

    
        if (self.grass_nbr == Grass.nbr_of_grass-1 and Grass.track_texture is None): 
            screen.blit(Grass.grass_texture, self.rect) 
            pygame.draw.rect(screen, self.color, self.rect)    
            logger.info("Saved track")
            # time.sleep(0.02)
            pygame.image.save(screen, "track.png")
            Grass.track_texture = pygame.image.load("track.png").convert()
            screen.blit(Grass.track_texture, (0,0))
            self.color = (255,255,255)
            pass

        

        pass
    
    # A completer