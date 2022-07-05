import pickle
import os
from config import BASE_DIR


class FileManager:

    def check_data_folder_exists_decorator(func):
        def wrapper(self, data, *args, **kwargs):
            if not os.path.exists(f'{BASE_DIR}/data'):
                os.mkdir('data')
            func(self, data)
        return wrapper

    def load_data(self, name):
        with open('data/' + name, 'rb') as f:
            return pickle.load(f)

    @check_data_folder_exists_decorator
    def save_data(self, data):
        with open(f'data/level_{data["level"]}', 'wb') as f:
            pickle.dump(data, f)

f = FileManager()

test_data = {
    "level": 1,
    "obstacles": {
        "easy": 10,
        "medium": 15,
        "hard": 5,
    },
    "word": "orange"
}

f.save_data(test_data)

data = f.load_data('level_1')
print(data)

print(os.path.exists(f'{os.path.dirname(__file__)}/data'))