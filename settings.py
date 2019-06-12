# settings file

class Settings():
    """A class to store all the settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (87, 212, 163)

        # ship settings
        self.ship_speed_factor = 1.5

