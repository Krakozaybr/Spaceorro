from abc import ABC

from src.entities.abstract.abstract import EntityView
from src.entities.spaceships.basic_types import DefaultSpaceship, create_view, TeamMixin
from src.utils.image_manager import ImageManager
from src.entities.teams import Team


class PallariansMixin(TeamMixin, ABC):
    spaceship_team = Team.pallarians


class PallariansCruiser(DefaultSpaceship, PallariansMixin):

    # static fields
    config_name = "pallarians_cruiser.json"
    start_config_name = "cruiser.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().PALLARIANS_CRUISER), self
        )


class PallariansDestroyer(DefaultSpaceship, PallariansMixin):

    # static fields
    config_name = "pallarians_destroyer.json"
    start_config_name = "destroyer.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().PALLARIANS_DESTROYER), self
        )


class PallariansDreadnought(DefaultSpaceship, PallariansMixin):

    # static fields
    config_name = "pallarians_dreadnought.json"
    start_config_name = "dreadnought.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().PALLARIANS_DREADNOUGHT), self
        )


class PallariansMothership(DefaultSpaceship, PallariansMixin):

    # static fields
    config_name = "pallarians_mothership.json"
    start_config_name = "mothership.json"

    def create_view(self) -> EntityView:
        return create_view(
            ImageManager().get_pic(ImageManager().PALLARIANS_MOTHERSHIP), self
        )
