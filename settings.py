# settings file

class Settings():
    """A class to store all the settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #self.bg_color = (87, 212, 163)
        #self.bg_image = "images/space.bmp"
        self.bullets_allowed = 3

        # ship settings
        self.ship_speed_factor = 1.5

        # bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
