"""
Food Class - Enhanced Food Logic
Neon Snake Game
"""

import pygame
import random
from typing import Tuple
from .constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    COLORS
)


class Food:
    """Enhanced Food class with visual effects"""

    def __init__(self):
        self.position = (0, 0)
        self.animation_frame = 0
        self.pulse_direction = 1
        self.refresh()

    def refresh(self, occupied_positions: set = None):
        """Spawn food at random empty position"""
        if occupied_positions is None:
            occupied_positions = set()

        # Find empty position
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                break
        else:
            # If no empty position, use center
            self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

        self.animation_frame = random.random() * 6.28  # Random start phase

    def get_position(self) -> Tuple[int, int]:
        """Get food position"""
        return self.position

    def update(self):
        """Update animation"""
        self.animation_frame += 0.15
        if self.animation_frame > 6.28:
            self.animation_frame = 0

    def draw(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """Draw food with pulsing glow effect"""
        x = self.position[0] * GRID_SIZE + offset_x
        y = self.position[1] * GRID_SIZE + offset_y
        center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)

        # Calculate pulse scale
        pulse = (self.animation_frame % 6.28) / 6.28
        pulse_scale = 0.8 + 0.4 * abs(pulse - 0.5) * 2

        # Draw outer glow
        glow_size = int(GRID_SIZE * 1.5 * pulse_scale)
        glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surface,
            (*COLORS["food_glow"], 100),
            (glow_size, glow_size),
            glow_size // 2
        )
        surface.blit(glow_surface, (center[0] - glow_size, center[1] - glow_size))

        # Draw food (circle with gradient effect)
        food_size = int((GRID_SIZE // 2 - 2) * pulse_scale)
        pygame.draw.circle(surface, COLORS["food"], center, food_size)

        # Draw highlight
        highlight_pos = (center[0] - food_size // 3, center[1] - food_size // 3)
        pygame.draw.circle(surface, (255, 255, 255), highlight_pos, max(2, food_size // 4))
