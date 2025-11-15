# camera.py

class Camera:
    def __init__(self, screen, world_width, world_height):
        self.screen = screen
        self.world_width = world_width
        self.world_height = world_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, target_x, target_y):
        """
        Center the camera on (target_x, target_y),
        and clamp so we don't go outside the world.
        """
        screen_w, screen_h = self.screen.get_size()

        # center on target
        self.offset_x = target_x - screen_w // 2
        self.offset_y = target_y - screen_h // 2

        # clamp to world bounds
        self.offset_x = max(0, min(self.offset_x, self.world_width - screen_w))
        self.offset_y = max(0, min(self.offset_y, self.world_height - screen_h))

    def world_to_screen(self, x, y):
        """
        Convert world coordinates (x, y) -> screen coordinates.
        Use this for any object you draw.
        """
        return x - self.offset_x, y - self.offset_y
