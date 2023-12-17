import pygame
from block import Block




class Road(Block):  # Vous pouvez ajouter des classes parentes
    __surface_type = 0.02
    __color = (33, 25, 48)
    sound = None

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y):
        super().__init__(x,y)
        pass
    
    def draw(self, screen):

        if (Block.track_texture is None):
            pygame.draw.rect(screen, Road.__color, self._rect)  

        super().draw(screen)
        pass
    
    # A completer