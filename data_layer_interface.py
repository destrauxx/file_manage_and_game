from file_manager import FileManager
from game import save, load

file_manager = FileManager()

class DataInterface:
    def __init__(self) -> None:
        self.file_manager = FileManager()  
    
    def save_game_data(self):
        save_data = save()
        self.file_manager.save_data(save_data)

    def load_game_data(self, name):
        load_data = self.file_manager.load_data(name)
        load(load_data)

d = DataInterface()
d.save_game_data()
d.load_game_data('level_3')