import pygame
from pygame.sprite import Sprite
import spritesheet

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initilize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # explosion spritesheet
        self.ss = spritesheet.spritesheet('images/alien_exp_pixelsheet.png')
        self.exp1 = self.ss.image_at((0, 0, 40, 40), -1)
        self.exp2 = self.ss.image_at((40, 0, 40, 40), -1)
        self.exp3 = self.ss.image_at((0, 40, 40, 40), -1)
        self.exp4 = self.ss.image_at((40, 40, 40, 40), -1)
        self.die = 0

        # Load the alien image and set its rect attribute
        self.image1a = pygame.image.load('images/Alien_1a.png')
        self.image1a = pygame.transform.scale(self.image1a, (50, 45))
        self.image2a = pygame.image.load('images/Alien_2a.png')
        self.image2a = pygame.transform.scale(self.image2a, (60, 45))
        self.image3a = pygame.image.load('images/Alien_3a.png')
        self.image3a = pygame.transform.scale(self.image3a, (60, 45))
        self.image1b = pygame.image.load('images/Alien_1b.png')
        self.image1b = pygame.transform.scale(self.image1b, (50, 45))
        self.image2b = pygame.image.load('images/Alien_2b.png')
        self.image2b = pygame.transform.scale(self.image2b, (60, 45))
        self.image3b = pygame.image.load('images/Alien_3b.png')
        self.image3b = pygame.transform.scale(self.image3b, (60, 45))
        self.image = self.image1a
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def explode_alien(self): pass

    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

