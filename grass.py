import pygame
import track
import logging
from block import Block


logger = logging.getLogger('MariooCarteLogger')


#Class for the grass block
#It also handles the texture loading and track texture saving & displaying.

class Grass(Block):  

    __surface_type = 0.2
    grass_texture = None
    sound = None

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type
        
    def __init__(self, x, y):
        super().__init__(x,y)

        
        pass

    
    def draw(self, screen):
        if (Grass.grass_texture is None):
            Grass.grass_texture = pygame.image.load("textures/grass_five.png").convert()
            Grass.grass_texture = pygame.transform.scale(Grass.grass_texture, (track.BLOCK_SIZE, track.BLOCK_SIZE))
        
        if (Grass.sound is None):
            Grass.sound = pygame.mixer.Sound("sounds/grass.wav")

        if (Block.track_texture is None):
            screen.blit(Grass.grass_texture, self._rect)
            # pygame.draw.rect(screen, self.color, self.rect)    
            pass

        super().draw(screen)


        pass
    
    # A completer