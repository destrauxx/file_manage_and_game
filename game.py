from time import sleep
from tkinter import *
from config import CANVAS_SIZE, BG_COLOR, EMPTY, FIELD_SIZE, RECT_SIZE
from random import randint

class Board(Tk):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas(width=CANVAS_SIZE, height=CANVAS_SIZE, bg=BG_COLOR)
        self.canvas.pack()
        self.field_size = FIELD_SIZE
        self.field = self.build_field_grid()
    
    def build_field_grid(self):
        '''
        Строит сетку поля по заданным данным (размер клетки, размер поля)
        '''
        row = [EMPTY] * self.field_size
        col = []
        for _ in range(self.field_size): 
            col.append(row[:])
        return col  
    
    def get_field_size(self):
        return self.field_size

board = Board()

class Snake():
    def __init__(self):
        self.field_size = FIELD_SIZE
        self.rect_size = RECT_SIZE
        self.player_pos_row = randint(0, self.field_size-2)
        self.player_pos_col = randint(0, self.field_size-2)
        self.player_x = self.player_pos_row * self.rect_size
        self.player_y = self.player_pos_col * self.rect_size
        self.snake = self.render_player()
        board.canvas.bind_all('<KeyPress>', self.change_direction)
        self.player_direction = ''

    def build_player_on_grid(self):
        board.field[self.player_pos_row][self.player_pos_row] = 'player'

    def render_player(self):
        '''
        Отрисовывает игрока на игровом поле
        '''
        r_size = self.rect_size
        self.build_player_on_grid()
        player = board.canvas.create_rectangle(self.player_x, self.player_y, self.player_x + r_size, self.player_y + r_size, fill='white')
        return player

    def change_direction(self, event):
        '''
        Изменяет направление движения по кнопке
        '''
        
        if (event.keysym == 'Up' or event.keysym == 'w') and self.player_direction != 'down':
            self.player_direction = 'up'

        if (event.keysym == 'Down' or event.keysym == 's') and self.player_direction != 'up':
            self.player_direction = 'down'

        if (event.keysym == 'Right' or event.keysym == 'd') and self.player_direction != 'left':
            self.player_direction = 'right'

        if (event.keysym == 'Left' or event.keysym == 'a') and self.player_direction != 'right':
            self.player_direction = 'left'
   
    def move(self, apple):
        '''
        Постоянно смещает змейку в сторону направления движения
        '''
        field = board.field
        r_size = self.rect_size
        field_size = self.field_size
        player_direction = self.player_direction

        if player_direction == 'up':
            self.player_pos_col -= 1
            self.check_apple_eat(apple)

            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_col < 0:
                self.player_pos_col += 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row][self.player_pos_col + 1] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                board.canvas.move(self.snake, 0, -r_size)

        if player_direction == 'down':
            self.player_pos_col += 1
            self.check_apple_eat(apple)

            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_col > field_size - 2:
                self.player_pos_col -= 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row][self.player_pos_col - 1] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                board.canvas.move(self.snake, 0, r_size)

        if player_direction == 'left':
            self.player_pos_row -= 1
            self.check_apple_eat(apple)

            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_row < 0:
                self.player_pos_row += 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row + 1][self.player_pos_col] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                board.canvas.move(self.snake, -r_size, 0)

        if player_direction == 'right':
            self.player_pos_row += 1
            self.check_apple_eat(apple)

            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_row > field_size - 2:
                self.player_pos_row -= 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row - 1][self.player_pos_col] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                board.canvas.move(self.snake, r_size, 0)

        return apple

    def check_apple_eat(self, apple):
        field = board.field
        if field[self.player_pos_row][self.player_pos_col] == 'apple':
            board.field[self.player_pos_row][self.player_pos_col] = 'empty'
            board.canvas.delete(apple)
            print(board.canvas.find_all())
            apple.place_apple()

snake = Snake()

class Apple():
    def __init__(self):
        self.apple_size = RECT_SIZE
        self.field_size = board.get_field_size()

    def place_apple(self):
        row = randint(0, self.field_size-2)
        col = randint(0, self.field_size-2)
        field_size = self.field_size
        apple_size = self.apple_size

        while row == snake.player_pos_row or col == snake.player_pos_row:
            row = randint(0, field_size-2)
            col = randint(0, field_size-2)

        x = row * apple_size
        y = col * apple_size
        board.field[row][col] = 'apple'
        self.apple = board.canvas.create_rectangle(x, y, x + apple_size, y + apple_size, fill='red')
        self.tag = f'apple#{self.apple}'
        print(self.tag)
    
apple = Apple()
apple.place_apple()

while True:
    apple = snake.move(apple)
    board.update()
    sleep(0.1)

def save():
    return {
        "level": 1,
        "obstacles": {
            "easy": 10,
            "medium": 15,
            "hard": 5,
        },
        "word": "orange"
}

def load(data):
    print(data)
