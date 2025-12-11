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
 ## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **Left Arrow** | Move player left |
| **Right Arrow** | Move player right |
| **Spacebar** | Fire player bullet |


---


## 🚦 Control Flow States (The Main Blocks)

The game uses a state machine to determine which actions are permitted in the main game loop, ensuring smooth transitions and blocking unwanted actions (like movement) during specific events. 

| State | Value | Description | Permitted Actions |
| :--- | :--- | :--- | :--- |
| **RUNNING** | 1 | Standard combat phase. | Player Movement/Shooting, Enemy/Boss Movement/Shooting, Collision Checks. |
| **BOSS\_ENGAGE** | 3 | Transition state when the Boss spawns. | **Only** Boss Descent Movement. All player/enemy actions are paused. |
| **GAME\_OVER** | 2 | End state after the player is hit. | Drawing 'GAME OVER' message. (All game action is blocked.) |


---


## 🎯 Gameplay Mechanics

* Score 1 point for every regular enemy destroyed.
* Upon reaching **15 points**, the game transitions to the **BOSS\_ENGAGE** state.
* Hitting the Boss reduces its health. Defeating the Boss awards bonus points and resets the state to **RUNNING** with regular enemies.
* Collision with any enemy (or boss projectile) results in **Game Over**.


## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for feature improvements, bug fixes, or better graphics.


## 📜 License

This project is licensed under the MIT License - see the LICENSE.md file for details.