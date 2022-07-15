from time import sleep
from tkinter import *
from config import CANVAS_SIZE, BG_COLOR, EMPTY, FIELD_SIZE, RECT_SIZE
from random import randint


class Board(Tk):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas(
            width=CANVAS_SIZE, height=CANVAS_SIZE, bg=BG_COLOR)
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
        self.field_size = board.get_field_size()
        self.rect_size = RECT_SIZE
        self.player_positions = [[self.field_size//2-1, self.field_size//2-1]]
        # self.player_positions[0][1] = [self.field_size//2-1]
        self.player_coords = [[self.player_positions[0][0] * self.rect_size, self.player_positions[0][1] * self.rect_size]]
        self.player_parts_tags = []
        self.snake = self.render_player()
        board.canvas.bind_all('<KeyPress>', self.change_direction)
        self.snake_direction = ''

    def build_player_on_grid(self):
        board.field[self.player_positions[0][0]][self.player_positions[0][1]] = 'player'
        # for position in self.player_positions:
        #     board.field[position[0]][position[1]] = 'player'

    def render_player(self):
        '''
        Отрисовывает игрока на игровом поле
        '''
        r_size = self.rect_size
        self.build_player_on_grid()
        x = self.player_coords[0][0]
        y = self.player_coords[0][1]
        self.player_parts_tags.append(
            board.canvas.create_rectangle(x, y, x + r_size, y + r_size, fill='green')
            )

    # def render_new_part(self):    

    def change_direction(self, event):
        '''
        Изменяет направление движения по кнопке
        '''

        if (event.keysym == 'Up' or event.keysym == 'w') and self.snake_direction != 'down':
            self.snake_direction = 'up'

        if (event.keysym == 'Down' or event.keysym == 's') and self.snake_direction != 'up':
            self.snake_direction = 'down'

        if (event.keysym == 'Right' or event.keysym == 'd') and self.snake_direction != 'left':
            self.snake_direction = 'right'

        if (event.keysym == 'Left' or event.keysym == 'a') and self.snake_direction != 'right':
            self.snake_direction = 'left'

    def move(self, apple):
        '''
        Постоянно смещает змейку в сторону направления движения
        '''
        field = board.field
        r_size = self.rect_size
        field_size = self.field_size
        snake_direction = self.snake_direction

        if snake_direction == 'up':
            self.player_positions[-1][1] = self.player_positions[0][1] - 1
            apple_eated = self.check_apple_eat(apple)

            if self.player_positions[0][1] < 0:
                for snake_part in self.player_parts_tags:
                    board.canvas.delete(snake_part)
            elif field[self.player_positions[0][0]][self.player_positions[0][1]] == 'empty':
                if apple_eated:
                    print('APPLE EATED!')
                    self.player_positions.append([self.player_positions[-1][0], self.player_positions[-1][1] + 1])
                    field[self.player_positions[-1][0]][self.player_positions[-1][1]] = 'player'
                    self.player_coords.append([self.player_positions[-1][0] * r_size, self.player_positions[-1][1] * r_size])
                    self.player_parts_tags.append(
                        board.canvas.create_rectangle(
                            self.player_coords[-1][0], self.player_coords[-1][1], self.player_coords[-1][0] + r_size, self.player_coords[-1][1] + r_size, fill='green')
                    )
                else:
                    field[self.player_positions[0][0]][self.player_positions[0][1] + 1] = 'empty'

                board.canvas.move(self.player_parts_tags[-1], self.player_coords[0][0] - self.player_coords[-1][0], self.player_coords[0][1] - r_size - self.player_coords[-1][1])

                # field[self.player_positions[0][0]][self.player_positions[0][1]] = 'player'
                last_player_coords = self.player_coords.pop()
                last_player_position = self.player_positions.pop()
                last_player_tag = self.player_parts_tags.pop()
                self.player_coords.insert(0, last_player_coords)
                self.player_positions.insert(0, last_player_position)
                self.player_parts_tags.insert(0, last_player_tag)

                self.player_coords[0][1] -= r_size
                print(self.player_coords, self.player_positions, self.player_parts_tags)

        if snake_direction == 'down':
            self.player_positions[0][1] += 1
            if self.player_positions[0][1] > field_size - 2:
                self.player_positions[0][1] -= 1
            apple_eated = self.check_apple_eat(apple)

            if field[self.player_positions[0][0]][self.player_positions[0][1]] == 'empty':
                field[self.player_positions[0][0]][self.player_positions[0][1] - 1] = 'empty'
                field[self.player_positions[0][0]][self.player_positions[0][1]] = 'player'
                self.player_coords[0][1] += r_size
                board.canvas.move(self.player_parts_tags[0], 0, r_size)

        if snake_direction == 'left':
            self.player_positions[0][0] -= 1
            apple_eated = self.check_apple_eat(apple)

            if field[self.player_positions[0][0]][self.player_positions[0][1]] != 'empty' or self.player_positions[0][0] < 0:
                self.player_positions[0][0] += 1
            elif field[self.player_positions[0][0]][self.player_positions[0][1]] == 'empty':
                field[self.player_positions[0][0] + 1][self.player_positions[0][1]] = 'empty'
                field[self.player_positions[0][0]][self.player_positions[0][1]] = 'player'
                self.player_coords[0][0] -= r_size
                board.canvas.move(self.player_parts_tags[0], -r_size, 0)

        if snake_direction == 'right':
            self.player_positions[0][0] += 1
            if self.player_positions[0][0] > field_size - 2:
                self.player_positions[0][0] -= 1
            apple_eated = self.check_apple_eat(apple)

            if field[self.player_positions[0][0]][self.player_positions[0][1]] == 'empty':
                field[self.player_positions[0][0] - 1][self.player_positions[0][1]] = 'empty'
                field[self.player_positions[0][0]][self.player_positions[0][1]] = 'player'
                self.player_coords[0][0] += r_size
                board.canvas.move(self.player_parts_tags[0], r_size, 0)
        # print('[OUT]', self.player_coords, self.player_positions, self.player_parts_tags)
        return apple

    def check_apple_eat(self, apple):
        field = board.field
        if field[self.player_positions[-1][0]][self.player_positions[-1][1]] == 'apple':
            board.field[self.player_positions[-1][0]][self.player_positions[-1][1]] = 'empty'
            apple.destrukt_apple()
            apple.place_apple()
            return True
        return False

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

        while board.field[row][col] != 'empty':
            row = randint(0, field_size-2)
            col = randint(0, field_size-2)

        x = row * apple_size
        y = col * apple_size
        board.field[row][col] = 'apple'
        self.apple = board.canvas.create_rectangle(
            x, y, x + apple_size, y + apple_size, fill='red')

    def destrukt_apple(self):
        board.canvas.delete(self.apple)

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
