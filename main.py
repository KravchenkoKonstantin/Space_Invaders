import pygame
import sys
from settings import *
from player import Player
from wave import WaveManager
from effects import spawn_particles
from ui import (Button, draw_ui, draw_menu_screen, draw_leaderboard_screen,
                draw_game_over)
from highscore import load_highscore, load_leaderboard, save_highscore

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    try:
        bg_image = pygame.image.load(BACKGROUND_IMG).convert()
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill(BLACK)

    try:
        heart_img = pygame.image.load(HEART_IMG).convert_alpha()
        HEART_SIZE = 30
        heart_img = pygame.transform.scale(heart_img, (HEART_SIZE, HEART_SIZE))
    except:
        heart_img = None


    state = "MENU"
    score = 0
    highscore = load_highscore()

    btn_width, btn_height = 220, 60
    cx = SCREEN_WIDTH // 2 - btn_width // 2

    btn_color = (128, 0, 128)
    btn_hover = (170, 0, 170)

    start_btn = Button(cx, 250, btn_width, btn_height, "Старт", btn_color, btn_hover)
    leaderboard_btn = Button(cx, 340, btn_width, btn_height, "Топ лидеров", btn_color, btn_hover)
    quit_btn = Button(cx, 430, btn_width, btn_height, "Выход", btn_color, btn_hover)
    menu_buttons = [start_btn, leaderboard_btn, quit_btn]

    back_btn = Button(cx, 480, btn_width, btn_height, "Назад", btn_color, btn_hover)

    player = None
    wave_manager = None
    all_sprites = None
    player_bullets = None
    enemy_bullets = None
    particles = None

    def start_game():
        nonlocal player, wave_manager, all_sprites, player_bullets, enemy_bullets, particles, score, state
        score = 0
        all_sprites = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        particles = pygame.sprite.Group()

        player = Player((SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        all_sprites.add(player)

        wave_manager = WaveManager()
        wave_manager.start_new_wave()
        state = "PLAYING"

    running = True
    while running:
        dt = clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == "LEADERBOARD":
                        state = "MENU"
                    elif state == "GAME_OVER":
                        state = "MENU"

            if state == "MENU":
                for btn in menu_buttons:
                    btn.update(mouse_pos)
                    if btn.handle_event(event):
                        if btn == start_btn:
                            start_game()
                        elif btn == leaderboard_btn:
                            state = "LEADERBOARD"
                        elif btn == quit_btn:
                            running = False

            elif state == "LEADERBOARD":
                back_btn.update(mouse_pos)
                if back_btn.handle_event(event):
                    state = "MENU"

            elif state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start_game()
                    elif event.key == pygame.K_q:
                        state = "MENU"

            elif state == "PLAYING":
                pass

        if state == "PLAYING":
            keys = pygame.key.get_pressed()
            player.update(keys, player_bullets)

            status = wave_manager.update(enemy_bullets, player.rect.center)
            if status == 'game_over':
                state = "GAME_OVER"
                new_high = save_highscore(score)
                if score > highscore:
                    highscore = score

            player_bullets.update()
            enemy_bullets.update()
            particles.update()

            hits = pygame.sprite.groupcollide(wave_manager.enemies, player_bullets, False, True)
            for enemy, bullets in hits.items():
                enemy.health -= len(bullets)
                if enemy.health <= 0:
                    enemy.kill()
                    score += 10
                    spawn_particles(particles, enemy.rect.center, ORANGE, 10, 3, 300)

            if wave_manager.boss:
                hits_boss = pygame.sprite.spritecollide(wave_manager.boss, player_bullets, True)
                for _ in hits_boss:
                    wave_manager.boss.health -= 1
                    if wave_manager.boss.health <= 0:
                        spawn_particles(particles, wave_manager.boss.rect.center, RED, 25, 5, 500)
                        wave_manager.boss.kill()
                        wave_manager.boss = None
                        score += 100
                    else:
                        spawn_particles(particles, wave_manager.boss.rect.center, WHITE, 3, 2, 200)

            hits_player = pygame.sprite.spritecollide(player, enemy_bullets, True)
            if hits_player:
                if player.hit():
                    if player.lives <= 0:
                        state = "GAME_OVER"
                        new_high = save_highscore(score)
                        if score > highscore:
                            highscore = score
                    else:
                        spawn_particles(particles, player.rect.center, GREEN, 5, 2, 200)

            pygame.sprite.groupcollide(enemy_bullets, player_bullets, True, True)

            if len(wave_manager.enemies) == 0 and not wave_manager.boss:
                wave_manager.start_new_wave()
                score += 50 * wave_manager.wave_number

        screen.blit(bg_image, (0, 0))

        if state == "MENU":
            draw_menu_screen(screen, menu_buttons)
        elif state == "LEADERBOARD":
            leaderboard_scores = load_leaderboard()
            draw_leaderboard_screen(screen, leaderboard_scores, back_btn)
        elif state == "PLAYING":
            all_sprites.draw(screen)
            wave_manager.enemies.draw(screen)
            if wave_manager.boss:
                screen.blit(wave_manager.boss.image, wave_manager.boss.rect)
            player_bullets.draw(screen)
            enemy_bullets.draw(screen)
            particles.draw(screen)
            draw_ui(screen, score, player.lives, wave_manager.wave_number, heart_img)
        elif state == "GAME_OVER":
            if all_sprites:
                all_sprites.draw(screen)
                if wave_manager:
                    wave_manager.enemies.draw(screen)
                    if wave_manager.boss:
                        screen.blit(wave_manager.boss.image, wave_manager.boss.rect)
                player_bullets.draw(screen)
                enemy_bullets.draw(screen)
                particles.draw(screen)
            new_high = score >= highscore
            draw_game_over(screen, score, highscore, new_high)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()