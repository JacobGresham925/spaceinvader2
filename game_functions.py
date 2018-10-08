import sys
from time import sleep
import pygame
from bullet import Bullet
from bulletalien import Bulletalien
from alien import Alien
# from button import Button
import random


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def fire_alienbullet(aliens, alienbullets, ai_settings, screen):
    for alien in aliens:
        if len(aliens) > 50:
            ran = random.randint(1, 30000)
            if ran < 2:
                new_bullet2 = Bulletalien(ai_settings, screen, alien)
                alienbullets.add(new_bullet2)
        if len(aliens) > 40:
            ran = random.randint(1, 20000)
            if ran < 3:
                new_bullet = Bulletalien(ai_settings, screen, alien)
                alienbullets.add(new_bullet)
        if len(aliens) < 40:
            ran = random.randint(1, 12000)
            if ran < 5:
                new_bullet = Bulletalien(ai_settings, screen, alien)
                alienbullets.add(new_bullet)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, savescore, highscore_button, msgg):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)
            get_high_score(ai_settings, screen, sb, ship, aliens, bullets, play_button, msgg, highscore_button, stats, mouse_x, mouse_y)


def get_high_score(ai_settings, screen, sb, ship, aliens, bullets, play_button, msgg, highscore_button, stats, mouse_x, mouse_y):
    button2_clicked = highscore_button.rect.collidepoint(mouse_x, mouse_y)
    if button2_clicked and not stats.game_active:
        ai_settings.hs = 1


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Start a new game the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        ai_settings.mu = 1

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, highscore_button, score, alien, space_invaders, s10, s20, s30, music1, music2, music3,
                  alienbullets, ufo):
    """Update images on the screen and flip the new screen"""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alienbullet in alienbullets.sprites():
        alienbullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information.
    sb.show_score()
    if ai_settings.mu == 1:
        music2.stop()
        music3.stop()
        music1.play(-1)
        ai_settings.mu = 0
    if ai_settings.mu == 2:
        music1.stop()
        music3.stop()
        music2.play(-1)
        ai_settings.mu = 0
    if ai_settings.mu == 3:
        music1.stop()
        music2.stop()
        music3.play(-1)
        ai_settings.mu = 0
    ufo.blitme()
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        screen.fill(ai_settings.bg_color)
        play_button.draw_button()
        highscore_button.draw_button()
        space_invaders.draw_button()
        s10.draw_button()
        s20.draw_button()
        s30.draw_button()
        alien.image = alien.image1a
        alien.rect.centerx = 1200 / 2 + 6
        alien.rect.top = 80
        alien.blitme()
        alien.image = alien.image2a
        alien.rect.centerx = 1200 / 2
        alien.rect.top = 140
        alien.blitme()
        alien.image = alien.image3a
        alien.rect.centerx = 1200 / 2
        alien.rect.top = 200
        alien.blitme()
        if ai_settings.hs == 1:
            score.draw_button()
    if stats.game_active:
        ai_settings.hs = 0
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, alienbullets, play_button, ufo):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()
    alienbullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for bulletalien in alienbullets.copy():
        if bulletalien.rect.top >= 800:
            alienbullets.remove(bulletalien)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)
    alienbullet_ship_collision(alienbullets, ship, ai_settings, screen, stats, sb, aliens, bullets, play_button, ufo)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, False)
    alien_die(ai_settings, screen, aliens, bullets)
    if len(aliens) == 66:
        ai_settings.mu = 1
    if len(aliens) == 44:
        ai_settings.mu = 2
    if len(aliens) == 22:
        ai_settings.mu = 3
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # Destroy existing bullets, speed up game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def alien_die(ai_settings, screen, aliens, bullets):
    for alien in aliens.sprites():
        if alien.die == 0:
            for bullet in bullets.sprites():
                if pygame.Rect.colliderect(alien.rect, bullet.rect):
                    alien.die = 1
                    bullets.remove(bullet)
        elif alien.die == 1:
            alien.image = alien.exp1
        elif alien.die == 5:
            alien.image = alien.exp2
        elif alien.die == 10:
            alien.image = alien.exp3
        elif alien.die == 15:
            alien.image = alien.exp4
        elif alien.die == 20:
            aliens.remove(alien)
        if alien.die > 0:
            alien.die += 1


def alienbullet_ship_collision(alienbullets, ship, ai_settings, screen, stats, sb, aliens, bullets, play_button, ufo):
    for alienbullet in alienbullets.sprites():
        if pygame.Rect.colliderect(alienbullet.rect, ship.rect):
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets)
    for bullet in bullets:
        if pygame.Rect.colliderect(bullet.rect, ufo.rect):
            bullets.remove(bullet)
            stats.score += (random.randint(1, 5) * 100)
            sb.prep_score()
            sb.prep_high_score()


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    if row_number == 2 or row_number == 3:
        alien.image = alien.image2a
    if row_number == 4 or row_number == 5:
        alien.image = alien.image3a
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    if row_number == 0 or row_number == 1:
        alien.rect.x = alien.x + 10
    else:
        alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Update scoreboard.
        sb.prep_ships()
        ship.explode_ship(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        alienbullets.empty()
        # ship.image = ship.ship_image
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause
        sleep(0.5)

    else:
        ship.explode_ship(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        hs_file = open("score.txt", "r")
        hs = int(hs_file.read())
        hs_file.close()
        if stats.high_score > hs:
            hs_file = open("score.txt", "w")
            hs_file.write(str(stats.high_score))
            hs_file.close()
        hs_file = open("score.txt", "r")
        hs = int(hs_file.read())
        hs_file.close()
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets)
            break


def flip_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    for alien in aliens.sprites():
        if alien.image == alien.image1a or alien.image == alien.image2a or alien.image == alien.image3a:
            if alien.image == alien.image1a:
                alien.image = alien.image1b
                # alien.x = alien.rect.x + 10
            if alien.image == alien.image2a:
                alien.image = alien.image2b
            if alien.image == alien.image3a:
                alien.image = alien.image3b
        else:
            if alien.image == alien.image1b:
                alien.image = alien.image1a
                # alien.x = alien.rect.x + 10
            if alien.image == alien.image2b:
                alien.image = alien.image2a
            if alien.image == alien.image3b:
                alien.image = alien.image3a


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets):
    """
    Check if the fleet is at an edge,
    and then update the positions of all aliens in the fleet.
    """
    fire_alienbullet(aliens, alienbullets, ai_settings, screen)
    check_fleet_edges(ai_settings, aliens)
    if ai_settings.tick == 30:
        flip_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        ai_settings.tick = 0
    ai_settings.tick += 1
    aliens.update()


    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, alienbullets)


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()