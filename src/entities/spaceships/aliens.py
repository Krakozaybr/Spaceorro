from abc import ABC

from src.entities.abstract.abstract import EntityView
from src.entities.spaceships.basic_types import DefaultSpaceship, create_view
from src.entities.teams import Team
from src.utils.image_manager import ImageManager
from src.entities.spaceships.basic_types import TeamMixin


class AliensMixin(TeamMixin, ABC):
    spaceship_team = Team.aliens


class AliensCorvette(DefaultSpaceship, AliensMixin):

    # static fields
    config_name = "aliens_corvette.json"
    start_config_name = "corvette.json"

    def create_view(self) -> EntityView:
        return create_view(ImageManager().get_pic(ImageManager().ALIENS_CORVETTE), self)


class AliensDrone(DefaultSpaceship, AliensMixin):

    # static fields
    config_name = "aliens_drone.json"
    start_config_name = "drone.json"

    def create_view(self) -> EntityView:
        return create_view(ImageManager().get_pic(ImageManager().ALIENS_DRONE), self)


class AliensMothership(DefaultSpaceship, AliensMixin):

    # static fields
    config_name = "aliens_mothership.json"
    start_config_name = "mothership.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().ALIENS_MOTHERSHIP), self
        )
