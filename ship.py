
import pygame
from pygame.sprite import Sprite
import spritesheet
from time import sleep
import game_functions as gf


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Get ship from sprite sheet and load its image and rect.
        self.ss = spritesheet.spritesheet('images/ship_pixelsheet.png')
        self.ship_image = self.ss.image_at((0, 0, 52, 40), -1)
        # self.ship_images = []
        self.image = self.ship_image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.gf = gf
        # Load the ship image and get its rect.
        # self.image = pygame.image.load('images/ship.bmp')
        # self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's posisiton based on the movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

    def explode_ship(self, ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
        """Go through the processes of making the ship explode"""
        self.image = self.ss.image_at((52, 0, 52, 40), -1)
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        pygame.display.flip()
        sleep(.1)
        self.image = self.ss.image_at((0, 40, 52, 40), -1)
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        pygame.display.flip()
        sleep(.1)
        self.image = self.ss.image_at((52, 40, 52, 40), -1)
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        pygame.display.flip()
        sleep(.1)
        self.image = self.ss.image_at((0, 80, 52, 40), -1)
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        pygame.display.flip()
        sleep(.1)
        self.image = self.ss.image_at((52, 80, 52, 40), -1)
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        pygame.display.flip()
        sleep(.1)
        self.image = self.ss.image_at((0, 120, 52, 40), -1)
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        pygame.display.flip()
        sleep(.1)
        self.image = self.ship_image
        screen.fill(ai_settings.bg_color)
        ship.blitme()
        aliens.draw(screen)
        pygame.display.flip()