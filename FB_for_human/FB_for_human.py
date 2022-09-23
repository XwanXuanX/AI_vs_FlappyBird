# FlappyBird, Original Edition

# import modules
import sys
import random 
import pygame

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
        if self.is_flapped:
            self.up_speed = max(12, self.up_speed + 1)
        else:
            self.is_flapped = True

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        left, top = position

        pipe_height = PIPE_HEIGHT
        if top > 0:
            pipe_height = BASE_HEIGHT - top + 1
        self.rect = pygame.Rect(left, top, PIPE_WIDTH, pipe_height)
        # use to calculate score
        self.used_for_score = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

    @staticmethod
    def generate_pipe_position():
        # generate top and bottom cords for pipes
        top = int(BASE_HEIGHT * 0.2) + random.randrange(
            0, int(BASE_HEIGHT * 0.6 - PIPE_GAP_SIZE))
        return {
            'top': (SCREEN_WIDTH + 25, top - PIPE_HEIGHT),
            'bottom': (SCREEN_WIDTH + 25, top + PIPE_GAP_SIZE)
        }


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
        pipe_sprites.add(
            Pipe((SCREEN_WIDTH + i * SCREEN_WIDTH / 2,
                  pipe_pos.get('top')[-1])))
        # Add pipe below
        pipe_sprites.add(
            Pipe((SCREEN_WIDTH + i * SCREEN_WIDTH / 2,
                  pipe_pos.get('bottom')[-1])))
    return bird, pipe_sprites


# check if birds collide with pipes
def collision(bird, pipe_sprites):
    is_collision = False
    for pipe in pipe_sprites:
        if pygame.sprite.collide_rect(bird, pipe):
            is_collision = True

    # update birds
    is_dead = bird.update()
    if is_dead:
        is_collision = True

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
    screen.blit(font.render(str(int(score)), True, (255, 255, 255)),
                (offset, SCREEN_HEIGHT * 0.1))


# Draw Game over
def draw_game_over(screen, text):
    font_size = 24
    font = pygame.font.SysFont('arial', font_size)
    screen.blit(font.render(text, True, (255, 255, 255), (0, 0, 0)),
                (60, SCREEN_HEIGHT * 0.4))


# key detection
def press(is_game_running, bird):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # space bar to flap the bird
                if is_game_running:
                    bird.up()
            elif event.key == 13 and not is_game_running:  # press enter to resume when game over
                return True


def main():
    screen = init_game()
    bird, pipe_sprites = init_sprite()
    clock = pygame.time.Clock()
    is_add_pipe = True
    is_game_running = True
    score = 0
    while True:
        restart = press(is_game_running, bird)  # press key
        if restart:
            return
        screen.fill((0, 0, 0))
        is_collision = collision(bird, pipe_sprites)  # collision detection
        if is_collision:
            is_game_running = False  # if collide, game over
        if is_game_running:
            is_add_pipe, score = move_pipe(bird, pipe_sprites, is_add_pipe,
                                           score)  # add pipes when game is not over
        else:
            draw_game_over(screen, 'Press Enter To Start!')  # if game is over, print the message
        bird.draw(screen)
        draw_score(screen, score)

        pygame.draw.line(screen, (255, 255, 255), (0, BASE_HEIGHT),
                         (SCREEN_WIDTH, BASE_HEIGHT))

        for pipe in pipe_sprites:
            pipe.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    while True:
        main()
