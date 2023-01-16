from abc import ABC

from src.entities.abstract.abstract import EntityView
from src.entities.spaceships.basic_types import DefaultSpaceship, create_view, TeamMixin
from src.utils.image_manager import ImageManager
from src.entities.teams import Team


class RobotorMixin(TeamMixin, ABC):
    spaceship_team = Team.player


class RobotorDrone(DefaultSpaceship, RobotorMixin):

    # static fields
    config_name = "robotor_drone.json"
    start_config_name = "drone.json"

    def create_view(self) -> EntityView:
        return create_view(ImageManager().get_pic(ImageManager().ROBOTOR_DRONE), self)


class RobotorBattleship(DefaultSpaceship, RobotorMixin):

    # static fields
    config_name = "robotor_battleship.json"
    start_config_name = "battleship.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().ROBOTOR_BATTLESHIP), self
        )


class RobotorMiner(DefaultSpaceship, RobotorMixin):

    # static fields
    config_name = "robotor_miner.json"
    start_config_name = "cruiser.json"

    def create_view(self) -> EntityView:
        return create_view(ImageManager().get_pic(ImageManager().ROBOTOR_MINER), self)


class RobotorMothership(DefaultSpaceship, RobotorMixin):

    # static fields
    config_name = "robotor_mothership.json"
    start_config_name = "mothership.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().ROBOTOR_MOTHERSHIP), self
        )
