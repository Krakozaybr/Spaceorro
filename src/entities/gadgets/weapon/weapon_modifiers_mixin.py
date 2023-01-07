from src.entities.basic_entity.basic_spaceship import SpaceshipMixin
from src.entities.modifiers_and_characteristics import WeaponModifiers


class WeaponModifiersMixin(SpaceshipMixin):
    _modifiers: WeaponModifiers

    @property
    def modifiers(self) -> WeaponModifiers:
        if not hasattr(self, "_modifiers"):
            self._modifiers = self.spaceship.weapon_modifiers
        return self._modifiers
