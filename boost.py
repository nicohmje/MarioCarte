import pygame
from block import Block
import track

#Class for the boost block


class Boost(Block):  # Vous pouvez ajouter des classes parentes
    __surface_type = 0.02
    __color = (149, 40, 143)
    sound = None

    Boost_texture = None


    @classmethod    
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y):

        super().__init__(x,y)
        pass
    
    def draw(self, screen):

        if (Boost.sound is None):
            Boost.sound = pygame.mixer.Sound("sounds/boost.wav")

        if (Boost.Boost_texture is None):
            Boost.Boost_texture = pygame.image.load("textures/boost.png").convert_alpha()
            Boost.Boost_texture = pygame.transform.scale(Boost.Boost_texture, (track.BLOCK_SIZE, track.BLOCK_SIZE))
        

        if (Block.track_texture is None):
            pygame.draw.rect(screen, (33, 25, 48), self._rect)  
            screen.blit(Boost.Boost_texture, self._rect)

        super().draw(screen)
        
        pass