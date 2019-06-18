# settings file

class Settings():
    """A class to store all the settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's static  settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #self.bg_color = (87, 212, 163)
        #self.bg_image = "images/space.bmp"
        self.bullets_allowed = 3

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # alien_settings
        self.alien_drop_speed = 10

        # how quickly the game speeds up
        self.speedup_scale = 1.2

        # how quickly the alien point value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        
        # scoring
        self.alien_points = 50

    def increase_speed(self):
        """initialize speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

