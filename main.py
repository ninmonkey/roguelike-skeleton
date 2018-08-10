import logging
import os

from app.game import Game
from app.common import get_full_path

# logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.path.join('logs','log.txt'), level=logging.DEBUG)


def main():
    g = Game(root_path=get_full_path(__file__))
    print("""USE_FOG_OF_WAR = {}
TORCH_RADIUS = {}""".format(g.use_fog_of_war, g.torch_radius))
    g.loop()


if __name__ == '__main__':
    main()
    print("To view hotkeys, see Game.handle_input")
    print('Done.')