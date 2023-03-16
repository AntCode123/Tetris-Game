#importing modules
import pygame, sys, threading, random, time


#setup
pygame.init()
wn = pygame.display.set_mode((300, 300))
wn.fill((0, 0, 0))
clock = pygame.time.Clock()
try:
    joystick = pygame.joystick.Joystick(0)
except:
    pass


#fonts
score_font = pygame.font.SysFont("calbri", 30, False)
next_shape_font = pygame.font.SysFont("calbri", 30, False)
game_over_font = pygame.font.SysFont("calbri", 25, False)


#Game class
class Game:
    def __init__(self):
        self.FPS = 400
        self.score = 0
        self.state = "playing"
        self.positions_taken = []
        self.field_blocks = []
        self.row_blocks = []
        self.end_blocks = []
        self.colors = {"red":(180, 0, 0), "green":(0, 180, 0), "blue":(8, 43, 193), "orange":(255, 125, 0), "yellow":(255, 255, 0), "purple":(255, 0, 255), "cyan":(0, 255, 255)}


    #handling events/input from user
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause()
                if self.state == "playing":
                    if event.key == pygame.K_a: figure.move(-15)
                    if event.key == pygame.K_d: figure.move(15)
                    if event.key == pygame.K_r: figure.rotate()
                    if event.key == pygame.K_s: figure.fall_speed = 0.01
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 3: self.pause()
                if self.state == "playing":
                    if event.button == 0: figure.fall_speed = 0.005
                    if event.button == 1: figure.rotate()
            if event.type == pygame.JOYHATMOTION:
                if self.state == "playing":
                    if event.value == (-1, 0):figure.move(-15)
                    if event.value == (1, 0):figure.move(15)


    #pausing and resuming the game
    def pause(self):
        if self.state == "playing": self.state = "paused"
        else:
            self.state = "playing"
            figure.fall()


    #checking if the game is over
    def check_game_over(self):
        for block in figure.shape:
            if (block.x, block.y) in self.positions_taken:
                self.state = "end animation"


    #end block animation
    def end_animation(self):
        for i in range(10):
            for j in range(20):
                x = i * 15
                y = j * 15
                self.end_blocks.append(Block(x, y, (255, random.randint(80, 230), 0)))
                wn.fill((0, 0, 0))
                self.render()
                self.display_text()
                for block in self.end_blocks:
                    pygame.draw.rect(wn, block.color, (block.x + 0.5, block.y + 0.5, 14, 14), border_radius = 3)
                pygame.display.update()
                pygame.time.wait(5)
        self.state = "game over"
        self.field_blocks.clear()
        figure.ghost.clear()
        figure.shape.clear()
        figure.next_shape.clear()
                

    #drawing the blocks to the window
    def draw_blocks(self):
        for block in figure.ghost: pygame.draw.rect(wn, (255, 255, 255), (block.x, block.y, 14, 14), 2, border_radius = 3)
        for block in figure.shape: pygame.draw.rect(wn, (255, 125, 0), (block.x, block.y, 14, 14), border_radius = 3)
        for block in self.field_blocks: pygame.draw.rect(wn, (255, 125, 0), (block.x, block.y, 14, 14), border_radius = 3)
        if self.state != "end animation":
            for block in figure.next_shape: pygame.draw.rect(wn, (255, 125, 0), (block.x, block.y, 14, 14), border_radius = 3)
            

    #displaying text to window
    def display_text(self):
        score_text = score_font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        next_shape_text = next_shape_font.render(f"NEXT SHAPE", True, (255, 255, 255))
        wn.blit(score_text, (160, 10))
        wn.blit(next_shape_text, (160, 80))
        if self.state == "game over":
            game_text = game_over_font.render(f"GAME", True, (255, 255, 255))
            over_text = game_over_font.render(f"OVER", True, (255, 255, 255))
            wn.blit(game_text, (193, 133))
            wn.blit(over_text, (195, 153))


    #rendering all objects to the window
    def render(self):
        field.draw()
        self.draw_blocks()
        pygame.draw.rect(wn, (255, 255, 255), (170, 121, 100, 60), 4)


    #updating the window
    def update(self):
        pygame.display.update()
        wn.fill((0, 0, 0))
        clock.tick(self.FPS)



#Field class
class Field:
    def __init__(self):
        self.grid = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] for j in range(20)]
        self.grid.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])


    #configuring the field
    def configure(self):
        for i in range(21):
            for j in range(12):
                if self.grid[i][j] == 1:
                    x = -15 + j * 15
                    y = i * 15
                    game.positions_taken.append((x, y))


    #drawing the field
    def draw(self):
        for i in range(20):
            for j in range(10):
                x = j * 15
                y = i * 15
                pygame.draw.rect(wn, (50, 55, 72), (x, y, 14, 14))


    #updating the field
    def update(self):
        for block in figure.shape:
            i = (block.y) // 15
            j = (block.x + 15) // 15
            self.grid[i][j] = 1
            game.positions_taken.append((block.x, block.y))
            game.field_blocks.append(block)
            

    #refreshing the field
    def refresh(self):
        for i in range(21):
            for j in range(12):
                if self.grid[i][j] == 1:
                    x = -15 + j * 15
                    y = i * 15
                    game.positions_taken.append((x, y))


    #removing the complete row and dropping everything above down
    def drop_and_remove(self):
        for i in range(20):
            y_row_position = i * 15 
            row = self.grid[i]
            row_blocks = []
            if row == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
                for block in game.field_blocks:
                    if block.y < y_row_position: block.y += 15
                    elif block.y == y_row_position: block.x = 1000
                self.grid.remove(row)
                self.grid.insert(0, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
                game.positions_taken.clear()
                game.score += 1
                self.refresh()
    

#Figure class
class Figure:
    def __init__(self):
        self.next_letter = None
        self.shape = None
        self.ghost = None
        self.centre_rotation = None


    #shuffle the next set of letters
    def create_letters_set(self):
        self.letters_list = ["I", "L", "J", "S", "Z", "T", "O"]
        random.shuffle(self.letters_list)
        self.letters_count = 0

        
    #finding the next figure
    def next(self):
        if figure.letters_count == 7:
            figure.create_letters_set()
        self.next_letter = random.choice(self.letters_list)
        offset = 137
        if self.next_letter == "I": self.next_shape = [Block(53 + offset, 8 + offset, game.colors["cyan"]), Block(68 + offset, 8 + offset, game.colors["cyan"]), Block(83 + offset,  8 + offset, game.colors["cyan"]), Block(98 + offset, 8 + offset, game.colors["cyan"])]
        elif self.next_letter == "L": self.next_shape = [Block(60 + offset, 15 + offset, game.colors["orange"]), Block(75 + offset, 15 + offset, game.colors["orange"]), Block(90 + offset, 15 + offset, game.colors["orange"]), Block(90 + offset, 0 + offset, game.colors["orange"])]
        elif self.next_letter == "J": self.next_shape = [Block(60 + offset, 0 + offset, game.colors["blue"]), Block(60 + offset, 15 + offset, game.colors["blue"]), Block(75 + offset, 15 + offset, game.colors["blue"]), Block(90 + offset, 15 + offset, game.colors["blue"])]
        elif self.next_letter == "S": self.next_shape = [Block(60 + offset, 15 + offset, game.colors["green"]), Block(75 + offset, 15 + offset, game.colors["green"]), Block(75 + offset, 0 + offset, game.colors["green"]), Block(90 + offset, 0 + offset, game.colors["green"])]
        elif self.next_letter == "Z": self.next_shape = [Block(60 + offset, 0 + offset, game.colors["red"]), Block(75 + offset, 0 + offset, game.colors["red"]), Block(75 + offset, 15 + offset, game.colors["red"]), Block(90 + offset, 15 + offset, game.colors["red"])]
        elif self.next_letter == "T": self.next_shape = [Block(60 + offset, 15 + offset, game.colors["purple"]), Block(75 + offset, 15 + offset, game.colors["purple"]), Block(75 + offset, 0 + offset, game.colors["purple"]), Block(90 + offset, 15 + offset, game.colors["purple"])]
        elif self.next_letter == "O": self.next_shape = [Block(68 + offset, 15 + offset, game.colors["yellow"]), Block(68 + offset, 0 + offset, game.colors["yellow"]), Block(83 + offset, 15 + offset, game.colors["yellow"]), Block(83 + offset, 0 + offset, game.colors["yellow"])]

    #adding new figure
    def add(self):
        self.letter = self.next_letter
        if self.letter == "I":
            self.shape = [Block(45, 0, game.colors["cyan"]), Block(60, 0, game.colors["cyan"]), Block(75, 0, game.colors["cyan"]), Block(90, 0, game.colors["cyan"])]
            self.ghost = [Block(45, 0, game.colors["cyan"]), Block(60, 0, game.colors["cyan"]), Block(75, 0, game.colors["cyan"]), Block(90, 0, game.colors["cyan"])]
            self.centre_rotation = [60, 0]
        elif self.letter == "L":
            self.shape = [Block(45, 15, game.colors["orange"]), Block(60, 15, game.colors["orange"]), Block(75, 15, game.colors["orange"]), Block(75, 0, game.colors["orange"])]
            self.ghost = [Block(45, 15, game.colors["orange"]), Block(60, 15, game.colors["orange"]), Block(75, 15, game.colors["orange"]), Block(75, 0, game.colors["orange"])]
            self.centre_rotation = [60, 15]
        elif self.letter == "J":
            self.shape = [Block(45, 0, game.colors["blue"]), Block(45, 15, game.colors["blue"]), Block(60, 15, game.colors["blue"]), Block(75, 15, game.colors["blue"])]
            self.ghost = [Block(45, 0, game.colors["blue"]), Block(45, 15, game.colors["blue"]), Block(60, 15, game.colors["blue"]), Block(75, 15, game.colors["blue"])]
            self.centre_rotation = [60, 15]
        elif self.letter == "S":
            self.shape = [Block(45, 15, game.colors["green"]), Block(60, 15, game.colors["green"]), Block(60, 0, game.colors["green"]), Block(75, 0, game.colors["green"])]
            self.ghost = [Block(45, 15, game.colors["green"]), Block(60, 15, game.colors["green"]), Block(60, 0, game.colors["green"]), Block(75, 0, game.colors["green"])]
            self.centre_rotation = [60, 0]
        elif self.letter == "Z":
            self.shape = [Block(45, 0, game.colors["red"]), Block(60, 0, game.colors["red"]), Block(60, 15, game.colors["red"]), Block(75, 15, game.colors["red"])]
            self.ghost = [Block(45, 0, game.colors["red"]), Block(60, 0, game.colors["red"]), Block(60, 15, game.colors["red"]), Block(75, 15, game.colors["red"])]
            self.centre_rotation = [60, 0]
        elif self.letter == "T":
            self.shape = [Block(45, 15, game.colors["purple"]), Block(60, 15, game.colors["purple"]), Block(60, 0, game.colors["purple"]), Block(75, 15, game.colors["purple"])]
            self.ghost = [Block(45, 15, game.colors["purple"]), Block(60, 15, game.colors["purple"]), Block(60, 0, game.colors["purple"]), Block(75, 15, game.colors["purple"])]
            self.centre_rotation = [60, 15]
        elif self.letter == "O":
            self.shape = [Block(60, 15, game.colors["yellow"]), Block(60, 0, game.colors["yellow"]), Block(75, 15, game.colors["yellow"]), Block(75, 0, game.colors["yellow"])]
            self.ghost = [Block(60, 15, game.colors["yellow"]), Block(60, 0, game.colors["yellow"]), Block(75, 15, game.colors["yellow"]), Block(75, 0, game.colors["yellow"])]
        self.letters_count += 1
        self.letters_list.remove(self.letter)
        game.check_game_over()
        self.next()
        self.ghost_fall()
        self.fall_speed = 0.2
        timer = threading.Timer(self.fall_speed, self.fall)
        timer.start()
        

    #making the figure fall
    def fall(self):
        if game.state != "paused":
            able = []
            for block in self.shape:
                block.goto_next = (block.x, block.y + 15)
                if block.goto_next not in game.positions_taken: able.append(True)
                else: able.append(False)
            if False not in able:
                for block in self.shape: block.y += 15
                if self.letter != "O": self.centre_rotation[1] += 15
                timer = threading.Timer(self.fall_speed, self.fall)
                timer.start()
            else:
                field.update()
                field.drop_and_remove()
                self.add()


    #resetting the ghost figure position
    def ghost_reset(self):
        for i in range(4):
            self.ghost[i].x = self.shape[i].x
            self.ghost[i].y = self.shape[i].y


    #making the ghost figure fall until it gets blocked off
    def ghost_fall(self):
        blocked_off = False
        while blocked_off == False:
            able = []
            for block in self.ghost:
                block.goto_next = (block.x, block.y + 15)
                if block.goto_next not in game.positions_taken: able.append(True)
                else: able.append(False)
            if False not in able:
                for block in self.ghost: block.y += 15
            else: blocked_off = True
            

    #moving the figure left and right
    def move(self, direction):
        able = []
        for block in self.shape:
            block.goto_next = (block.x + direction, block.y)
            if block.goto_next not in game.positions_taken: able.append(True)
            else: able.append(False)
        if False not in able:
            for block in self.shape: block.x += direction
            if self.letter != "O": self.centre_rotation[0] += direction
            self.ghost_reset()
            self.ghost_fall()
            

    #rotating the figure
    def rotate(self):
        able = []
        if self.letter != "I" and self.letter != "O":
            for block in self.shape:
                if [block.x, block.y] != self.centre_rotation:
                    if (block.x, block.y) == (self.centre_rotation[0] - 15, self.centre_rotation[1] - 15): block.goto_next = (self.centre_rotation[0] + 15, self.centre_rotation[1] - 15)
                    elif (block.x, block.y) == (self.centre_rotation[0] + 15, self.centre_rotation[1] - 15): block.goto_next = (self.centre_rotation[0] + 15, self.centre_rotation[1] + 15)
                    elif (block.x, block.y) == (self.centre_rotation[0] - 15, self.centre_rotation[1] + 15): block.goto_next = (self.centre_rotation[0] - 15, self.centre_rotation[1] - 15)
                    elif (block.x, block.y) == (self.centre_rotation[0] + 15, self.centre_rotation[1] + 15): block.goto_next = (self.centre_rotation[0] - 15, self.centre_rotation[1] + 15)
                    elif (block.x, block.y) == (self.centre_rotation[0], self.centre_rotation[1] - 15): block.goto_next = (self.centre_rotation[0] + 15, self.centre_rotation[1])
                    elif (block.x, block.y) == (self.centre_rotation[0], self.centre_rotation[1] + 15): block.goto_next = (self.centre_rotation[0] - 15, self.centre_rotation[1])
                    elif (block.x, block.y) == (self.centre_rotation[0] - 15, self.centre_rotation[1]): block.goto_next = (self.centre_rotation[0], self.centre_rotation[1] -  15)
                    elif (block.x, block.y) == (self.centre_rotation[0] + 15, self.centre_rotation[1]): block.goto_next = (self.centre_rotation[0], self.centre_rotation[1] + 15)
                    if block.goto_next not in game.positions_taken: able.append(True)
                    else: able.append(False)
        if self.letter == "I":
            for block in self.shape:
                if [block.x, block.y] != self.centre_rotation:
                    if (block.x, block.y) == (self.centre_rotation[0] - 15, self.centre_rotation[1]): block.goto_next = (self.centre_rotation[0], self.centre_rotation[1] - 15)
                    elif (block.x, block.y) == (self.centre_rotation[0] + 15, self.centre_rotation[1]): block.goto_next = (self.centre_rotation[0], self.centre_rotation[1] + 15)
                    elif (block.x, block.y) == (self.centre_rotation[0] + 30, self.centre_rotation[1]): block.goto_next = (self.centre_rotation[0], self.centre_rotation[1] + 30)
                    elif (block.x, block.y) == (self.centre_rotation[0], self.centre_rotation[1] - 15): block.goto_next = (self.centre_rotation[0] - 15, self.centre_rotation[1])
                    elif (block.x, block.y) == (self.centre_rotation[0], self.centre_rotation[1] + 15): block.goto_next = (self.centre_rotation[0] + 15, self.centre_rotation[1])
                    elif (block.x, block.y) == (self.centre_rotation[0], self.centre_rotation[1] + 30): block.goto_next = (self.centre_rotation[0] + 30, self.centre_rotation[1])
                    if block.goto_next not in game.positions_taken: able.append(True)
                    else: able.append(False)
        if False not in able and self.letter != "O":
            for block in self.shape:
                if [block.x, block.y] != self.centre_rotation:
                    block.x = block.goto_next[0]
                    block.y = block.goto_next[1]
            self.ghost_reset()
            self.ghost_fall()
            


#Block class
class Block:
    def __init__(self, x, y, color = None):
        self.x = x
        self.y = y
        self.color = color
        self.goto_next = None


#creating class instances
game = Game()
field = Field()
figure = Figure()
field.configure()
figure.create_letters_set()
figure.next()
figure.add()

#main game loop
while game.state != "end animation":
    game.events()
    game.render()
    game.display_text()
    game.update()
    

#ending the program
game.end_animation()
wn.fill((0, 0, 0))
game.render()
for block in game.end_blocks:
    pygame.draw.rect(wn, block.color, (block.x + 0.5, block.y + 0.5, 14, 14), border_radius = 3)
game.display_text()
game.update()
time.sleep(1)
pygame.quit()
sys.exit()



    
