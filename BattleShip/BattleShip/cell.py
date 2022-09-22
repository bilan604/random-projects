class Cell(object):
    def __init__(self, content: str, empty_marker, hit_marker: str, miss_marker: str) -> None:
        super().__init__()
        self.content = content
        self.has_been_fired_at = False
        self.empty_marker = empty_marker
        self.hit_marker = hit_marker
        self.miss_marker = miss_marker

    def representation(self, hidden: bool = False) -> str:
        if not self.has_been_fired_at:
            return self.empty_marker if hidden else self.content
        elif self.contains_ship():
            return self.hit_marker
        else:
            return self.miss_marker

    def shoot(self) -> None:
        self.has_been_fired_at = True

    def contains_ship(self) -> bool:
        return self.content != self.empty_marker

    def __str__(self) -> str:
        return self.content
