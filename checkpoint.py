import pygame
from road import Road
from block import Block
import track


#Class for the checkpoint block

class Checkpoint(Block):  # Vous pouvez ajouter des classes parentes

    __surface_type = Road.surface_type_()
    __color = (255, 184, 104)
    __nbr_of_checkpoints = 0
    sound = None
    finish_texture = []

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y, id):

        self.id = id
        if id>Checkpoint.__nbr_of_checkpoints:
            Checkpoint.__nbr_of_checkpoints = id
        super().__init__(x, y)

        pass
    

    def draw(self, screen):

        if (Checkpoint.sound is None):
            Checkpoint.sound = pygame.mixer.Sound("sounds/checkpoint.wav")

        if (not len(Checkpoint.finish_texture)):
            Checkpoint.finish_texture.append(pygame.image.load("textures/checkpoint1.png").convert())
            Checkpoint.finish_texture[-1] = pygame.transform.scale(Checkpoint.finish_texture[-1], (track.BLOCK_SIZE, track.BLOCK_SIZE))

            Checkpoint.finish_texture.append(pygame.image.load("textures/checkpoint2.png").convert())
            Checkpoint.finish_texture[-1] = pygame.transform.scale(Checkpoint.finish_texture[-1], (track.BLOCK_SIZE, track.BLOCK_SIZE))

            Checkpoint.finish_texture.append(pygame.image.load("textures/checkpoint3.png").convert())
            Checkpoint.finish_texture[-1] = pygame.transform.scale(Checkpoint.finish_texture[-1], (track.BLOCK_SIZE, track.BLOCK_SIZE))

            Checkpoint.finish_texture.append(pygame.image.load("textures/Finish.png").convert())
            Checkpoint.finish_texture[-1] = pygame.transform.scale(Checkpoint.finish_texture[-1], (track.BLOCK_SIZE, track.BLOCK_SIZE))


        if (Block.track_texture is None):
            match self.id:
                case Checkpoint.__nbr_of_checkpoints:
                    screen.blit(Checkpoint.finish_texture[-1], self.rect)
                case 0:
                    screen.blit(Checkpoint.finish_texture[0], self.rect)
                case 1:
                    screen.blit(Checkpoint.finish_texture[1], self.rect)
                case 2: 
                    screen.blit(Checkpoint.finish_texture[2], self.rect)
                case _:
                    pygame.draw.rect(screen, self.__color, self.rect) 

        super().draw(screen)

        pass    
    # A completer