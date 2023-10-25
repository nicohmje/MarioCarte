import pygame
import numpy as np
import track


class Grass():  # Vous pouvez ajouter des classes parentes

    surface_type = 0.2
    color = (150,196,132)
    nbr_of_grass = 0 

    texture_image = None
        
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.grass_nbr = np.copy(Grass.nbr_of_grass)
        if (not Grass.nbr_of_grass):
            pass
        Grass.nbr_of_grass += 1
        
        pass
    
    def draw(self, screen):
        if (self.grass_nbr == 0 and not (Grass.texture_image is None)):
            screen.blit(Grass.texture_image, (0,0))
            return
        
        elif (self.grass_nbr == Grass.nbr_of_grass-1 and Grass.texture_image is None):
            pygame.draw.rect(screen, self.color, self.rect)    
            print("saved track")
            #time.sleep(0.02)
            pygame.image.save(screen, "track.png")
            Grass.texture_image = pygame.image.load("track.png").convert()
            screen.blit(Grass.texture_image, (0,0))
            self.color = (255,255,255)
            pass
        elif (Grass.texture_image is None):
            pygame.draw.rect(screen, self.color, self.rect)    
            pass

        pass
    
    # A completer