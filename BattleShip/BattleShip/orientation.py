import enum


class Orientation(enum.Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    @staticmethod
    def from_string(str_orientation: str) -> "Orientation":
        str_orientation = str_orientation.lower().strip()
        if any(letter.isspace() for letter in str_orientation):
            raise ValueError(f'{str_orientation} does not represent an Orientation')
        for ori in Orientation:
            if ori.value.startswith(str_orientation):
                return ori
        raise ValueError(f'{str_orientation} does not represent an Orientation')
