from settings import *

pg.init()

font_numbers = pg.font.SysFont(None, 45)
font_title = pg.font.SysFont(None, 80)
font_text = pg.font.SysFont(None, 38)

class Grid:
    def __init__(self):
        self.x = WIDTH // 6
        self.y = HEIGHT // 6
        self.color = BLACK
        self.lenght = 2 * WIDTH // 3 - 4
        self.square_l = self.lenght // 9
        self.number_positions = self.get_positions()
        self.solution = self.get_matrix()
        self.sudoku = self.get_zeros(self.solution)
        self.locked_cells = self.get_locked_cells()
        self.player_entries = {}
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        music_path = os.path.join(base_path, 'music')
        self.play_list = [os.path.join(music_path, file) for file in os.listdir(music_path) if file.endswith('.mp3')]
        self.current_list = []
        random.shuffle(self.play_list)
        self.paused = False

    def draw_grid(self):
        for i in range(10):
            thickness = 2
            if i % 3 == 0:
                thickness += 4
            pg.draw.line(screen, self.color, (self.x, self.y + (i * self.square_l)), (self.x + self.lenght, self.y + (i * self.square_l)), thickness)
            pg.draw.line(screen, self.color, (self.x + (i * self.square_l), self.y), (self.x + (i * self.square_l), self.y + self.lenght), thickness)

    def get_positions(self):
        positions = [[None for _ in range(9)] for _ in range(9)]
        padding = self.square_l // 3
        for i in range(9):
            for j in range(9):
                positions[i][j] = (self.x + (j * self.square_l) + padding + 3, self.y + (i * self.square_l) + padding - 1)
        return positions

    def get_matrix(self):
        base  = 3
        side  = base*base
        def pattern(r,c): return (base*(r%base)+r//base+c)%side
        def shuffle(s): return sample(s,len(s)) 
        rBase = range(base) 
        rows  = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)] 
        cols  = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums  = shuffle(range(1,base*base+1))
        board = [[nums[pattern(r,c)] for c in cols] for r in rows]
        return board

    def get_zeros(self, matrix):
        while True:
            counter = random.randint(40, 60)
            matrix_zeros = [[j for j in i] for i in matrix]
            while counter > 0:
                matrix_zeros[random.randint(0, 8)][random.randint(0, 8)] = 0
                counter -= 1
            self.sudoku = matrix_zeros
            if self.has_unique_solution():
                break

        return self.sudoku

    def fill_grid(self):
        for i in range(9):
            for j in range(9):
                number = self.sudoku[i][j]
                if number == 0:
                    continue
                if (i, j) in self.player_entries:
                    if self.check_number(i, j):
                        number_text = font_numbers.render(str(number), True, BLUE)
                    else:
                        number_text = font_numbers.render(str(number), True, RED)
                else:
                    number_text = font_numbers.render(str(number), True, BLACK)
                screen.blit(number_text, self.number_positions[i][j])

    def update_numbers(self, player, number):
        if (player.y_current, player.x_current) not in self.locked_cells:
            self.sudoku[player.y_current][player.x_current] = number
            self.player_entries[(player.y_current, player.x_current)] = number

    def count_solutions(self, board):
        empty = self.find_empty_cell(board)
        if not empty:
            return 1  
        row, col = empty
        count = 0
        for num in range(1, 10):
            if self.is_valid_move(board, num, row, col):
                board[row][col] = num
                count += self.count_solutions(board)
                if count > 1:
                    break
                board[row][col] = 0

        return count

    def find_empty_cell(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def is_valid_move(self, board, num, row, col):
        if num in board[row]:
            return False
        if num in [board[i][col] for i in range(9)]:
            return False
        box_x, box_y = col // 3, row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num:
                    return False
        return True

    def has_unique_solution(self):
        board_copy = [row[:] for row in self.sudoku]
        return self.count_solutions(board_copy) == 1
    
    def get_locked_cells(self):
        locked = set()
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] != 0:
                    locked.add((i, j))
        return locked

    def check_number(self, i, j):
        if (i, j) in self.player_entries:
            return self.player_entries[(i, j)] == self.solution[i][j]
        return False
    
    def play_music(self):
        if not self.paused and not pg.mixer.music.get_busy(): 
            if not self.current_list:
                self.current_list = self.play_list[:]
                random.shuffle(self.current_list)
            current_song = self.current_list.pop(0)
            pg.mixer.music.load(current_song)
            pg.mixer.music.play()

class Player:
    def __init__(self, grid):
        self.tile_lenght = grid.square_l
        self.positions = [[(WIDTH // 6 + i * self.tile_lenght, HEIGHT // 6 + j * self.tile_lenght) for j in range(9)] for i in range(9)]
        self.x_current = 0
        self.y_current = 0
        self.x = self.positions[self.x_current][self.y_current][0]
        self.y = self.positions[self.x_current][self.y_current][1]
        self.color = GRAY
        self.lives = 3
    
    def draw(self):
        pg.draw.rect(screen, self.color, pg.Rect(self.x, self.y, self.tile_lenght, self.tile_lenght))
    
    def move(self, dx, dy):
        if dx + self.x_current < 9 and dx + self.x_current >= 0:
            self.x_current += dx 
        if dy + self.y_current < 9 and dy + self.y_current >= 0:
            self.y_current += dy
        self.x = self.positions[self.x_current][self.y_current][0]
        self.y = self.positions[self.x_current][self.y_current][1]

    def round(self, grid):
        running = True
        while running:
            if self.lives <= 0:
                end_message = "Game over. Press Enter to try again."
                running = False
            elif grid.sudoku == grid.solution:
                end_message = "You won! Press Enter to play again."
                running = False

            if running:
                screen.fill(WHITE)
                self.draw()
                grid.draw_grid()
                grid.fill_grid()

                number_text = font_title.render("Sudoku!", True, BLACK)
                screen.blit(number_text, (WIDTH * 5 // 16, HEIGHT * 3 // 48))
                lives_text = font_text.render(f"Lives: {self.lives}", True, BLACK)
                screen.blit(lives_text, (WIDTH // 36, HEIGHT * 62 // 72))
                errase_text = font_text.render(f"Press 0 to errase.", True, BLACK)
                screen.blit(errase_text, (WIDTH // 36, HEIGHT * 65 // 72))
                errase_text = font_text.render(f"Press Q to turn on/off the music.", True, BLACK)
                screen.blit(errase_text, (WIDTH // 36, HEIGHT * 68 // 72))

                pg.mixer.music.set_endevent(pg.USEREVENT)
                grid.play_music()
                music = pg.mixer.music.get_busy()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.USEREVENT:
                        grid.play_music()
                    elif event.type == pg.KEYDOWN:
                        if event.key in (pg.K_UP, pg.K_w):
                            self.move(0, -1)
                        elif event.key in (pg.K_DOWN, pg.K_s):
                            self.move(0, 1)
                        elif event.key in (pg.K_LEFT, pg.K_a):
                            self.move(-1, 0)
                        elif event.key in (pg.K_RIGHT, pg.K_d):
                            self.move(1, 0)
                        elif event.key in key_to_number:
                            number = key_to_number[event.key]
                            grid.update_numbers(self, number)
                            if number != 0:
                                if not grid.check_number(self.y_current, self.x_current):
                                    self.lives -= 1
                        elif event.key == pg.K_q:
                            if music:
                                pg.mixer.music.pause()
                                grid.paused = True
                            else:
                                pg.mixer.music.unpause()
                                grid.paused = False
                            music = not music

                pg.display.flip()
                clock.tick(FPS)
        
        while True:
            screen.fill(WHITE)
            message_text = font_numbers.render(end_message, True, BLACK)
            screen.blit(message_text, (1 * WIDTH // 6, HEIGHT // 2))
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    return
