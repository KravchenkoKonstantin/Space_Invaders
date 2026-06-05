import pygame
import sys 
import random
from settings import *
from player import Player
from wave import WaveManager
from effects import spawn_particles
from ui import draw_ui, draw_menu, draw_game_over
from highscore import load_highscore, save_highscore

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()

    # Загрузка фона
    try:
        bg_image = pygame.image.load(BACKGROUND_IMG).convert()
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.fill(BLACK)


    # Состояния
    state = "MENU"
    score = 0
    highscore = load_highscore()

    # Игровые объекты
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

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start_game()
                    if event.key == pygame.K_q:
                        running = False
            elif state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        start_game()
                    if event.key == pygame.K_q:
                        running = False

        # Логика игры
        if state == "PLAYING":
            keys = pygame.key.get_pressed()
            player.update(keys, player_bullets)

            status = wave_manager.update(enemy_bullets, player.rect.center)
            if status == 'game_over':
                state = "GAME_OVER"
                save_highscore(score)
                if score > highscore:
                    highscore = score

            player_bullets.update()
            enemy_bullets.update()
            particles.update()

            # Пули игрока против врагов
            hits = pygame.sprite.groupcollide(wave_manager.enemies, player_bullets, False, True)
            for enemy, bullets in hits.items():
                enemy.health -= len(bullets)
                if enemy.health <= 0:
                    enemy.kill()
                    score += 10

                    spawn_particles(particles, enemy.rect.center, ORANGE, 10, 3, 300)

            # Пули игрока против босса
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

            # Вражеские пули против игрока
            hits_player = pygame.sprite.spritecollide(player, enemy_bullets, True)
            if hits_player:
                if player.hit(): 
                    if player.lives <= 0:
                        state = "GAME_OVER"
                        save_highscore(score)
                        if score > highscore:
                            highscore = score
                    else:
                        spawn_particles(particles, player.rect.center, GREEN, 5, 2, 200)

            # Уничтожение пуль друг об друга
            pygame.sprite.groupcollide(enemy_bullets, player_bullets, True, True)


            if len(wave_manager.enemies) == 0 and not wave_manager.boss:
                wave_manager.start_new_wave()
                score += 50 * wave_manager.wave_number

        # Рендеринг
        screen.blit(bg_image, (0, 0))

        if state == "MENU":
            draw_menu(screen, highscore)
        elif state == "PLAYING":
            all_sprites.draw(screen)
            wave_manager.enemies.draw(screen)
            if wave_manager.boss:
                screen.blit(wave_manager.boss.image, wave_manager.boss.rect)
            player_bullets.draw(screen)
            enemy_bullets.draw(screen)
            particles.draw(screen)
            draw_ui(screen, score, player.lives, wave_manager.wave_number)
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