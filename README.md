# 🏎️ Geo-Racer Matrix 

A modern, arcade-style 2D car racing game built completely with Python and Pygame. Instead of relying on external image sprites, this game renders all graphical assets (cars, road, particles) dynamically using basic geometric shapes and modular drawing functions. 

Developed as a Computer Graphics (CSE-328) Lab Project, this game demonstrates the practical application of Object-Oriented Programming (OOP), File Handling, and interactive event loops.

## ✨ Features

* **🎮 Dual Control System:** Play using either Keyboard (Arrow keys) or Mouse (Click and swipe).
* **📈 Progressive Difficulty:** The game speed and environment dynamically accelerate over time to increase the challenge.
* **🛡️ Collectibles & Power-ups:**
  * **Coins (Yellow):** Grants a +3-second time bonus to your final score.
  * **Shields (Purple):** Provides 5 seconds of invincibility, allowing you to smash through enemy cars.
* **💾 High Score Tracking:** Utilizes File I/O to automatically save and load the highest survival time/score in a `highscore.txt` file.
* **💥 Particle Effects:** Custom crash animation using randomized particle physics when the player collides with an enemy.
* **🎨 Pure Geometric Rendering:** No external image files are needed! Everything is drawn using Pygame's built-in shape and path rendering tools.

## 🛠️ Technologies Used

* **Language:** Python 3.x
* **Library:** Pygame
* **Concepts:** OOP, Collision Detection, Mathematical Coordinate Mapping, File Handling.

## 🕹️ Controls

* **Mouse:** Click and hold the left mouse button, then swipe left or right to steer the car smoothly.
* **Keyboard:** Use `LEFT Arrow` and `RIGHT Arrow` keys to move the car.

## 🚀 How to Run

1. Make sure you have Python installed on your system.
2. Install the required Pygame library using pip:
   ```bash
   pip install pygame# CG-Lab-projects
