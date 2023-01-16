from abc import ABC

from src.entities.abstract.abstract import EntityView
from src.entities.spaceships.basic_types import DefaultSpaceship, create_view, TeamMixin
from src.entities.teams import Team
from src.utils.image_manager import ImageManager


class AquamarinsMixin(TeamMixin, ABC):
    spaceship_team = Team.aquamarins


class AquamarinsDrone(DefaultSpaceship, AquamarinsMixin):

    # static fields
    config_name = "aquamarins_drone.json"
    start_config_name = "drone.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().AQUAMARINS_DRONE), self
        )


class AquamarinsBattleship(DefaultSpaceship, AquamarinsMixin):

    # static fields
    config_name = "aquamarins_battleship.json"
    start_config_name = "battleship.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().AQUAMARINS_BATTLESHIP), self
        )


class AquamarinsCruiser(DefaultSpaceship, AquamarinsMixin):

    # static fields
    config_name = "aquamarins_cruiser.json"
    start_config_name = "cruiser.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().AQUAMARINS_CRUISER), self
        )


class AquamarinsDestroyer(DefaultSpaceship, AquamarinsMixin):

    # static fields
    config_name = "aquamarins_destroyer.json"
    start_config_name = "destroyer.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().AQUAMARINS_DESTROYER), self
        )


class AquamarinsDreadnought(DefaultSpaceship, AquamarinsMixin):

    # static fields
    config_name = "aquamarins_dreadnought.json"
    start_config_name = "dreadnought.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().AQUAMARINS_DREADNOUGHT), self
        )


class AquamarinsMothership(DefaultSpaceship, AquamarinsMixin):

    # static fields
    config_name = "aquamarins_mothership.json"
    start_config_name = "mothership.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().AQUAMARINS_MOTHERSHIP), self
        )
