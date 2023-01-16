from abc import ABC

from src.entities.abstract.abstract import EntityView
from src.entities.spaceships.basic_types import DefaultSpaceship, create_view, TeamMixin
from src.utils.image_manager import ImageManager
from src.entities.teams import Team


class BloodhuntersMixin(TeamMixin, ABC):
    spaceship_team = Team.bloodhunters


class BloodhuntersDrone(DefaultSpaceship, BloodhuntersMixin):

    # static fields
    config_name = "bloodhunters_drone.json"
    start_config_name = "drone.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().BLOODHUNTERS_DRONE), self
        )


class BloodhuntersCorvette(DefaultSpaceship, BloodhuntersMixin):

    # static fields
    config_name = "bloodhunters_corvette.json"
    start_config_name = "corvette.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().BLOODHUNTERS_CORVETTE), self
        )


class BloodhuntersCruiser(DefaultSpaceship, BloodhuntersMixin):

    # static fields
    config_name = "bloodhunters_cruiser.json"
    start_config_name = "cruiser.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().BLOODHUNTERS_CRUISER), self
        )


class BloodhuntersDroneBase(DefaultSpaceship, BloodhuntersMixin):

    # static fields
    config_name = "bloodhunters_drone_base.json"
    start_config_name = "drone_base.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().BLOODHUNTERS_DRONE_BASE), self
        )
