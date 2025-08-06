import json
import os

class DataManager:
    def __init__(self, filename="words_data.json"):
        """Initialize DataManager with a filename and load data from file."""
        self.filename = filename
        self.words = {}
        self.loadData()

    def loadData(self):
        """Load words data from the JSON file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.words = json.load(file)
        else:
            self.words = {}

    def saveData(self):
        """Save the current words data to the JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.words, file, ensure_ascii=False, indent=4)
    
    def add_word(self, chinese, pinyin, english):
        """Add a new word to the data and save it to the file."""
        word_id = f"word_{len(self.words) + 1}"
        self.words[word_id] = {
            "chinese": chinese,
            "pinyin": pinyin,
            "english": english
        }
        self.saveData()
        return word_id
