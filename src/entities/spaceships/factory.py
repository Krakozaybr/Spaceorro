from pymunk import Vec2d

from src.entities.abstract.abstract import EntityFactory
from src.entities.basic_entity.basic_spaceship import BasicSpaceship
from random import choice

from src.entities.spaceships.aliens import *
from src.entities.spaceships.aquamarins import *
from src.entities.spaceships.bloodhunters import *
from src.entities.spaceships.pallarians import *
from src.entities.spaceships.robotors import *


class SpaceshipFactory(EntityFactory):

    spaceships = [
        RobotorDrone,
        RobotorBattleship,
        RobotorMiner,
        RobotorMothership,
        PallariansCruiser,
        PallariansDestroyer,
        PallariansDreadnought,
        PallariansMothership,
        AquamarinsDrone,
        AquamarinsBattleship,
        AquamarinsCruiser,
        AquamarinsDestroyer,
        AquamarinsDreadnought,
        AquamarinsMothership,
        BloodhuntersDrone,
        BloodhuntersCorvette,
        BloodhuntersCruiser,
        BloodhuntersDroneBase,
        AliensCorvette,
        AliensDrone,
        AliensMothership,
    ]

    @classmethod
    def create_entity(cls, pos: Vec2d) -> BasicSpaceship:
        return choice(cls.spaceships).create_default(pos)
