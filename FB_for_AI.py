# FlappyBird, AI Edition
# Modified from FB_original
# Increase getters and APIs for AI to call

# import modules
from gc import is_finalized
import sys
import random
from telnetlib import GA
from time import sleep
from turtle import up 
import pygame
from pynput.keyboard import Key, Controller
import threading


# FPS
FPS = 30
# Screen width and height
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
# Pipe width and height
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
# Pipe gap size
PIPE_GAP_SIZE = 100
# Bird width and height
BIRD_WIDTH = BIRD_HEIGHT = 20
# Floor height
FLOOR_HEIGHT = 80
# Gameplay area
BASE_HEIGHT = SCREEN_HEIGHT - FLOOR_HEIGHT


class Bird(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(*position, BIRD_WIDTH, BIRD_HEIGHT)
        self.is_flapped = False
        self.up_speed = 10
        self.down_speed = 0
        self.time_pass = FPS / 1000

    # update bird position
    def update(self):
        # check if the bird is flapped or not
        if self.is_flapped:
            # upspeed decrease through time
            self.up_speed -= 60 * self.time_pass
            self.rect.top -= self.up_speed
            # when upspeed is 0, make the bird fall
            if self.up_speed <= 0:
                self.down()
                self.up_speed = 10
                self.down_speed = 0
        else:
            # the bird is not flapped, downspeed increase through time
            self.down_speed += 30 * self.time_pass
            self.rect.bottom += self.down_speed

        # check if the bird hits top and bottom border
        is_dead = False
        if self.rect.top <= 0:  # top border
            self.up_speed = 0
            self.rect.top = 0
            is_dead = True
        if self.rect.bottom >= BASE_HEIGHT:  # bottom border
            self.up_speed = 0
            self.down_speed = 0
            self.rect.bottom = BASE_HEIGHT
            is_dead = True
        return is_dead

    # Bird did not flap -> go down
    def down(self):
        self.is_flapped = False

    # Bird flapped -> go up
    def up(self):
        if self.is_flapped: self.up_speed = max(12, self.up_speed + 1)
        else: self.is_flapped = True

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

#________________________________________________________________________
#   API for AI to call
#   Get the center X position of bird

    def getBirdYPos(self):
        return self.rect.centery
#________________________________________________________________________


class Pipe(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        left, self.top = position
        pipe_height = PIPE_HEIGHT
        if self.top > 0: pipe_height = BASE_HEIGHT - self.top + 1
        self.rect = pygame.Rect(left, self.top, PIPE_WIDTH, pipe_height)
        # use to calculate score
        self.used_for_score = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

#_________________________________________________________________________
#   API for AI to call
#   Get the top and bottom position of pipes

    def getPipeYPos(self):
        return self.top
#_________________________________________________________________________

    @staticmethod
    def generate_pipe_position():
        # generate top and bottom cords for pipes
        top = int(BASE_HEIGHT * 0.2) + random.randrange(0, int(BASE_HEIGHT * 0.6 - PIPE_GAP_SIZE))
        return {
            'top': (SCREEN_WIDTH + 25, top - PIPE_HEIGHT),
            'bottom': (SCREEN_WIDTH + 25, top + PIPE_GAP_SIZE)}


# Initialize game
def init_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('AI VS. Flappy Bird')
    return screen


# initialize sprites
def init_sprite():
    # bird class 
    bird_position = [SCREEN_WIDTH * 0.2, (SCREEN_HEIGHT - BIRD_HEIGHT) / 3]
    bird = Bird(bird_position)
    # pipe class
    pipe_sprites = pygame.sprite.Group()
    for i in range(2):
        pipe_pos = Pipe.generate_pipe_position()
        # Add pipe above
        pipe_sprites.add(Pipe((SCREEN_WIDTH + i * SCREEN_WIDTH / 2,
                         pipe_pos.get('top')[-1])))
        # Add pipe below
        pipe_sprites.add(Pipe((SCREEN_WIDTH + i * SCREEN_WIDTH / 2,
                         pipe_pos.get('bottom')[-1])))
    return bird, pipe_sprites


# check if birds collide with pipes
def collision(bird, pipe_sprites):
    is_collision = False
    for pipe in pipe_sprites:
        if pygame.sprite.collide_rect(bird, pipe): is_collision = True
    # update birds
    is_dead = bird.update()
    if is_dead: is_collision = True
    return is_collision


# move pipes forward
def move_pipe(bird, pipe_sprites, is_add_pipe, score):
    flag = False
    for pipe in pipe_sprites:
        pipe.rect.left -= 4
        # when birds fly pass a pipe, add score
        if pipe.rect.centerx < bird.rect.centerx and not pipe.used_for_score:
            pipe.used_for_score = True
            score += 0.5
        # Add new pipes into the scene
        if pipe.rect.left < 10 and pipe.rect.left > 0 and is_add_pipe:
            pipe_pos = Pipe.generate_pipe_position()
            pipe_sprites.add(Pipe(position=pipe_pos.get('top')))
            pipe_sprites.add(Pipe(position=pipe_pos.get('bottom')))
            is_add_pipe = False
        # Delete pipes not in scene
        elif pipe.rect.right < 0:
            pipe_sprites.remove(pipe)
            flag = True
    if flag:
        is_add_pipe = True
    return is_add_pipe, score


# Draw score
def draw_score(screen, score):
    font_size = 32
    digits = len(str(int(score)))
    offset = (SCREEN_WIDTH - digits * font_size) / 2
    font = pygame.font.SysFont('Blod', font_size)
    screen.blit(font.render(str(int(score)), True, (255, 255, 255)), (offset, SCREEN_HEIGHT * 0.1))


# key detection
def press(is_game_running, bird):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and is_game_running:
            bird.up() # space bar to flap the bird


#________________________________________________________________
#   Main Game Class

class Game():
    def __init__(self):
        self.screen = init_game()
        self.bird, self.pipe_sprites = init_sprite()
        self.clock = pygame.time.Clock()
        self.is_add_pipe = True
        self.is_game_running = True
        self.score = 0
    
    def CreateGame(self):
        while True:
            press(self.is_game_running, self.bird)  # detect button press

            self.screen.fill((0, 0, 0)) # set background color

            is_collision = collision(self.bird, self.pipe_sprites)  # collision detection
            if is_collision: self.is_game_running = False  # if collide, game over

            if self.is_game_running:
                self.is_add_pipe, self.score = move_pipe(self.bird, self.pipe_sprites, self.is_add_pipe,
                                                         self.score)  # add pipes when game is not over
            else: pygame.quit(); return

            # Draw elements
            self.bird.draw(self.screen)
            draw_score(self.screen, self.score)
            pygame.draw.line(self.screen, (255, 255, 255), (0, BASE_HEIGHT),
                            (SCREEN_WIDTH, BASE_HEIGHT))
            for pipe in self.pipe_sprites: pipe.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FPS)


#________________________________________________________________
#   Thread 1: Create and run the game
#   Thread 2: AI mimic keyboard input

# AI will modify this global variable to decide whether to jump.
should_jump = True

# create and run a new game, exit when gameover
def StartGame():
    game = Game()
    game.CreateGame()
    if game.is_game_running == False: return

# when game is not over, mimic keyborad input; exit when gameover
def StartPlay():
    global should_jump
    keyboard = Controller()
    key = " "

    while True:
        if gameThread.is_alive() and should_jump == True:
            keyboard.press(key)
            keyboard.release(key)
            sleep(0.4)
        elif gameThread.is_alive() and should_jump == False: pass
        else: return

# Multithread class: call different functions based on thread name
class AIThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        if self.name == "GameThread":   StartGame()
        elif self.name == "AIThread":   StartPlay()
        print("Exiting " + self.name)


#_________________________________________________________________
#   Main Function for testing (Will be commented out later)

if __name__ == "__main__":
    gameThread = AIThread(1, "GameThread")
    aiThread = AIThread(2, "AIThread")

    gameThread.start()
    aiThread.start()
#_________________________________________________________________