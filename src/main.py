from game import Game
from pymunk.vec2d import Vec2d


if __name__ == '__main__':
    # Game().start()
    v = Vec2d(12, 5)
    print(v.normalized())
    print(v.normalized() * ((144 + 25)**0.5))
