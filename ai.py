import time
from ai_parse import AI_PARSE
from controller import Controller
from kart import Kart
import logging

MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50

logger = logging.getLogger('MariooCarteLogger')

#Just a general AI class that delegates all the work to AI_PARSE

class AI(Controller):
    
    def __init__(self, string, pos_ini, angle_ini):
        super().__init__()
        self.is_ai = True
        self.initial_position = pos_ini
        self.initial_angle = angle_ini
        self.__ai = AI_PARSE(string, pos_ini, angle_ini)
        if AI_PARSE.need_to_map:
            # try:
            self.__ai.parse(False)
            # except Exception:
            #     logger.warn("AI Parsing failed. Trying again in safe mode.")
            #     try:
            #         self.__ai.parse(True)
            #     except:
            #         logger.error("Failed to find correct commands for the Kart. Exiting.")
            #         exit()
            # except KeyboardInterrupt:
            #     logger.error("AI Parsing interrupted by user. Exiting.")
            #     exit()
            # except:
            #     logger.error("Failed to find correct commands for the Kart. Exiting.")
            #     exit()
        else:
            logger.debug("No need to map")

    @property
    def ai(self):
        return self.__ai

    # @property
    # def step(self):
    #     return super().step

    def move(self, string):
        delay = (1./(120.*Kart.nbr_of_karts_()))
        time.sleep(delay)
        logger.debug("Step %i", self.step)
        keys = self.__ai.move(super().step)
        super(AI, self.__class__).step.fset(self, super().step+1)
        return keys
    
    def reset(self, step=0):
        super(AI, self.__class__).step.fset(self, step+1)
    

        