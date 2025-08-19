import pygame


class SpriteSheet:
    def __init__(self, image: pygame.Surface, dimension: tuple[int, int]):
        self.image = image
        self.rows, self.cols = dimension

    def get_frames(self):
        frames = []

        w = self.image.get_width() / self.cols
        h = self.image.get_height() / self.rows

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                x = w * j
                y = h * i

                frame = pygame.Rect(x, y, w, h)
                row.append(frame)
            frames.append(row)
        
        return frames
    
    