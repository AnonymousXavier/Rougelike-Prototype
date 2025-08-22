from src.Misc import Misc
from src.Globals import settings


class Camera:
    def __init__(self):
        self.target: tuple[float, float] = (0, 0)
        self.grid_pos = [0, 0]
        self.speed = 3
        self.camera_grid_view_width = 0
        self.camera_grid_view_height = 0
        

    def get_rect(self, grid_width, grid_height):
        clamp = Misc.clamp

        cx, cy = self.grid_pos # Camera Center

        self.camera_grid_view_height = int(settings.SCREEN_HEIGHT / (settings.ZOOM * settings.DEFAULT_ROOM_SIZE)) - 1
        self.camera_grid_view_width = int(settings.SCREEN_WIDTH / (settings.ZOOM * settings.DEFAULT_ROOM_SIZE)) - 1

        half_viewport_width, half_viewport_height = self.camera_grid_view_width / 2, self.camera_grid_view_height / 2

        camera_top = clamp(round(cy - half_viewport_height), 0, grid_height)
        camera_bottom = clamp(round(cy + half_viewport_height), 0, grid_height)
        camera_left = clamp(round(cx - half_viewport_width), 0, grid_width)
        camera_right = clamp(round(cx + half_viewport_width), 0, grid_width)

        if camera_left == 0: 
            camera_right = camera_left + self.camera_grid_view_width
        if camera_right == grid_width: 
            camera_left = camera_right - self.camera_grid_view_width
        if camera_top == 0: 
            camera_bottom = camera_top + self.camera_grid_view_height
        if camera_bottom == grid_height: 
            camera_top = camera_bottom - self.camera_grid_view_height

        class Rect:
            top = int(camera_top)
            bottom = int(camera_bottom)
            left = int(camera_left)
            right = int(camera_right)

            grid_view_center = (cx, cy)
            grid_view_width = self.camera_grid_view_width
            grid_view_height = self.camera_grid_view_height

            width = (grid_view_width + 2) * settings.DEFAULT_ROOM_SIZE
            height = (grid_view_height + 2)* settings.DEFAULT_ROOM_SIZE
            size = (width, height)

        return Rect

    def update(self, dt):
        tx, ty = self.target
        gx, gy = self.grid_pos

        dx, dy = tx - gx, ty - gy
        vw, vh = self.camera_grid_view_width / 2, self.camera_grid_view_height / 2

        distance_multipliyer = Misc.get_vector_magnitude((dx, dy)) / Misc.get_vector_magnitude((vw, vh))
        distance_multipliyer = max(0.01, distance_multipliyer)

        transition_increment = max(0.2, self.speed * dt * distance_multipliyer)

        gx += min(abs(dx), transition_increment) * Misc.sign(dx) 
        gy += min(abs(dy), transition_increment) * Misc.sign(dy) 

        self.grid_pos = gx, gy

    def done_transitioning(self):
        return self.grid_pos == self.target
        