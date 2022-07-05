from tkinter import *
from random import randint
#& C:/Users/Виталий/AppData/Local/Programs/Python/Python38-32/python.exe "c:/Python vol 2/Labirint.py"
# Constants
CANVAS_SIZE = 600
RECT_SIZE = CANVAS_SIZE // 20
RATIO = CANVAS_SIZE // RECT_SIZE + 1
BG_COLOR = 'black'
PLAYER_X = CANVAS_SIZE // 2 - RECT_SIZE + 3
PLAYER_Y = CANVAS_SIZE // 2 - RECT_SIZE + 3
EMPTY = 'empty'

class Board(Tk):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas(width=CANVAS_SIZE, height=CANVAS_SIZE, bg='white')
        self.canvas.pack()
        # self.canvas.title('The Aquarius: The Third Chapter - February')
        self.rect_size = RECT_SIZE
        self.player_pos_row = 9
        self.player_pos_col = 9
        self.player_x = CANVAS_SIZE // 2 - RECT_SIZE + 3
        self.player_y = CANVAS_SIZE // 2 - RECT_SIZE + 3
        self.ratio = RATIO
        self.empty = EMPTY
        self.canvas.bind_all('<KeyPress>', self.player_move)
        self.pole = self.build_obstacles()
        self.player = self.render_player()

    def build_grid(self):
        row = [self.empty] * self.ratio
        col = []
        for _ in range(self.ratio): 
            col.append(row[:])
        return col

    def build_obstacles(self):
        '''Magic number: 3, its a gap between edges and figure
        '''
        field = self.build_grid()
        chance = 25
        

        for r in range(self.ratio):
            for c in range(self.ratio):
                r_num = randint(0, 100)
                if r_num <= chance:
                    field[r][c] = 'obst'
        return field
        
    def render_obstacles(self):
        field = self.pole
        r_size = self.rect_size - 3
        x1 = 3
        y1 = 3
        x2 = r_size
        y2 = r_size
        for r in range(self.ratio):
            for c in range(self.ratio):
                if field[r][c] == 'obst':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green')
                y1 += r_size + 3
                y2 += r_size + 3
            y1 = 3
            y2 = r_size
            x1 += r_size + 3
            x2 += r_size + 3
        return field

    def render_player(self):
        '''Magic number: 6, its a gap between edges and figure
        Render player on field
        '''
        r_size = self.rect_size - 6
        field = self.pole
        field[self.player_pos_row][self.player_pos_col] = 'player'
        for r in range(self.ratio):
            for c in range(self.ratio):
                if field[r][c] == 'player':
                    player = self.canvas.create_oval(self.player_x, self.player_y, self.player_x + r_size, self.player_y + r_size, fill='brown')
        return player

    def player_move(self, event):
        '''Magic number: 6, its a gap between edges and figure
        Render player on field
        '''
        field = self.pole
        r_size = self.rect_size
        
        if event.keysym == 'Up' or event.keysym == 'w':
            self.player_pos_col -= 1
            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_col < 0:
                self.player_pos_col += 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row][self.player_pos_col + 1] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                self.canvas.move(self.player, 0, -r_size)


        if event.keysym == 'Down' or event.keysym == 's':
            self.player_pos_col += 1
            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_col > 19:
                self.player_pos_col -= 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row][self.player_pos_col - 1] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                self.canvas.move(self.player, 0, r_size)


        if event.keysym == 'Right' or event.keysym == 'd':
            self.player_pos_row += 1
            
            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_row > 19:
                    self.player_pos_row -= 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row - 1][self.player_pos_col] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                self.canvas.move(self.player, r_size, 0)

        if event.keysym == 'Left' or event.keysym == 'a':
            self.player_pos_row -= 1
            if field[self.player_pos_row][self.player_pos_col] != 'empty' or self.player_pos_row < 0:
                self.player_pos_row += 1
            elif field[self.player_pos_row][self.player_pos_col] == 'empty':
                field[self.player_pos_row + 1][self.player_pos_col] = 'empty'
                field[self.player_pos_row][self.player_pos_col] = 'player'
                self.canvas.move(self.player, -r_size, 0)
board = Board()

board.render_obstacles()
    
board.mainloop()