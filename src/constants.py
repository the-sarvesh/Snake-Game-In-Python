"""
Game Constants Configuration
Neon Snake - Enhanced Snake Game
"""

import pygame
import os

# ============================================
# WINDOW & DISPLAY SETTINGS
# ============================================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 60

# ============================================
# COLOR PALETTE (Neon Cyber-Retro Theme)
# ============================================
COLORS = {
    # Background colors
    "background": (15, 23, 42),        # Deep Navy #0F172A
    "grid": (30, 41, 59),               # Lighter Slate #1E293B
    "grid_line": (30, 41, 59),          # Grid lines

    # Snake colors
    "snake_head": (16, 185, 129),       # Emerald Green #10B981
    "snake_body": (52, 211, 153),       # Light Green #34D399
    "snake_body_alt": (34, 197, 94),    # Green #22C55E
    "snake_eye": (255, 255, 255),       # White eyes

    # Food colors
    "food": (244, 63, 94),             # Neon Rose #F43F5E
    "food_glow": (251, 113, 133),       # Light Rose

    # UI colors
    "text_primary": (248, 250, 252),    # Off-white #F8FAFC
    "text_secondary": (148, 163, 184),  # Gray #94A3B8
    "accent": (245, 158, 11),           # Amber #F59E0B
    "accent_glow": (251, 191, 36),      # Light Amber

    # Button colors
    "button_normal": (30, 41, 59),       # Slate
    "button_hover": (51, 65, 85),       # Light Slate
    "button_border": (100, 116, 139),   # Border

    # Game state colors
    "game_over_overlay": (0, 0, 0, 180), # Semi-transparent black
    "paused_overlay": (0, 0, 0, 128),
}

# ============================================
# GAME MECHANICS SETTINGS
# ============================================
INITIAL_SPEED = 8  # Moves per second
SPEED_INCREMENT = 0.5
SPEED_INTERVAL = 5  # Increase speed every N food eaten
MAX_SPEED = 20

# Snake starting position (grid coordinates)
START_X = GRID_WIDTH // 2
START_Y = GRID_HEIGHT // 2

# ============================================
# UI SETTINGS
# ============================================
FONT_NAME = None  # Use default system font
TITLE_SIZE = 72
SUBTITLE_SIZE = 36
HUD_SIZE = 24
BUTTON_SIZE = 28
SMALL_SIZE = 18

# ============================================
# FILE PATHS
# ============================================
HIGH_SCORE_FILE = "high_score.txt"

# ============================================
# ANIMATION SETTINGS
# ============================================
PARTICLE_LIFETIME = 30  # Frames
PARTICLE_COUNT = 8
SCREEN_SHAKE_DURATION = 10
SCREEN_SHAKE_INTENSITY = 3

# Menu animation
TITLE_FLOAT_AMPLITUDE = 5
TITLE_FLOAT_SPEED = 0.05
BUTTON_HOVER_SCALE = 1.1
BUTTON_TRANSITION_SPEED = 0.2
