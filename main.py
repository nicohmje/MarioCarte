from track import Track
from ai import AI
from human import Human
from kart import Kart
import logging


logging.basicConfig(level=logging.DEBUG, format='%(filename)s -  %(levelname)s - %(message)s')
logger = logging.getLogger('MariooCarteLogger')


# La chaine de caractere decrivant le terrain

# string = """RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRBRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR
# RRRRRRRRRRRRRRRRRRRRRRRRRR"""


string = """GGGGGGGGGGGGGGGGGGGGGGGGGG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGRRRRG
GFFRRGGGGGGGGGGGGGGGGRRRRG
GLRRRGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGDDDDG
GRRRRRERRRRRGGBRRRRRRRRLLG
GRRRRRERRRRRGGBRRRRRRRRRRG
GLRRRRERRRRRRRBRRRRRRRRRRG
GLLRRRERRRRRRRBRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGGGGGG"""

# string = """GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GRRRRRCRRRRDRRRRRLRERRRRRRRRRRRFG
# GRRRRRCRRRRDRRRRRLRERRRRRLRRRRRFG
# GRRRRRCRRRLDRRRRRRRERRRRRLRRRRRFG
# GRRRRRCRRRLDRRRRRRRERRRRRRRRRRRFG
# GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"""

# string = """GGGGGGGGGGGGGGGGGGGGGGGG
# GRRRRGGGGGGGGGGGGGGGGGGG
# GRRRRGGGGGGGGRGGGGGGGGGG
# GRRRRGGGRRRGGGGGRGGRRRGG
# GRRRRGGGRGRRGRGGRGGRGGGG
# GRRRRGGGRRRRGRGGRRGRRGGG
# GRRRRGGGRGRGGRGGRGGRGGGG
# GBBBBGGGRGRGGRGGRGGRRRRG
# GRRRRGGGRRRGGRGGRGGGGGGG
# GRRRRGGGGGGGGGGGGGGGGGGG
# GRRRRGGGGGGGGGGGGGGGGGGG
# GRRRRRRRRRBRRRRRRRRRRRBG
# GRRRRRRRRRBRRRRRRRRRRRBG
# GRRRRRRRRRBRRRRRRRRRRRBG
# GRRRRRRRRRBRRRRRRRRRRRBG
# GGGGGGGGGGGGGGGGGGGGGGGG"""

# string = """GGGGGGGGGGGGGGGGGGGGGGGG
# GRRRRGRRRRRDBBRRRRGGGGGG
# GRRRRGRRRRRDRRRRRRGGGGGG
# GRRRRGRRRRRDRRRRRRGGGGGG
# GRRRRGRRRRRDRRRRRRGGGGGG
# GRRRRGRRRRGGGGRRRRGGGGGG
# GRRRRGRRRRGGGGRRRRGGGGGG
# GRRRRGRRRRGGGGRRRRGGGGGG
# GRRRRGRRRRGGGGRRRRGGGGGG
# GRRRRGBBBBGGGGEEEEGGGGGG
# GRRRRGRRRRGGGGRRRRGGGGGG
# GRRRRCRRRRGGGGRRRRRRRRFG
# GRRRRCRRRRGGGGRRBRRRRRFG
# GRRRRCRRRRGGGGRRRRRRRRFG
# GRRRRCRRRRGGGGRRRRRRRRFG
# GGGGGGGGGGGGGGGGGGGGGGGG"""


# string = """GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGRGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGGGGGGGGGGRRRRRRGGGGGGGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGGGGGG
# GGGGGGGGGGGRRRRRRRRRRRRGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGG
# GGGGGGGGGGRRRRRRRRRRRRRRRGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGGGG
# GGGGGGGGGRRRRRRRRRRRRRRRRRGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGGG
# GGGGGGGGRRRRRRRRRRRRRRRRRRGGGGGGBBBRRRRRRRRRRRRRRRRRRRRRRRRRRRBBBBRRGGGGGGG
# GGGGGGGRRRRRRRRRRRRRRRRRRRRGGGGRRBBBRRRRRRRRRRRRRRLLRRRRRRRRRRRBBBBBGGGGGGG
# GGGGGGGRRRRRRRRRRRRRRRRRRRRGGRRRRRRBBRRRRRRRRRRRRRLLRRRRRRRRRRRRBBBBBGGGGGG
# GGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRBBRRRRRRRRRRRRLLRRRRRRRRRRRRRRRRRGGGGGG
# GGGGGGRRRRRRRRRRRRRRRRRRRRRRCRRRRRRRRBRRRRRRRRRRRRGRRRRRRRRRRRRRRRRRRGGGGGG
# GGGGGRRRRRRRRRRRRRRRRRRRRRRRCCRRRRRRRRRRRRRRGGGGGGGGGGGGGGGRRRRRRRRRRRGGGGG
# GGGGGRRRRRRRRRRRGGRRRRRRRRRRCCRRRRRRRRRRRRGGGGGGGGGGGGGGGGGGRRRRRRRRRRGGGGG
# GGGGGRRRRRRRRRRGGGRRRRRRRRRRRCRRRRRRRRRRGGGGGGGGGGGGGGGGGGGGRRRRRRRRRRGGGGG
# GGGGRRRRRRRRRRGGGGGRRRRRRRRRRCRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRRGGGGGRRRRRRRRRRCCRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGRRRRRRRRRCCRRRRGGGGGGGGGGGGGGGRRGGGGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGRRRRRRRRRRRRRGGGGGGGGGGRRRRRRRRRRRGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGRRRRRRGGGGGGGGGGGRRRRRRRRRRRRRRRGGGGGRRRRRRRRRRGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGGGBBRRRRRRRRRRRRRRRGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGRBBBBRRRRRRRRRRRRRRRGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGRRRRRBBBRRRRRRRRRRRRRGGGGGGRRRRRRRRRGGGG
# GGGGFFFFFFFFFGGGGGGGGGGGGGGGGGGGGGRRRRRRRBBBRRRRRRRRRRRRGGGGGRRRRRRRRRRGGGG
# GGGGFFFFFFFFFGGGGGGGGGGGGGGGGGGGGRRRRRRRRRBBBRRRRRRRRRRRGGGGGGRRRRRRRRGGGGG
# GGGGRRRRRRRRRRGGGGGGGGGGGGGGGGGRRRRRRRRRRRRBBRRRRRRRRRRRGGGGGGRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGGGGGRRREERRRRRRRRRRRRRRRRRRRRRRGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGGGGRRRREEERRRRRRRRRRRRRRRRRRRRRGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGGRRRRRRREERRRRRRRRRRRRRRRRRRRRRGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRRGGGGGGGGGGGRRRRRRRRREERRRRRRRGGRRRRRRRRRRGGGGGGGRRRRRRRRRGGGGG
# GGGGRRRRRRRRGGGGGGGGGGRRRRRRRRRRREEERRRRGGGRRRRRRRRRRRGGGGGGGRRRRRRRRRGGGGG
# GGGRRRRRRRRRGGGGGGGGRRRRRRRRRRRRRREERRRGGGGRRRRRRRRRRGGGGGGGRRDRRRRRRGGGGGG
# GGGRRRRRRRRRGGGGGBRRRRRRRRRRRRRRRRRRRGGGGGRRRRRRRRRRRGGGGGGRRRDDDRRRRGGGGGG
# GGGRRRRRRRRRGGGBBBBBRRRRRRRRRRRRRRRRGGGGGGRRRRRRRRRRRRRRRRRRRRRDDDRRRGGGGGG
# GGRRRRRRRRRRGRRRRRBBBBRRRRRRRRRRRRGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRDDDRRGGGGGG
# GGRRRRRRRRRRRRRRRRRRBRRRRRRRRRRRRGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRRDDRRGGGGGG
# GGRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRDRGGGGGGG
# GGRRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGG
# GGRRRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRBBRRRRRRRGGGGGGG
# GGRRRRRRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRBBRRRRRRGGGGGGGG
# GGRRRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRRBBRRRRRGGGGGGGGG
# GGRRRRRRRRRRRRRRRRRRRRGGGGGGGGGGGGGGGGGGGGRRRRRRRRRRRRRRRRRBBRGGGGGGGGGGGGG
# GGRRRRRRRRRRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGRRRRRRRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGRRRRRRRRGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG"""

# La position et l'orientation initiale du kart
initial_position = [150., 150.]
initial_angle = 0.

controller_2 =  Human()  # ou AI()
controller = AI(string,initial_position, initial_angle)
"""
==================== ATTENTION =====================
Vous ne devez pas modifier ces quatre lignes de code 
====================================================
"""

kart = Kart(controller)
track = Track(string, initial_position, initial_angle)
track.add_kart(kart)
track.play()