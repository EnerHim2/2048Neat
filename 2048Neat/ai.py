import pygame
import random 
import time 
import os   
import neat
import pickle
pygame.font.init()

BIG_HW = 970
BIG_PAD = 20
SMALL_HW = 170
SMALL_PAD = 2

TILE_HW = 40
STAT_FONT = pygame.font.SysFont("comicsans", 50)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

TILE_2 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "2.png")), (TILE_HW, TILE_HW))
TILE_4 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "4.png")), (TILE_HW, TILE_HW))
TILE_8 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "8.png")), (TILE_HW, TILE_HW))
TILE_16 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "16.png")), (TILE_HW, TILE_HW))
TILE_32 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "32.png")), (TILE_HW, TILE_HW))
TILE_64 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "64.png")), (TILE_HW, TILE_HW))
TILE_128 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "128.png")), (TILE_HW, TILE_HW))
TILE_256 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "256.png")), (TILE_HW, TILE_HW))
TILE_512 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "512.png")), (TILE_HW, TILE_HW))
TILE_1024 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "1024.png")), (TILE_HW, TILE_HW))
TILE_2048 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "2048.png")), (TILE_HW, TILE_HW))
TILE_4096 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "4096.png")), (TILE_HW, TILE_HW))
TILE_8192 = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "8192.png")), (TILE_HW, TILE_HW))
TILES = (TILE_2, TILE_4, TILE_8, TILE_16, TILE_32, TILE_64, TILE_128, TILE_256, TILE_512, TILE_1024, TILE_2048,
         TILE_4096, TILE_8192)
big_board = [[None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None],
             [None, None, None, None, None]]

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Tile:
    def __init__(self, board):
        self.x = random.randrange(len(board.boxes))
        self.y = random.randrange(len(board.boxes))
        while board.boxes[self.y][self.x] is not None:
            self.x = random.randrange(len(board.boxes))
            self.y = random.randrange(len(board.boxes))
        board.boxes[self.y][self.x] = self
        self.pos = (SMALL_PAD + self.x*(SMALL_PAD + TILE_HW) + board.x, SMALL_PAD + self.y*(SMALL_PAD + TILE_HW) + board.y)
        self.value = 0
        if random.random() > 0.9:
            self.value = 1
        self.img = TILES[self.value]

    def move_tile(self, x, y, board):
        self.pos = (SMALL_PAD + x*(SMALL_PAD + TILE_HW) + board.x, SMALL_PAD + y*(SMALL_PAD + TILE_HW) + board.y)

    def double_tile(self):
        self.value += 1
        self.img = TILES[self.value]

    def draw(self, win):
        win.blit(self.img, self.pos)

class Board:
    popped = False

    def __init__(self):
        while not self.popped:
            for y in range(len(big_board)):
                if self.popped:
                    break
                for x in range(len(big_board[y])):
                    if big_board[y][x] is None:
                        big_board[y][x] = self
                        self.x = BIG_PAD + x*(BIG_PAD + SMALL_HW)
                        self.y = BIG_PAD + y*(BIG_PAD + SMALL_HW)
                        self.popped = True
                        break
        self.boxes = [[None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None]]
    
    def board_full(self):
        for x in self.boxes:
            for y in x:
                if y is None:
                    return False
        return True

    def add_tile(self):
        if not self.board_full():
            Tile(self)

    def locked_board(self):
        if self.make_move("up", test=True) or self.make_move("down", test=True) or self.make_move("left", test=True) or self.make_move("right", test=True):
            return False
        else: return True

    def make_move(self, dir, test=False):
        made_move = False
        if dir == "up":
            for y in range(1, len(self.boxes)):
                for x in range(len(self.boxes)):
                    local_move = False
                    if self.boxes[y][x] is not None:
                        best_move = None
                        for i in reversed(range(y)):
                            if self.boxes[i][x] is None:
                                best_move = i
                                continue
                            elif self.boxes[i][x].value == self.boxes[y][x].value:
                                if self.boxes[i][x].value < len(TILES) - 1:
                                    if not test:
                                        self.boxes[y][x] = None
                                        self.boxes[i][x].double_tile()
                                    local_move = True
                                    made_move = True
                                break
                            else:
                                break
                        if best_move is not None and not local_move:
                            if not test:
                                self.boxes[y][x].move_tile(x, best_move, self)
                                self.boxes[best_move][x] = self.boxes[y][x]
                                self.boxes[y][x] = None
                            made_move = True
        if dir == "down":
            for y in reversed(range(len(self.boxes) - 1)):
                for x in range(len(self.boxes)):
                    local_move = False
                    if self.boxes[y][x] is not None:
                        best_move = None
                        for i in range(y + 1, len(self.boxes)):
                            if self.boxes[i][x] is None:
                                best_move = i
                                continue
                            elif self.boxes[i][x].value == self.boxes[y][x].value:
                                if self.boxes[i][x].value < len(TILES) - 1:
                                    if not test:
                                        self.boxes[y][x] = None
                                        self.boxes[i][x].double_tile()
                                    local_move = True
                                    made_move = True
                                break
                            else:
                                break
                        if best_move is not None and not local_move:
                            if not test:
                                self.boxes[y][x].move_tile(x, best_move, self)
                                self.boxes[best_move][x] = self.boxes[y][x]
                                self.boxes[y][x] = None
                            made_move = True
        if dir == "left":
            for x in range(1, len(self.boxes)):
                for y in range(len(self.boxes)):
                    local_move = False
                    if self.boxes[y][x] is not None:
                        best_move = None
                        for i in reversed(range(x)):
                            if self.boxes[y][i] is None:
                                best_move = i
                                continue
                            elif self.boxes[y][i].value == self.boxes[y][x].value:
                                if self.boxes[y][i].value < len(TILES) - 1:
                                    if not test:
                                        self.boxes[y][x] = None
                                        self.boxes[y][i].double_tile()
                                    local_move = True
                                    made_move = True
                                break
                            else:
                                break
                        if best_move is not None and not local_move:
                            if not test:
                                self.boxes[y][x].move_tile(best_move, y, self)
                                self.boxes[y][best_move] = self.boxes[y][x]
                                self.boxes[y][x] = None
                            made_move = True
        if dir == "right":
            for x in reversed(range(len(self.boxes) - 1)):
                for y in range(len(self.boxes)):
                    local_move = False
                    if self.boxes[y][x] is not None:
                        best_move = None
                        for i in range(x + 1, len(self.boxes)):
                            if self.boxes[y][i] is None:
                                # keep the best move y position stored and move it at the end
                                best_move = i
                                continue
                            elif self.boxes[y][i].value == self.boxes[y][x].value:
                                if self.boxes[y][i].value < len(TILES) - 1:
                                    if not test:
                                        self.boxes[y][x] = None
                                        self.boxes[y][i].double_tile()
                                    local_move = True
                                    made_move = True
                                break
                            else:
                                break
                        if best_move is not None and not local_move:
                            if not test:
                                self.boxes[y][x].move_tile(best_move, y, self)
                                self.boxes[y][best_move] = self.boxes[y][x]
                                self.boxes[y][x] = None
                            made_move = True

        # apply the move saved earlier if the def is not used as a test
        if made_move and not test:
            self.add_tile()
        return made_move

    def draw(self, win):
        pygame.draw.rect(win, [0, 0, 0], (0, 0, BIG_HW, BIG_HW))

def draw_window(win, boards):
    pygame.draw.rect(win, [0, 0, 0], (0, 0, BIG_HW, BIG_HW))

    for board in boards:
        board.draw(win)
        for line_board in board.boxes:
            for tile in line_board:
                if tile is not None:
                    tile.draw(win)

    pygame.display.update()

def main(genomes, config):
    global big_board
    big_board = [[None, None, None, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None],
                 [None, None, None, None, None]]
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((BIG_HW, BIG_HW))
    rem = []

    nets = []
    ge = []
    boards = []
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        boards.append(Board())
        g.fitness = 0
        ge.append(g)

    for board in boards:
        Tile(board)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit
                quit()

        for x, board in enumerate(boards):
            list_board = []
            for row in board.boxes:
                for i in row:
                    if i is not None:
                        list_board.append(i.value + 1)
                    else:
                        list_board.append(0)

            list_board = tuple(list_board)
            output = nets[x].activate(list_board)
            
            top_output = 0
            for i in range(4):
                if output[i] > output[top_output]:
                    top_output = i
            if top_output == 0:
                board.make_move("up")
            elif top_output == 1:
                board.make_move("down")
            elif top_output == 2:
                board.make_move("left")
            elif top_output == 3:
                board.make_move("right")

            new_list_board = []
            for row in board.boxes:
                for i in row:
                    if i is not None:
                        new_list_board.append(i.value + 1)
                    else:
                        new_list_board.append(0)
            new_list_board = tuple(new_list_board)

            if board.locked_board() or new_list_board == list_board:
                ge[x].fitness -= 5
                rem.append(board)
            else:
                addition = 0
                for i in range(len(list_board)):
                    addition += new_list_board[i] - list_board[i]
                ge[x].fitness += 0.1
                if addition > 0:
                    ge[x].fitness += addition

            if ge[x].fitness >= 150:
                pickle.dump(nets[0], open("best.pickle", "wb"))

        for x, board in enumerate(boards):
            if board in rem:
                boards.pop(x)
                nets.pop(x)
                ge.pop(x)

        if len(boards) < 1:
            run = False

        draw_window(win, boards)

def run(config_p):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_p)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,1000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)