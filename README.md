# Connect 4 with AI

## Project Description

This is a more advanced version of Connect 4 where you play against an AI that learns how to get better over time using
a neural network. I wanted to take the game and make it more interesting by adding machine learning, so the 
AI actually makes smart moves and gets more challenging the more it trains.

## Why I Made This Project
I made this Connect 4 game as part of a challenge in my Predictive Analytics option at BCIT. Our professor encouraged us
to build a game using what we had learned so far. At first, I thought about doing something simple like Tic Tac Toe, but
it felt too basic and didn’t really show off the full potential of what we were learning. I also just wanted to build 
something that wasn’t just for the assignment, but also showed that I could take initiative and apply what I’d learned 
in a meaningful way. So I decided to challenge myself by using an artificial neural network (ANN) to build an AI that 
could play Connect 4 instead. 

This project gave me a chance to familiarize myself with concepts like game state design, reward systems, and how to 
train a model to make decisions. I really wanted to learn more about how AI can be applied outside of typical data 
science tasks and figured building a game would be a fun and creative way to do that. I also got to practice using 
Python along with libraries like NumPy and TensorFlow, which helped me get more comfortable working with machine 
learning tools.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd Connect4Game
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python main.py
```

### System Requirements

- Operating System: Windows 10/11, macOS, or Linux
- RAM: 4GB minimum (8GB recommended for training AI)
- CPU: Multi-core processor recommended for AI training
- Graphics: Basic graphics card supporting OpenGL
- Storage: 500MB free space (including dependencies)
- Python 3.8 or higher

## Technologies Used

### Programming Languages
- Python 3.x

### Frameworks & Libraries
- PyTorch (v2.6.0) - Neural network and deep learning
- NumPy (v2.1.1) - Mathematical operations and board state management
- OpenCV (v4.11.0) - Image processing
- Pygame (via pygbag v0.9.2) - Game engine and graphics
- Scikit-learn (v1.5.2) - Machine learning utilities
- Pandas (v2.2.2) - Data manipulation and analysis

### Development Tools
- Python IDE (PyCharm, VS Code, etc.)
- Git for version control
- Virtual environment for dependency management

## Key Features

### Game Features
- Interactive game board with smooth piece dropping animation
- AI opponent with strategic decision making
- Self-learning AI through neural network training
- Score tracking and game state management
- Win detection in all directions (horizontal, vertical, diagonal)
- Draw game detection

### Technical Features
- Neural network-based AI decision making
- Position evaluation using heuristics
- Efficient board state management
- Modular code structure for easy maintenance
- Advanced AI training system through self-play

## Game Controls

- Mouse: Click on a column to drop a piece
- Menu Navigation:
  - 1: Start AI training mode
  - 2: Play against trained AI
- ESC: Exit game

## Dependencies
For a complete list of dependencies and their versions, see `requirements.txt`.
