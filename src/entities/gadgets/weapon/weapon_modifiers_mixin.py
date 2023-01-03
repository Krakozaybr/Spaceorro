from src.entities.basic_entity.basic_spaceship import MasterMixin
from src.entities.modifiers_and_characteristics import WeaponModifiers


class WeaponModifiersMixin(MasterMixin):
    _modifiers: WeaponModifiers

    @property
    def modifiers(self) -> WeaponModifiers:
        if not hasattr(self, "_modifiers"):
            self._modifiers = self.master.weapon_modifiers
        return self._modifiers
