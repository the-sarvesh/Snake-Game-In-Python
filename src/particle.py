"""
Particle System - Visual Effects
Neon Snake Game
"""

import pygame
import random
import math
from typing import List
from .constants import (
    COLORS, GRID_SIZE, PARTICLE_LIFETIME, PARTICLE_COUNT
)


class Particle:
    """Individual particle for visual effects"""

    def __init__(self, x: int, y: int, color: tuple = None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = PARTICLE_LIFETIME
        self.max_life = PARTICLE_LIFETIME

        # Random color from food palette
        if color is None:
            self.color = COLORS["food"]
        else:
            self.color = color

        self.size = random.randint(3, 6)
        self.decay = random.uniform(0.02, 0.05)

    def update(self) -> bool:
        """Update particle, return False if dead"""
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95  # Friction
        self.vy *= 0.95
        self.life -= 1
        return self.life > 0

    def draw(self, surface: pygame.Surface):
        """Draw particle with fade effect"""
        alpha = int(255 * (self.life / self.max_life))
        size = int(self.size * (self.life / self.max_life))

        # Create surface with alpha
        if size > 0:
            pygame.draw.circle(
                surface,
                (*self.color, alpha),
                (int(self.x), int(self.y)),
                size
            )


class ParticleSystem:
    """Manages all particles"""

    def __init__(self):
        self.particles: List[Particle] = []

    def emit(self, x: int, y: int, count: int = PARTICLE_COUNT, color: tuple = None):
        """Emit particles at position"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface)

    def clear(self):
        """Clear all particles"""
        self.particles.clear()


class ScreenShake:
    """Screen shake effect controller"""

    def __init__(self):
        self.intensity = 0
        self.duration = 0
        self.current_offset = (0, 0)

    def trigger(self, intensity: int = 5, duration: int = 10):
        """Trigger screen shake"""
        self.intensity = intensity
        self.duration = duration
        self.current_offset = (0, 0)

    def update(self) -> tuple:
        """Update shake and return offset"""
        if self.duration > 0:
            import random
            self.current_offset = (
                random.randint(-self.intensity, self.intensity),
                random.randint(-self.intensity, self.intensity)
            )
            self.duration -= 1
        else:
            self.current_offset = (0, 0)

        return self.current_offset

    def is_active(self) -> bool:
        """Check if shake is still active"""
        return self.duration > 0
