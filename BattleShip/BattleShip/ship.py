class Ship(object):
    def __init__(self, name: str, length: int) -> None:
        super().__init__()
        self.name = name
        self.initial = self.name[0]
        self.length = length
        self.health = length

    def __str__(self) -> str:
        return self.name

    def damage(self) -> None:
        self.health -= 1

    def destroyed(self) -> bool:
        return self.health == 0

    def __lt__(self, other: "Ship"):
        return self.name < other.name
