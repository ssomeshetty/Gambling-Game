# Lucky King

Lucky King is a dynamic gambling game that simulates a journey through 7 levels, where players make decisions at each stage, affecting their progress and earnings. With different risk levels—safe, mid-safe, and not-safe—the game challenges players to maximize their profits while navigating through these stages. The game uses an algorithm that adjusts risk probabilities based on player behavior, ensuring an engaging experience while encouraging continued play. Players’ statuses change from "Poor" to "King" as they progress, with corresponding visual icons for each stage.

---

## Technologies Used

1. **Python** - Backend logic and game mechanics.
2. **Django** - Web framework for building the game’s backend.
3. **SQLite3** - Database for storing player data, bet histories, and game progress.
4. **Bootstrap** - Frontend framework for responsive design and user interface.

---

## Features

- **Dynamic Gameplay**: Navigate through 7 stages with different risk levels at each decision point. Your decisions directly affect your bet amount, earnings, and progress.
  
- **Behavioral Algorithm**: The system dynamically adjusts the likelihood of winning or losing based on your betting patterns, session length, and play history, ensuring an engaging and personalized experience.

- **Visual Progression**: Your status evolves from "Poor" to "King," with corresponding icon changes, depending on your choices and success in the game.

- **Profit Maximization**: The game dynamically introduces more risky choices as you continue playing to ensure that the platform remains profitable, while keeping the experience engaging.

- **Responsible Gambling**: Features like betting limits, session time tracking, and loss recovery ensure that the game promotes ethical play and discourages excessive gambling behavior.

---

## Setup and Installation

### Prerequisites

To run the game locally, ensure you have the following installed:

- Python 3.x
- Django
- SQLite3
- Bootstrap (for front-end)

### Installation Steps

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/lucky-king.git


2. Navigate into the project directory:
   ```bash
   cd lucky-king
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the migrations to set up the database:
   ```bash
   python manage.py migrate
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your browser and navigate to:
   ```text
   http://127.0.0.1:8000
   ```

---

## Responsible Gambling

We encourage responsible gambling by implementing several ethical features in the game:

- **Betting Limits**: Set maximum bet limits to control your exposure.
- **Session Time Tracking**: Keep track of how long you have been playing to avoid excessive gambling.
- **Loss Recovery**: Implement strategies to minimize losses and avoid chasing them.

---

## License

This project is for educational purposes only. It is not intended to be used as a real gambling platform.

---

## Contact

For any inquiries or suggestions, please reach out to the project maintainer at [bremblue189@gmail.com].

---

## Acknowledgments

- Django Framework for web development.
- SQLite3 for data storage.
- Bootstrap for responsive design.
```
