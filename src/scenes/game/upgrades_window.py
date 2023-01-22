from typing import Sequence, Tuple, Callable, Optional, Dict, Union

import pygame
from pygame_gui import UIManager
from pygame_gui.core import UIElement
from pygame_gui.elements import UIWindow, UIPanel, UITextBox, UIButton, UILabel, UIImage

from src.resources import Resources, Resource
from src.settings import W, H

from src.entities.upgrade_system import SpaceshipUpgradeSystem, MinerUpgradeSystem
from src.utils.signal import SignalFieldMixin, Signal


class FieldBlock(UIPanel, SignalFieldMixin):
    active: bool
    upgrade_signal = Signal()

    CURRENT_LEVEL_SIZE = 40, 40
    TITLE_SIZE = 120, 40
    BTN_SIZE = 80, 30

    def __init__(
        self,
        relative_rect: pygame.Rect,
        parent: "UpgradesBlock",
        name: str,
        getter: Callable[[], str],
        upgrade: Callable,
        anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
        manager: Optional[UIManager] = None,
    ):
        UIPanel.__init__(
            self, relative_rect, container=parent, anchors=anchors, manager=manager
        )
        SignalFieldMixin.__init__(self)
        self.active = True
        self.title = UILabel(
            text=name,
            relative_rect=pygame.Rect(0, 0, *self.TITLE_SIZE),
            container=self,
            anchors={"centery": "centery"},
            manager=manager,
        )
        self.getter = getter
        self.upgrade = upgrade
        self.current = UILabel(
            text=getter(),
            relative_rect=pygame.Rect(0, 0, *self.CURRENT_LEVEL_SIZE),
            container=self,
            anchors={"left_target": self.title, "centery": "centery"},
            manager=manager,
        )
        btn_w, btn_h = self.BTN_SIZE
        self.btn = UIButton(
            text="Upgrade",
            relative_rect=pygame.Rect(-btn_w - 2, 0, *self.BTN_SIZE),
            container=self,
            anchors={"right": "right", "centery": "centery"},
            manager=manager,
        )

    def update(self, time_delta: float):
        super().update(time_delta)
        if self.active:
            self.btn.enable()
        else:
            self.btn.disable()
        if self.btn.check_pressed():
            self.upgrade()
            self.current.set_text(self.getter())
            self.upgrade_signal.emit()


class ResourceView(UIPanel):
    COUNT_SIZE = 50, 20

    def __init__(
        self,
        parent: "CostBlock",
        relative_rect: pygame.Rect,
        resource: Resource,
        anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
        manager: Optional[UIManager] = None,
    ):
        super().__init__(
            relative_rect, anchors=anchors, container=parent, manager=manager
        )
        img = resource.resource_type.get_image(30, 30)
        self.img = UIImage(
            relative_rect=img.get_rect(),
            image_surface=img,
            container=self,
            manager=manager,
        )
        self.count = UILabel(
            text=str(resource.quantity),
            relative_rect=pygame.Rect(0, 0, *self.COUNT_SIZE),
            anchors={"left": "left", "right": "right", "top_target": self.img},
            container=self,
            manager=manager,
        )

    def update_resource(self, resource: Resource):
        self.count.set_text(str(resource.quantity))


class CostBlock(UIPanel):
    RESOURCE_SIZE = 40, 50

    def __init__(
        self,
        relative_rect: pygame.Rect,
        parent: "UpgradesBlock",
        get_cost: Callable,
        anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
        manager: Optional[UIManager] = None,
    ):
        super().__init__(
            relative_rect, anchors=anchors, container=parent, manager=manager
        )
        self.get_cost = get_cost
        resources = get_cost()
        target = UILabel(
            text="Cost:",
            relative_rect=pygame.Rect(0, 0, 40, 60),
            container=self,
            manager=manager,
        )
        self.resources_display = dict()
        for resource, rt in resources:
            if resource.quantity:
                anchors = (
                    {"left_target": target} if target is not None else {"left": "left"}
                )
                target = self.resources_display[rt] = ResourceView(
                    relative_rect=pygame.Rect(0, 0, *self.RESOURCE_SIZE),
                    resource=resource,
                    anchors=anchors,
                    parent=self,
                    manager=manager,
                )

    def update_resources(self):
        resources = self.get_cost()
        for resource, rt in resources:
            if rt in self.resources_display:
                self.resources_display[rt].update_resource(resource)


class UpgradesBlock(UIPanel):
    W = 300
    H = 300
    MARGIN = 10
    PADDING = 10
    TITLE_HEIGHT = 30

    COST_BLOCK_SIZE = 280, 60
    CAN_UPGRADE_SIZE = 280, 30
    FIELD_SIZE = 280, 40

    def __init__(
        self,
        title: str,
        parent: "UpgradesWindow",
        column: int,
        row: int,
        fields: Sequence[
            Tuple[str, Callable[[], str], Callable]
        ],  # [(field name, getter, upgrade)]
        get_cost: Callable[[], Resources],
        can_upgrade: Callable[[], bool],
        anchors: Optional[Dict[str, Union[str, UIElement]]] = None,
        manager: Optional[UIManager] = None,
    ):
        super().__init__(
            pygame.Rect(self.W * column, self.H * row, self.W, self.H),
            container=parent,
            anchors=anchors,
            manager=manager,
        )
        self.can_upgrade = can_upgrade
        self.title = UITextBox(
            title,
            pygame.Rect(
                self.PADDING, self.PADDING, self.W - self.PADDING * 2, self.TITLE_HEIGHT
            ),
            container=self,
            manager=manager,
        )
        self.cost_view = CostBlock(
            parent=self,
            relative_rect=pygame.Rect(self.PADDING, 0, *self.COST_BLOCK_SIZE),
            get_cost=get_cost,
            anchors={"top_target": self.title},
            manager=manager,
        )
        prev = self.cost_view
        self.fields = []
        for i, (name, getter, upgrade) in enumerate(fields):
            field = FieldBlock(
                relative_rect=pygame.Rect(self.PADDING, 0, *self.FIELD_SIZE),
                name=name,
                parent=self,
                getter=getter,
                upgrade=upgrade,
                anchors={"top_target": prev},
                manager=manager,
            )
            field.upgrade_signal.connect(self.update_cost)
            self.fields.append(field)
            prev = field

    def update_cost(self):
        self.cost_view.update_resources()

    def update(self, time_delta: float):
        super().update(time_delta)
        if self.can_upgrade():
            for field in self.fields:
                field.active = True
        else:
            for field in self.fields:
                field.active = False


class UpgradesWindow(UIWindow):
    W = 650
    H = 700
    upgrade_system: SpaceshipUpgradeSystem

    def __init__(
        self,
        upgrade_system: SpaceshipUpgradeSystem,
        manager: UIManager,
    ):
        self.upgrade_system = upgrade_system
        super().__init__(
            pygame.Rect((W - self.W) // 2, (H - self.H) // 2, self.W, self.H),
            manager=manager,
            window_display_title="Upgrades",
        )
        self.life_block = UpgradesBlock(
            "Life Upgrades",
            self,
            0,
            0,
            [
                (
                    "Health",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.life_characteristics.max_health,
                            2,
                        )
                    ),
                    self.upgrade_system.life_characteristics_upgrades.upgrade_health_coef,
                ),
                (
                    "Armor",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.life_characteristics.armor, 2
                        )
                    ),
                    self.upgrade_system.life_characteristics_upgrades.upgrade_armor_coef,
                ),
            ],
            lambda: self.upgrade_system.life_characteristics_upgrades.cost,
            can_upgrade=self.upgrade_system.can_upgrade_life_characteristics,
            manager=manager,
        )
        self.velocity_block = UpgradesBlock(
            "Velocity Upgrades",
            self,
            0,
            1,
            [
                (
                    "Speed",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.velocity_characteristics.max_speed,
                            2,
                        )
                    ),
                    self.upgrade_system.velocity_characteristics_upgrades.upgrade_speed,
                ),
                (
                    "Rotation Speed",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.velocity_characteristics.max_rotation_speed,
                            2,
                        )
                    ),
                    self.upgrade_system.velocity_characteristics_upgrades.upgrade_rotation_speed,
                ),
            ],
            lambda: self.upgrade_system.velocity_characteristics_upgrades.cost,
            self.upgrade_system.can_upgrade_velocity_characteristics,
            manager=manager,
        )
        self.weapon_block = UpgradesBlock(
            "Weapon Upgrades",
            self,
            1,
            0,
            [
                (
                    "Bullet Damage",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.weapon_modifiers.bullet_damage_coef,
                            2,
                        )
                    ),
                    self.upgrade_system.weapon_modifiers_upgrades.upgrade_bullet_damage_coef,
                ),
                (
                    "Bullet Life Time",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.weapon_modifiers.bullet_life_time_coef,
                            2,
                        )
                    ),
                    self.upgrade_system.weapon_modifiers_upgrades.upgrade_bullet_life_time_coef,
                ),
                (
                    "Bullet Mass",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.weapon_modifiers.bullet_mass_coef,
                            2,
                        )
                    ),
                    self.upgrade_system.weapon_modifiers_upgrades.upgrade_bullet_mass_coef,
                ),
                (
                    "Bullet Speed",
                    lambda: str(
                        round(
                            self.upgrade_system.spaceship.weapon_modifiers.bullet_speed_coef,
                            2,
                        )
                    ),
                    self.upgrade_system.weapon_modifiers_upgrades.upgrade_bullet_speed_coef,
                ),
            ],
            lambda: self.upgrade_system.weapon_modifiers_upgrades.cost,
            self.upgrade_system.can_upgrade_weapon_modifiers,
            manager=manager,
        )
        if isinstance(self.upgrade_system, MinerUpgradeSystem):
            self.mining_block = UpgradesBlock(
                "Mining Upgrades",
                self,
                1,
                1,
                [
                    (
                        "Level",
                        lambda: str(
                            self.upgrade_system.spaceship.mining_characteristics.level
                        ),
                        self.upgrade_system.mining_characteristics.upgrade_level,
                    )
                ],
                lambda: self.upgrade_system.mining_characteristics.cost,
                self.upgrade_system.can_upgrade_mining_characteristics,
                manager=manager,
            )
