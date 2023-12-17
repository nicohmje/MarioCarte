from abc import abstractmethod
import pygame
import track
import logging

logger = logging.getLogger('MariooCarteLogger')

class Block():

    nbr_of_blocks = 0
    track_texture = None

    # @property
    # def block_id(self):
    #     return self._block_id
    
    def __init__(self,x,y) -> None:
        self._rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.__block_id = Block.nbr_of_blocks
        Block.nbr_of_blocks += 1
        pass

    @property
    @abstractmethod
    def surface_type_(self) -> float:
        pass

    def draw(self, screen) -> None:
        if (self.__block_id == 0 and not (Block.track_texture is None)):
            screen.blit(Block.track_texture, (0,0))
            return
        
        if (self.__block_id == Block.nbr_of_blocks-1 and Block.track_texture is None):
            pygame.image.save(screen, "textures/track.png")
            Block.track_texture = pygame.image.load("textures/track.png").convert()
            logger.info("Saved track image")
            pass
        pass