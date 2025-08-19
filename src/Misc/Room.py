class Room:
    def __init__(self, x: int, y: int, size: int):
        self.size = size
        self.top_left = x, y

    def is_inside(self, coord: tuple[int, int]):
        tx, ty = self.top_left
        bx, by = tx + self.size, ty + self.size
        px, py = coord

        return px > tx and px < bx and py > ty and py < by

