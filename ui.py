import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)  # рамка
        font = pygame.font.Font(None, 40)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_text(surface, text, size, color, x, y, center=True):
    font = pygame.font.Font(None, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surf, text_rect)

def draw_menu_screen(surface, buttons):
    surface.fill(BLACK)
    draw_text(surface, "Space Invaders", 64, GREEN, SCREEN_WIDTH//2, 120)
    for btn in buttons:
        btn.draw(surface)

def draw_leaderboard_screen(surface, scores, back_button):
    surface.fill(BLACK)
    draw_text(surface, "ТОП ЛИДЕРОВ", 48, YELLOW, SCREEN_WIDTH//2, 60)
    if not scores:
        draw_text(surface, "Нет рекордов", 36, WHITE, SCREEN_WIDTH//2, 200)
    else:
        for i, sc in enumerate(scores):
            y = 130 + i * 50
            draw_text(surface, f"{i+1}. {sc}", 36, WHITE, SCREEN_WIDTH//2, y)
    back_button.draw(surface)

def draw_ui(surface, score, lives, wave):
    draw_text(surface, f"Очки: {score}", 30, WHITE, 70, 20, center=False)
    draw_text(surface, f"Жизни: {lives}", 30, WHITE, SCREEN_WIDTH - 70, 20, center=False)
    draw_text(surface, f"Волна: {wave}", 30, WHITE, SCREEN_WIDTH // 2, 20)

def draw_game_over(surface, score, highscore, new_high):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    draw_text(surface, "ИГРА ОКОНЧЕНА", 72, RED, SCREEN_WIDTH//2, 150)
    draw_text(surface, f"Очки: {score}", 48, WHITE, SCREEN_WIDTH//2, 250)
    if new_high:
        draw_text(surface, "НОВЫЙ РЕКОРД!", 36, YELLOW, SCREEN_WIDTH//2, 300)
    else:
        draw_text(surface, f"Рекорд: {highscore}", 36, WHITE, SCREEN_WIDTH//2, 300)
    draw_text(surface, "ENTER - играть снова", 30, WHITE, SCREEN_WIDTH//2, 400)
    draw_text(surface, "Q - выход в меню", 30, WHITE, SCREEN_WIDTH//2, 440)