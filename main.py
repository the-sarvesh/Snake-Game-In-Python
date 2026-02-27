"""
Neon Snake - Enhanced Snake Game
Main Entry Point
"""

import pygame
import sys
import random
from enum import Enum
from typing import Optional

from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GRID_SIZE,
    COLORS, INITIAL_SPEED, SPEED_INCREMENT, SPEED_INTERVAL, MAX_SPEED,
    HIGH_SCORE_FILE
)
from src.snake import Snake
from src.food import Food
from src.particle import ParticleSystem, ScreenShake
from src.ui import Button, UI


class GameState(Enum):
    """Game state enumeration"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Game:
    """Main game class"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Neon Snake - Enhanced Edition")

        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.high_score = self.load_high_score()
        self.speed = INITIAL_SPEED

        # Game objects
        self.snake = Snake()
        self.food = Food()
        self.particles = ParticleSystem()
        self.screen_shake = ScreenShake()
        self.ui = UI()

        # UI elements
        self.buttons = self.create_menu_buttons()

        # Font
        self.font = pygame.font.Font(None, 36)

    def load_high_score(self) -> int:
        """Load high score from file"""
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """Save high score to file"""
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(self.high_score))

    def create_menu_buttons(self):
        """Create main menu buttons"""
        buttons = []
        button_y = WINDOW_HEIGHT // 2
        button_spacing = 70

        # Start button
        start_btn = Button("START GAME", WINDOW_WIDTH // 2, button_y, callback=self.start_game)
        buttons.append(start_btn)

        # Quit button
        quit_btn = Button("QUIT", WINDOW_WIDTH // 2, button_y + button_spacing * 2, callback=self.quit_game)
        buttons.append(quit_btn)

        return buttons

    def start_game(self):
        """Start a new game"""
        self.snake.reset()
        self.food.refresh(set(self.snake.body))
        self.score = 0
        self.speed = INITIAL_SPEED
        self.particles.clear()
        self.ui.reset_game_over()
        self.state = GameState.PLAYING

    def toggle_pause(self):
        """Toggle pause state"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING

    def game_over(self):
        """Handle game over"""
        # Check high score
        is_new_high_score = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            is_new_high_score = True

        self.screen_shake.trigger(intensity=8, duration=15)
        self.state = GameState.GAME_OVER

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Menu events
            if self.state == GameState.MENU:
                for button in self.buttons:
                    button.handle_event(event)

            # Game events
            elif self.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.toggle_pause()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.set_direction(0, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.set_direction(0, 1)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.set_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.set_direction(1, 0)

            # Paused events
            elif self.state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.toggle_pause()

            # Game over events
            elif self.state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_game()

        return True

    def update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            # Update food
            self.food.update()

            # Move snake
            if not self.snake.move():
                self.game_over()
                return

            # Check food collision
            if self.snake.check_food_collision(self.food.get_position()):
                # Emit particles
                food_x = self.food.get_position()[0] * GRID_SIZE + GRID_SIZE // 2
                food_y = self.food.get_position()[1] * GRID_SIZE + GRID_SIZE // 2
                self.particles.emit(food_x, food_y, count=12, color=COLORS["food"])

                # Grow snake and update score
                self.snake.grow()
                self.score += 1

                # Increase speed periodically
                if self.score % SPEED_INTERVAL == 0 and self.speed < MAX_SPEED:
                    self.speed += SPEED_INCREMENT

                # Spawn new food
                self.food.refresh(set(self.snake.body))

        # Update particles
        self.particles.update()

        # Update screen shake
        self.screen_shake.update()

    def draw(self):
        """Draw game"""
        # Get screen shake offset
        shake_offset = self.screen_shake.current_offset

        # Draw based on state
        if self.state == GameState.MENU:
            self.ui.draw_main_menu(self.screen, self.buttons)

        elif self.state in [GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER]:
            # Apply screen shake
            self.screen.fill(COLORS["background"])

            # Draw grid (with offset for shake)
            self._draw_grid(shake_offset)

            # Draw game objects (with offset)
            self.food.draw(self.screen, shake_offset[0], shake_offset[1])
            self.snake.draw(self.screen, shake_offset[0], shake_offset[1])
            self.particles.draw(self.screen)

            # Draw HUD
            self.ui.draw_hud(self.screen, self.score, self.high_score)

            # Draw pause overlay
            if self.state == GameState.PAUSED:
                self.ui.draw_paused(self.screen)

            # Draw game over
            if self.state == GameState.GAME_OVER:
                is_new = self.score >= self.high_score and self.score > 0
                self.ui.draw_game_over(self.screen, self.score, self.high_score, is_new)

        pygame.display.flip()

    def _draw_grid(self, offset=(0, 0)):
        """Draw background grid"""
        from src.constants import GRID_SIZE

        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(
                self.screen, COLORS["grid_line"],
                (x + offset[0] % GRID_SIZE, 0),
                (x + offset[0] % GRID_SIZE, WINDOW_HEIGHT),
                1
            )
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(
                self.screen, COLORS["grid_line"],
                (0, y + offset[1] % GRID_SIZE),
                (WINDOW_WIDTH, y + offset[1] % GRID_SIZE),
                1
            )

    def quit_game(self):
        """Quit the game"""
        pygame.quit()
        sys.exit()

    def run(self):
        """Main game loop"""
        running = True

        # Custom event for snake movement timing
        MOVE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(MOVE_EVENT, int(1000 / self.speed))

        while running:
            # Handle events
            running = self.handle_events()

            # Update movement timer based on current speed
            current_interval = int(1000 / self.speed)
            pygame.time.set_timer(MOVE_EVENT, current_interval)

            # Handle movement event
            for event in pygame.event.get(MOVE_EVENT):
                if self.state == GameState.PLAYING:
                    self.update()

            # Draw
            self.draw()

            # Cap framerate
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
