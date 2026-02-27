# Neon Snake - Enhanced Edition

<p align="center">
  <img src="https://img.shields.io/badge/Python-Pygame-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Version-2.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

A modern, visually stunning Snake game built with Python and Pygame. Features a neon cyber-retro aesthetic with smooth animations, particle effects, and a polished UI.

## Features

### Visual Enhancements
- **Neon Cyber-Retro Theme**: Deep navy background with vibrant neon colors
- **Particle Effects**: Explosions when collecting food
- **Screen Shake**: Impact feedback on collisions
- **Animated UI**: Floating title, pulsing buttons, smooth transitions
- **Glow Effects**: Food pulses with a glowing aura
- **Custom Snake Eyes**: Snake head has eyes that follow movement direction

### Gameplay Improvements
- **Input Buffering**: Prevents accidental 180-degree turns from rapid key presses
- **Dynamic Speed**: Game gradually speeds up as you collect more food
- **Persistent High Scores**: Your best score is saved between sessions
- **Pause Functionality**: Press ESC to pause/resume
- **Smooth Controls**: Supports both arrow keys and WASD

### UI/UX
- **Main Menu**: Animated title with hover effects
- **Heads-Up Display**: Real-time score and high score tracking
- **Game Over Screen**: Shows final score, high score, and restart prompt
- **Responsive Design**: 800x600 window with grid-based gameplay

## Installation

### Prerequisites
- Python 3.7+
- Pygame library

### Setup

1. Clone or download this repository
2. Install the required dependency:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move snake |
| ESC | Pause/Resume |
| SPACE | Restart (on game over) |

## Project Structure

```
snake-game/
├── main.py              # Main game entry point
├── requirements.txt     # Python dependencies
├── src/
│   ├── __init__.py
│   ├── constants.py     # Game configuration
│   ├── snake.py         # Snake logic
│   ├── food.py          # Food with animations
│   ├── particle.py      # Particle effects
│   └── ui.py           # Menus and UI
└── high_score.txt      # Saved high score
```

## Game Screenshots

The game features:
- **Main Menu**: Animated "NEON SNAKE" title with Start and Quit buttons
- **Gameplay**: Grid-based movement with real-time score display
- **Game Over**: Overlay showing final score and high score

## Technical Details

- **Resolution**: 800x600 pixels
- **Grid Size**: 20x20 pixel blocks
- **Frame Rate**: 60 FPS
- **Initial Speed**: 8 moves/second
- **Speed Increase**: +0.5 every 5 food eaten

## License

This project is open source and available under the MIT License.

## Credits

Original game concept by the-sarvesh
Enhanced edition created with modern Python game development practices.

---

<p align="center">Built with Python & Pygame</p>
