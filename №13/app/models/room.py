from dataclasses import dataclass


@dataclass
class Room:
    id: int
    number: str
    floor: int
    type_name: str
    price: int          # за ночь, ₸
    capacity: int       # максимум гостей
    description: str

    @property
    def title(self):
        return f"№ {self.number} · {self.type_name}"
