import pygame
import time
import logging


logger = logging.getLogger('MariooCarteLogger')

def splash_screen(screen, texture, started):
    logger.info("Started")
    dimensions = screen.get_size()
    screen = pygame.display.set_mode((1300,647))
    while (not started):
        screen.blit(texture, (0,0))
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            screen = pygame.display.set_mode(dimensions)
            return True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            return False
        pygame.display.flip()
        time.sleep(1./30.)


def countdown(screen, texture, started):
    logger.info("Started")
    dimensions = screen.get_size()
    screen = pygame.display.set_mode((1300,647))
    while (not started):
        screen.blit(texture, (0,0))
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            screen = pygame.display.set_mode(dimensions)
            return True
        pygame.display.flip()
        time.sleep(1./30.)
     
def get_key():
        time.sleep(0.02)
        return pygame.key.get_pressed()

    

