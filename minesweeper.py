import random
class Board:
    PLAYING = 0
    WON = 1
    LOST = 2
    MINE = 9
    def __init__(self,size):
        self.size = size

        if size is 8:
            self.mine_count = 10
        elif size is 16:
            self.mine_count = 40

        random.seed(0)
        self.grid = [[0 for x in range(0,self.size)] for y in range(self.size)]
        self.shown_grid = [['?' for x in range(0,self.size)] for y in range(self.size)]
        self.create_bombs()
        self.init_vals()
        print(self.grid[1][0])


    def create_bombs(self):
        for x in range(self.mine_count):

            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)

            while self.grid[row][col] is self.MINE:
                row = random.randint(0,self.size-1)
                col = random.randint(0,self.size-1)
            self.grid[row][col] = self.MINE


    def pretty_print(self, show_all = False, show_mines = False):
        for row in range(len(self.grid)):
            print('-'  * len(self.grid[0]) * 2)
            print('|', end='')
            for col in range(len(self.grid[row])):
                if not show_all:
                    if self.grid[row][col] is self.MINE and show_mines:

                        print(self.grid[row][col], end='|')
                            
                    else:
                        print(self.shown_grid[row][col], end='|')
                else:
                    print(self.grid[row][col], end='|')
            print(' ')  # To change lines 
        print('-' * (len(self.grid[0])) * 2)


    def init_vals(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] is not self.MINE:
                    c_row = y - 1
                    c_col = x - 1
                    sum = 0

                    for c in range(8):
                        if (c_row >= 0 and c_row < self.size) and (c_col >= 0 and c_col < self.size):
                            if self.grid[c_row][c_col] is self.MINE:
                                sum += 1

                        if c < 2:
                            c_col += 1
                        elif c < 4:
                            c_row += 1
                        elif c < 6:
                            c_col -= 1
                        else:
                            c_row -= 1
                    self.grid[y][x] = sum

    def find_neighbors(self,x,y):

        if self.grid[y][x] is 0:

            c_row = y - 1
            c_col = x - 1
            for c in range(8):
                if (c_row >= 0 and c_row < self.size) and (c_col >= 0 and c_col < self.size):
                    if type(self.shown_grid[c_row][c_col]) is str:
                        self.shown_grid[y][x] = self.grid[y][x]

                        self.find_neighbors(c_col,c_row)


                if c < 2:
                    c_col += 1
                elif c < 4:
                    c_row += 1
                elif c < 6:
                    c_col -= 1
                else:
                    c_row -= 1


        self.shown_grid[y][x] = self.grid[y][x]

    def process_comm(self,resp):
        resp.replace(" ", "")
        comma_i = resp.find(",")
        if comma_i is not -1:

            col = int(resp[comma_i - 1])
            row = int(resp[comma_i + 1])

            return (col,row, '-f' in resp)

        else:
            return False

    def do_move(self,info):

        (col,row,flag) = info
        if not (row >= 0 and row < self.size) or not (col >= 0 and col < self.size):
            return False

        if self.shown_grid[row][col] is not '?' and self.shown_grid[row][col] is not '?*':
            return False
        if flag:
            if type(self.shown_grid[row][col]) is str:
                if '*' not in self.shown_grid[row][col]:
                    self.shown_grid[row][col] = '?*'
                else:
                    self.shown_grid[row][col] = '?'
            else:
                return False
        else:
            self.find_neighbors(col, row)

        return True


    def check_game_status(self,info):
        (col,row,flag) = info

        if flag:
            for y in range(self.size):
                for x in range(self.size):
                    if self.grid[y][x] is self.MINE and '*' not in self.shown_grid[y][x] or (self.grid[y][x] is not self.MINE and '*' in self.shown_grid[y][x]):
                        return self.PLAYING



            return self.WON

        if self.shown_grid[row][col] is self.MINE:
                return self.LOST
        else:
            return self.PLAYING



