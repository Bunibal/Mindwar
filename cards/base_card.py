from enum import Enum, auto

from ursina import Entity, color


class CardType(Enum):
    SPELL = auto()
    UNIT = auto()
    BUILDING = auto()
    RESOURCE = auto()

class BaseCard(Entity):
    def __init__(self, name: str, card_type: CardType, description: str, **kwargs):
        self.name = name
        self.card_type = card_type
        self.description = description
        self.properties = kwargs

        super().__init__(
            model=self.get_model_for_card(card_type),
            scale=(1, 1, 1),
            position=(0, 0, 0),
            origin=(0, 0),
            highlight_color=color.azure,
            pressed_color=color.lime
        )

    @staticmethod
    def get_model_for_card(card_type: CardType):
        card_type_name = card_type.name.lower()
        return f"assets/models/cards/{card_type_name}.glb"

    def play_card(self):
        self.disable()
        self.delete()