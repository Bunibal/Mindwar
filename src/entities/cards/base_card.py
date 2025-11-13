import json
from enum import Enum, auto

from ursina import Entity, color

#import settings


class CardType(Enum):
    SPELL = auto()
    UNIT = auto()
    BUILDING = auto()
    RESOURCE = auto()


class BaseCard(Entity):
    def __init__(self, card_name: str, card_image: str, card_type: CardType, card_description: str, **kwargs):
        self.card_name = card_name
        self.card_image = card_image
        self.card_type = card_type
        self.card_description = card_description
        self.card_properties = kwargs

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
        return f"{settings.CARDS_DIR}/{card_type_name}.glb"

    def play_card(self):
        # TODO: Implement the logic for playing the card
        print("Playing card:", self.card_name)
        # self.disable()
        # self.delete()

    @staticmethod
    def load_cards():
        cards = []
        with open(settings.CARDS, 'r') as f:
            data = json.load(f)
            for card_data in data['cards']:
                card = BaseCard(
                    card_name=card_data['name'],
                    card_image=card_data['image'],
                    card_type=CardType[card_data['card_type'].upper()],
                    card_description=card_data['description'],
                    **card_data['properties']
                )
                cards.append(card)
        return cards

    def __str__(self):
        return f"Card(card_name={self.card_name}, card_type={self.card_type}, card_image={self.card_image}, card_properties={self.card_properties})"
