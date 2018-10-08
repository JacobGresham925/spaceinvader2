# import sys

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from ufo import UFO
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
# No longer need since we are not creating aliens in this file from alien import Alien
import game_functions as gf
from alien import Alien
# import spritesheet


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")
    highscore_button = Button(ai_settings, screen, 'High Score')
    hs_file = open("score.txt", "r")
    ai_settings.hs = int(hs_file.read())
    hs_file.close()
    msgg = 'The high score is ' + str(ai_settings.hs)
    score = Button(ai_settings, screen, msgg)
    score.rect.centery += 150
    score.msg_image_rect.center = score.rect.center
    highscore_button.rect.centery += 80
    highscore_button.msg_image_rect.center = highscore_button.rect.center
    savescore = 0
    space_invaders = Button(ai_settings, screen, "Space Invaders")
    space_invaders.rect.centery -= 350
    space_invaders.msg_image_rect.center = space_invaders.rect.center
    s10 = Button(ai_settings, screen, " =  10")
    s10.rect.centerx = 1200 / 2 + 100
    s10.rect.top = 80
    s10.msg_image_rect.center = s10.rect.center
    s20 = Button(ai_settings, screen, " =  20")
    s20.rect.centerx = 1200 / 2 + 100
    s20.rect.top = 140
    s20.msg_image_rect.center = s20.rect.center
    s30 = Button(ai_settings, screen, " =  30")
    s30.rect.centerx = 1200 / 2 + 100
    s30.rect.top = 200
    s30.msg_image_rect.center = s30.rect.center
    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    stats.high_score = ai_settings.hs

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    ufo = UFO(ai_settings, screen)
    bullets = Group()
    alienbullets = Group()
    aliens = Group()
    alien = Alien(ai_settings, screen)

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Music
    music1 = pygame.mixer.Sound('audio/deep1.wav')
    music2 = pygame.mixer.Sound('audio/deep2.wav')
    music3 = pygame.mixer.Sound('audio/deep3.wav')

    # Start the main loop for the game.
    while True:
        if ai_settings.hs < stats.high_score and stats.game_active:
            ai_settings.hs = stats.high_score
            msgg = 'The high score is ' + str(ai_settings.hs)
            score = Button(ai_settings, screen, msgg)
            score.rect.centery += 150
            score.msg_image_rect.center = score.rect.center
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets, savescore, highscore_button, msgg)
        if stats.game_active:
            ship.update()
            ufo.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets, alienbullets, play_button, ufo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
                         bullets, play_button, highscore_button, score, alien, space_invaders, s10, s20, s30, music1,
                         music2, music3, alienbullets, ufo)


run_game()
