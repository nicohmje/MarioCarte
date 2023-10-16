import track
import pygame

class Checkpoint():  # Vous pouvez ajouter des classes parentes
    surface_type = 0
    color = (50, 50, 0)
    id = -1

    def __init__(self, x, y, id):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.surface_type = 0.02
        self.id = id
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)    
        pass
    
    # A completer