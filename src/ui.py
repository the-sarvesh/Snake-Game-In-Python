"""
UI Module - Menus, HUD, and Game Screens
Neon Snake Game
"""

import pygame
import math
from typing import Optional, Callable, List
from .constants import (
    COLORS, WINDOW_WIDTH, WINDOW_HEIGHT,
    TITLE_SIZE, SUBTITLE_SIZE, HUD_SIZE, BUTTON_SIZE, SMALL_SIZE,
    FONT_NAME, TITLE_FLOAT_AMPLITUDE, TITLE_FLOAT_SPEED,
    BUTTON_HOVER_SCALE, BUTTON_TRANSITION_SPEED
)


class Button:
    """Interactive button with hover effects"""

    def __init__(self, text: str, x: int, y: int, width: int = 250, height: int = 50,
                 callback: Optional[Callable] = None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback

        self.hovered = False
        self.hover_scale = 1.0
        self.target_scale = 1.0

    def update(self):
        """Update button state"""
        # Smooth hover transition
        self.hover_scale += (self.target_scale - self.hover_scale) * BUTTON_TRANSITION_SPEED

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events, return True if clicked"""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.hovered = self.is_point_inside(mouse_pos)
            self.target_scale = BUTTON_HOVER_SCALE if self.hovered else 1.0

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.callback:
                self.callback()
                return True
        return False

    def is_point_inside(self, point: tuple) -> bool:
        """Check if point is inside button"""
        rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        return rect.collidepoint(point)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """Draw button with effects"""
        # Calculate scaled dimensions
        scaled_width = int(self.width * self.hover_scale)
        scaled_height = int(self.height * self.hover_scale)

        # Draw button background
        rect = pygame.Rect(
            self.x - scaled_width // 2,
            self.y - scaled_height // 2,
            scaled_width,
            scaled_height
        )

        # Color based on hover state
        if self.hovered:
            pygame.draw.rect(surface, COLORS["button_hover"], rect, border_radius=8)
            pygame.draw.rect(surface, COLORS["accent"], rect, 2, border_radius=8)
        else:
            pygame.draw.rect(surface, COLORS["button_normal"], rect, border_radius=8)
            pygame.draw.rect(surface, COLORS["button_border"], rect, 2, border_radius=8)

        # Draw text
        text_surface = font.render(self.text, True, COLORS["text_primary"])
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)


class UI:
    """UI Manager for menus and HUD"""

    def __init__(self):
        self.title_animation = 0.0
        self.game_over_alpha = 0
        self.show_game_over = False

    def draw_main_menu(self, surface: pygame.Surface, buttons: List[Button]):
        """Draw main menu screen"""
        # Background
        surface.fill(COLORS["background"])

        # Draw grid
        self._draw_grid(surface)

        # Animated title
        self.title_animation += TITLE_FLOAT_SPEED
        title_y = WINDOW_HEIGHT // 4 + math.sin(self.title_animation) * TITLE_FLOAT_AMPLITUDE

        # Title shadow
        title_font = pygame.font.Font(FONT_NAME, TITLE_SIZE)
        title_shadow = title_font.render("NEON SNAKE", True, (0, 0, 0))
        title_rect = title_shadow.get_rect(center=(WINDOW_WIDTH // 2 + 3, title_y + 3))
        surface.blit(title_shadow, title_rect)

        # Title
        title_surface = title_font.render("NEON SNAKE", True, COLORS["accent"])
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, title_y))
        surface.blit(title_surface, title_rect)

        # Subtitle
        subtitle_font = pygame.font.Font(FONT_NAME, SUBTITLE_SIZE)
        subtitle_surface = subtitle_font.render("Enhanced Edition", True, COLORS["text_secondary"])
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, title_y + 60))
        surface.blit(subtitle_surface, subtitle_rect)

        # Draw buttons
        for button in buttons:
            button.update()
            button.draw(surface, pygame.font.Font(FONT_NAME, BUTTON_SIZE))

    def draw_hud(self, surface: pygame.Surface, score: int, high_score: int):
        """Draw in-game HUD"""
        # Semi-transparent HUD background
        hud_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 50)
        pygame.draw.rect(surface, (0, 0, 0, 128), hud_rect)

        # Score
        font = pygame.font.Font(FONT_NAME, HUD_SIZE)
        score_text = font.render(f"Score: {score}", True, COLORS["text_primary"])
        surface.blit(score_text, (20, 12))

        # High Score
        high_score_text = font.render(f"High Score: {high_score}", True, COLORS["accent"])
        high_score_rect = high_score_text.get_rect(right=WINDOW_WIDTH - 20, y=12)
        surface.blit(high_score_text, high_score_rect)

    def draw_paused(self, surface: pygame.Surface):
        """Draw paused overlay"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLORS["paused_overlay"])
        surface.blit(overlay, (0, 0))

        # Paused text
        font = pygame.font.Font(FONT_NAME, TITLE_SIZE)
        text = font.render("PAUSED", True, COLORS["text_primary"])
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        surface.blit(text, rect)

        # Instruction
        small_font = pygame.font.Font(FONT_NAME, SMALL_SIZE)
        instruction = small_font.render("Press ESC to resume", True, COLORS["text_secondary"])
        instr_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        surface.blit(instruction, instr_rect)

    def draw_game_over(self, surface: pygame.Surface, score: int, high_score: int, is_new_high_score: bool):
        """Draw game over screen"""
        # Fade in effect
        if self.game_over_alpha < 255:
            self.game_over_alpha += 15

        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(200, self.game_over_alpha)))
        surface.blit(overlay, (0, 0))

        # Game Over text
        font = pygame.font.Font(FONT_NAME, TITLE_SIZE)
        text = font.render("GAME OVER", True, COLORS["food"])
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        surface.blit(text, rect)

        # Score
        score_font = pygame.font.Font(FONT_NAME, SUBTITLE_SIZE)
        score_text = score_font.render(f"Score: {score}", True, COLORS["text_primary"])
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        surface.blit(score_text, score_rect)

        # High Score
        if is_new_high_score:
            hs_color = COLORS["accent"]
            hs_text = score_font.render("NEW HIGH SCORE!", True, hs_color)
        else:
            hs_color = COLORS["text_secondary"]
            hs_text = score_font.render(f"High Score: {high_score}", True, hs_color)

        hs_rect = hs_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        surface.blit(hs_text, hs_rect)

        # Restart instruction (pulsing)
        instruction_font = pygame.font.Font(FONT_NAME, BUTTON_SIZE)
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
        alpha = int(100 + 155 * pulse)
        instruction = instruction_font.render("Press SPACE to Restart", True, (*COLORS["text_secondary"], alpha))

        # Render with alpha
        inst_surface = pygame.Surface(instruction.get_size(), pygame.SRCALPHA)
        inst_surface.blit(instruction, (0, 0))
        inst_surface.set_alpha(alpha)

        instr_rect = inst_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3))
        surface.blit(inst_surface, instr_rect)

    def reset_game_over(self):
        """Reset game over state"""
        self.game_over_alpha = 0

    def _draw_grid(self, surface: pygame.Surface):
        """Draw background grid"""
        from .constants import GRID_SIZE

        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, COLORS["grid_line"], (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, COLORS["grid_line"], (0, y), (WINDOW_WIDTH, y), 1)
