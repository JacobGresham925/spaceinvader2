
import pygame
from pygame.sprite import Sprite
import spritesheet
from time import sleep
import game_functions as gf
import random


class UFO(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(UFO, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Get ship from sprite sheet and load its image and rect.
        self.UFO = pygame.image.load('images/UFO.png')
        # self.ship_images = []
        self.image = self.UFO
        self.image = pygame.transform.scale(self.image, (70, 45))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.gf = gf
        # Load the ship image and get its rect.
        # self.image = pygame.image.load('images/ship.bmp')
        # self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.top = self.screen_rect.top + 25

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = True

    def update(self):
        """Update the ship's posisiton based on the movement flags."""
        # Update the ship's center value, not the rect.
        self.tick = random.randint(1, 1000)
        if self.moving_right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left:
            self.center -= self.ai_settings.ship_speed_factor
        if self.rect.right < self.screen_rect.left and not self.moving_right:
            self.moving_left = False
            if self.tick == random.randint(1, 1000):
                self.moving_right = True
        if self.rect.left > self.screen_rect.right and not self.moving_left:
            self.moving_right = False
            if self.tick == random.randint(1, 1000):
                self.moving_left = True
        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx