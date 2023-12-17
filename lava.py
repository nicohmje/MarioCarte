import pygame
from block import Block
import track


#Class for the lava block

class Lava(Block):  # Vous pouvez ajouter des classes parentes
    __surface_type = 0.02
    __color = (159, 45, 32)
    sound = None
    Lava_texture = None

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y):

        super().__init__(x,y)
        pass
    
    def draw(self, screen):
        if (Lava.sound is None):
            Lava.sound = pygame.mixer.Sound("sounds/lava.wav")

        if (Lava.Lava_texture is None):
            Lava.Lava_texture = pygame.image.load("textures/lava.png").convert()
            Lava.Lava_texture = pygame.transform.scale(Lava.Lava_texture, (track.BLOCK_SIZE, track.BLOCK_SIZE))
        

        if (Block.track_texture is None):
            screen.blit(Lava.Lava_texture, self.rect)
        super().draw(screen)
        
        pass
    
    # A completer