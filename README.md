# 🚀 Pygame Boss Battle Shooter

A classic 2D top-down space shooter game built using Python and the Pygame library, featuring player movement, enemy spawning, shooting mechanics, and a challenging boss battle triggered by reaching a certain score.

## ✨ Features

* **Player Control:** Use arrow keys for horizontal movement and Spacebar to fire.
* **Sprite-Based Graphics:** Uses custom images (player, enemy, boss) instead of colored squares.
* **Dynamic Difficulty:** Regular enemies are paused when the Boss is active.
* **Boss Encounter:** A high-health boss that fires multiple projectiles and moves in a pattern.
* **Health Bar:** Visual health indicator for the Boss.
* **Collision Detection:** Accurate hit detection for player bullets, enemy bodies, and boss projectiles.

## 🛠️ Installation

### Prerequisites

You must have **Python 3.x** installed on your system.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/your-shooter-game.git](https://github.com/YourUsername/your-shooter-game.git)
    cd your-shooter-game
    ```

2.  **Install Pygame:**
    This project requires the Pygame library.
    ```bash
    pip install pygame
    ```

3.  **Add Assets:**
    The game requires custom image files (PNG recommended for transparency).
    * Create a folder named `assets` in the root directory.
    * Place your images inside, named exactly as:
        * `player_ship.png`
        * `enemy_ship.png`
        * `boss_ship.png`

## ▶️ How to Run

Execute the main game script from your terminal:

```bash
python shooter_game.py