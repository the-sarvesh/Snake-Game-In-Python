"""
Snake Class - Enhanced Snake Logic
Neon Snake Game
"""

import pygame
from collections import deque
from typing import List, Tuple
import random
from .constants import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    COLORS, START_X, START_Y
)


class Snake:
    """Enhanced Snake class with smooth movement and input buffering"""

    def __init__(self):
        self.reset()
        self.input_buffer = deque(maxlen=2)
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.grow_pending = 0

    def reset(self):
        """Reset snake to starting position"""
        # Start with length 3, centered
        self.body = [
            (START_X, START_Y),
            (START_X - 1, START_Y),
            (START_X - 2, START_Y)
        ]
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.input_buffer.clear()
        self.grow_pending = 0

    def get_head(self) -> Tuple[int, int]:
        """Get current head position"""
        return self.body[0]

    def set_direction(self, dx: int, dy: int):
        """
        Set direction (with 180-degree turn prevention)
        Uses input buffering to handle rapid key presses
        """
        # Prevent 180-degree turns
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return

        # Add to input buffer
        if len(self.input_buffer) < 2:
            self.input_buffer.append((dx, dy))
        else:
            self.input_buffer.popleft()
            self.input_buffer.append((dx, dy))

    def process_direction(self):
        """Process next direction from buffer"""
        if self.input_buffer:
            self.next_direction = self.input_buffer.popleft()
            # Verify it's not a 180-degree turn
            if self.next_direction != (-self.direction[0], -self.direction[1]):
                self.direction = self.next_direction

    def move(self) -> bool:
        """
        Move snake one step
        Returns True if move successful, False if collision occurred
        """
        self.process_direction()

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False

        # Check self collision (excluding tail tip which will move)
        if new_head in self.body[:-1]:
            return False

        # Add new head
        self.body.insert(0, new_head)

        # Remove tail if not growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

        return True

    def grow(self, amount: int = 1):
        """Mark snake to grow"""
        self.grow_pending += amount

    def check_food_collision(self, food_pos: Tuple[int, int]) -> bool:
        """Check if head collides with food"""
        return self.body[0] == food_pos

    def get_direction_vector(self) -> Tuple[int, int]:
        """Get current direction as (dx, dy) tuple"""
        return self.direction

    def draw(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0):
        """Draw the snake with enhanced visuals"""
        # Draw body segments
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE + offset_x
            y = segment[1] * GRID_SIZE + offset_y

            # Alternate colors for body segments
            if i == 0:
                color = COLORS["snake_head"]
            else:
                color = COLORS["snake_body"] if i % 2 == 0 else COLORS["snake_body_alt"]

            # Draw segment as rounded rectangle
            rect = pygame.Rect(x + 1, y + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(surface, color, rect, border_radius=4)

            # Add glow effect to head
            if i == 0:
                # Draw eyes
                self._draw_eyes(surface, x, y)

    def _draw_eyes(self, surface: pygame.Surface, x: int, y: int):
        """Draw snake eyes based on direction"""
        dx, dy = self.direction
        eye_size = 4

        # Calculate eye positions based on direction
        if dx == 1:  # Right
            eye1 = (x + GRID_SIZE - 6, y + 5)
            eye2 = (x + GRID_SIZE - 6, y + GRID_SIZE - 9)
        elif dx == -1:  # Left
            eye1 = (x + 4, y + 5)
            eye2 = (x + 4, y + GRID_SIZE - 9)
        elif dy == -1:  # Up
            eye1 = (x + 5, y + 4)
            eye2 = (x + GRID_SIZE - 9, y + 4)
        else:  # Down
            eye1 = (x + 5, y + GRID_SIZE - 6)
            eye2 = (x + GRID_SIZE - 9, y + GRID_SIZE - 6)

        pygame.draw.circle(surface, COLORS["snake_eye"], eye1, eye_size)
        pygame.draw.circle(surface, COLORS["snake_eye"], eye2, eye_size)
