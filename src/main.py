import os.path
import logging
from src.game import Game

LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging_example.txt')
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

if __name__ == "__main__":
    try:
        Game().start()
    except Exception as e:
        logging.exception(e)
