import pygame
from settings import *

def draw_text(surface, text, size, color, x, y, center=True):
    font = pygame.font.Font(None, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surf, text_rect)

def draw_ui(surface, score, lives, wave):
    draw_text(surface, f"Score: {score}", 30, WHITE, 70, 20, center=False)
    draw_text(surface, f"Lives: {lives}", 30, WHITE, SCREEN_WIDTH - 70, 20, center=False)
    draw_text(surface, f"Wave: {wave}", 30, WHITE, SCREEN_WIDTH // 2, 20)

def draw_menu(surface, highscore):
    surface.fill(BLACK)
    draw_text(surface, "SPACE INVADERS", 64, GREEN, SCREEN_WIDTH//2, 150)
    draw_text(surface, "Press ENTER to Start", 36, WHITE, SCREEN_WIDTH//2, 300)
    draw_text(surface, "Press Q to Quit", 36, WHITE, SCREEN_WIDTH//2, 350)
    draw_text(surface, f"High Score: {highscore}", 30, YELLOW, SCREEN_WIDTH//2, 450)

def draw_game_over(surface, score, highscore, new_high):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    draw_text(surface, "GAME OVER", 72, RED, SCREEN_WIDTH//2, 150)
    draw_text(surface, f"Score: {score}", 48, WHITE, SCREEN_WIDTH//2, 250)
    if new_high:
        draw_text(surface, "NEW HIGH SCORE!", 36, YELLOW, SCREEN_WIDTH//2, 300)
    else:
        draw_text(surface, f"High Score: {highscore}", 36, WHITE, SCREEN_WIDTH//2, 300)
    draw_text(surface, "Press ENTER to Play Again", 30, WHITE, SCREEN_WIDTH//2, 400)
    draw_text(surface, "Press Q to Quit", 30, WHITE, SCREEN_WIDTH//2, 440)