# Rush Hour AI Automation 🚗💨

This project involves automating the classic **Rush Hour** game, where the objective is to maneuver cars to free a specific vehicle from a congested parking lot. Developed for the **Artificial Intelligence** course in 2022, the goal was to create an algorithm that enables the computer to play the game independently, optimizing moves to achieve the objective efficiently.

## 🎮 Project Overview

In the **Rush Hour** game, players must strategically move vehicles to create a path for the target car to exit the parking lot. The challenge lies in navigating the grid and finding the optimal sequence of moves to solve the puzzle. This project automates the gameplay by implementing search algorithms and decision-making processes that mimic human strategy.

## 🛠️ Technologies Used
- **Python**: The primary programming language used for developing the automation script.
- **Pygame**: A library for creating graphical games, used to simulate the Rush Hour game environment.
- **Artificial Intelligence Algorithms**: Techniques such as **A*** search, **Breadth-First Search (BFS)**, or other pathfinding algorithms to determine the best moves.

## 📦 How to Install
Make sure you are running Python 3.7 or higher. Follow these steps to set up the project:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ia-rush.git
   cd ia-rush
2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows

2. **Install the required dependencies**:
   ```bash
    pip install -r requirements.txt

## 🎮 How to Play
To play the game, open three terminals and run the following commands in each terminal make sure the client pygame window has focus:

Start the server:
  ```bash
  python server.py
  ```

Start the viewer:
  ```bash
  python viewer.py
  ```

Start the client:
  ```bash
  python client.py
  ```
