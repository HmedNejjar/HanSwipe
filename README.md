# HanSwipe
HanSwipe is a desktop flashcard application designed to make learning Chinese vocabulary an engaging and effective experience. Built with Python and PyQt5, it features a modern, visually appealing interface with interactive elements to help you master new words.

## Features

- **Add Words:** Easily add new Chinese words with their corresponding Pinyin pronunciation and English meaning.
- **Interactive Flashcards:** Test your knowledge with a stylish flashcard system. Flip cards to reveal the answer with a smooth animation.
- **Progress Tracking:** Keep track of your learning progress by marking words as 'Known' or 'Don't Know'.
- **Local Data Storage:** All your vocabulary is saved locally in a `words_data.json` file, so your data stays on your machine.
- **Custom UI:** A sleek, modern interface with gradient components and smooth animations.

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

- Python 3
- pip

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/hmednejjar/hanswipe.git
   ```
2. Navigate to the project directory:
   ```sh
   cd hanswipe
   ```
3. Install the required packages:
   ```sh
   pip install PyQt5
   ```

### Running the Application

To launch HanSwipe, run the `Main.py` script from your terminal:

```sh
python Main.py
```

## How It Works

The application is structured into several modules, each with a specific responsibility:

- `Main.py`: The entry point and main application controller. It manages window switching and shares the `DataManager` instance across different UI screens.
- `data_manager.py`: Handles all data operations. It loads existing vocabulary from `words_data.json` at startup and saves any new words you add.
- `base_ui.py`: Contains the base window class and custom, reusable UI components like `GradientButton`, `GradientLabel`, and `FlipCard` that give the application its unique look and feel.
- `ui_main_menu.py`: Defines the application's main menu window, providing navigation to add words or start a test session.
- `ui_add_word.py`: Defines the window for adding new words to your vocabulary list.
- `ui_test_screen.py`: Implements the flashcard testing functionality, including the card flip animation and progress counters.

PS: for now after adding words, close the app and relaunch it to be able to test your knowledge 😜 (working on fixing the issue)

## Credits

This application was created by Bakr Marhfoul.
