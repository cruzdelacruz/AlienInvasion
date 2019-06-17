# game functions file

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # limit the number of bullets to number set in settings
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # hide the mouse cursor
        pygame.mouse.set_visible(False)

        # reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()



def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """update images on the screen and flip to the new screen"""
    # redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    #screen.blit(pygame.image.load(ai_settings.bg_image).convert(), [0, 0])

    # redraw all ships behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullets()
    
    ship.blitme()
    aliens.draw(screen)

    # draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()
    # get rid of old bullets

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_collisions(ai_settings, screen, ship, aliens, bullets)
    
def check_bullet_collisions(ai_settings, screen, ship, aliens, bullets):
     # check for any bullets that have hit aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    # repopulating fleet when all aliens disappear
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # decrement ships left
        stats.ships_left -= 1
        
        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        # create new fleet and center ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        # pause
        sleep(0.5)

        print(stats.ships_left)

    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this the same as if a ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """update the position of aliens"""
    """
    Check if the fleet is at an edge and then update the position of
    all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for alien-ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """ Fire a bullet if limit is not reached"""
    if len(bullets) < ai_settings.bullets_allowed:
        # create a new bullet and add it to the bullets group
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """determine the number of aliens that fit in a row"""
    av_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(av_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """determine the number of rows of aliens that fit on the screen"""
    av_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(av_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """create an alien and place it in the row"""
    # create an alien and place it in the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ create a full fleet of aliens"""
    # create an alien and find the number of aliens in a row
    # spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """respond appropriately if any aliens touch a screen edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1


