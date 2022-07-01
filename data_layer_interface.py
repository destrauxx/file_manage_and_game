from file_manager import FileManager
from game import save

file_manager = FileManager()

class DataInterface:
    def __init__(self) -> None:
        self.file_manager = FileManager()  
    
    def save_game_data(self):
        save_data = save()
        self.file_manager.save_data(save_data)

d = DataInterface()
d.save_game_data()