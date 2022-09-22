from . import ship, orientation


class ShipPlacement(object):

    def __init__(self, ship_: ship.Ship,
                 orientation_: orientation.Orientation,
                 row_start: int, col_start: int) -> None:
        self.ship = ship_
        self.row_start = row_start
        self.col_start = col_start
        self.orientation = orientation_
        if orientation_ == orientation.Orientation.HORIZONTAL:
            self.row_end = row_start
            self.col_end = col_start + ship_.length - 1
        elif orientation_ == orientation.Orientation.VERTICAL:
            self.row_end = row_start + ship_.length - 1
            self.col_end = col_start
        else:
            raise NotImplementedError(f'Placing ships {orientation_} is not supported yet.')

