import pygame
from pygame.locals import *

flags = FULLSCREEN | DOUBLEBUF

# initialise pygame
pygame.init()

# create window for gui
HEIGHT = 600
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
# screen.set_alpha(None)
FACTOR_OF_VIRUSES = 8
MAX_LEVEL = 5

# background
# background made by Kjpargeter from freepik.com
background = pygame.image.load("virus_background.png")

# Title and Icon
pygame.display.set_caption("Begone COVID-19")
# icon made by Ngor Phai from www.flaticon.com
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)


# Player
# playerImg made by Freepik from www.flaticon.com
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.playerImg = pygame.image.load("player.png")
        self.mask = pygame.mask.from_surface(self.playerImg)
        self.bullet = Bullet(x, y)
        self.cool_down_counter = 0

    def draw(self, scn):
        scn.blit(self.playerImg, (self.x, self.y))

    def fire_bullet(self):
        self.bullet.state = "fire"
        screen.blit(self.bullet.bulletImg, (self.bullet.x, self.bullet.y))


def initialise_level(lvl, virusX, virusY, collided, viruses):
    print("initializing...")
    print("level:", lvl)
    print("viruses: ", viruses)
    initialX = 15
    initialY = 15
    virusX.clear()
    virusY.clear()
    collided.clear()
    for i in range(viruses):
        virusX.append(initialX + 80 * (i % FACTOR_OF_VIRUSES))
        if i // FACTOR_OF_VIRUSES > 0:
            virusY.append(initialY + 75 * (i // FACTOR_OF_VIRUSES))
        else:
            virusY.append(initialY)
        collided.append(False)

# virus
# virusImg made by Freepik from www.flaticon.com


class Virus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.virusImg = pygame.transform.scale(pygame.image.load("virus.png"), (64, 64))
        self.mask = pygame.mask.from_surface(self.virusImg)

    def draw(self):
        screen.blit(self.virusImg, (self.x, self.y))

    def collision(self, obj):
        return has_collided(obj, self)

# Bullet

# States of bullet:
# Ready - you can't see the bullet on the screen
# Fire - The bullet is moving
# Bullet image by Darius Dan on flaticon.com


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bulletImg = pygame.image.load("bullet.png")
        self.state = "ready"
        self.mask = pygame.mask.from_surface(self.bulletImg)


def has_collided(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def cumulative_sum(lvl, total):
    if lvl == 1:
        return total + lvl
    else:
        total += lvl
        return cumulative_sum(lvl - 1, total)


# score
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(score):
    displayed_score = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(displayed_score, (10, 10))


def show_level(lvl):
    displayed_level = font.render("Level: " + str(lvl), True, (255, 255, 255))
    screen.blit(displayed_level, (WIDTH - displayed_level.get_width() - 10, 10))


# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 48)
restart_font = pygame.font.Font('freesansbold.ttf', 48)


def show_final_score(score):
    final_score_text = game_over_font.render("Final Score:" + str(score), True, (255, 255, 255))
    restart_text = restart_font.render("Press 'space' to restart", 1, (255, 255, 255))
    screen.blit(final_score_text, (WIDTH / 2 - final_score_text.get_width() / 2,
                                   HEIGHT / 2 - final_score_text.get_height()))
    screen.blit(restart_text, (WIDTH/2 - restart_text.get_width() / 2,
                               HEIGHT / 2 + restart_text.get_height() / 2 - final_score_text.get_height() / 2))


def main():
    # Game Loop
    isRunning = True
    game_over = False
    FPS = 60
    clock = pygame.time.Clock()
    level = 1
    score = 0
    player = Player(370, HEIGHT - 120)
    player.draw(screen)
    player_spd = 4
    bullet = player.bullet
    num_of_viruses = FACTOR_OF_VIRUSES
    virusX = []
    virusY = []
    virusX_change = 1
    virusY_change = 30
    collided = []
    initialise_level(level, virusX, virusY, collided, num_of_viruses)

    while isRunning:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if score == cumulative_sum(MAX_LEVEL, 0) * FACTOR_OF_VIRUSES * 1000:
            show_final_score(score)
            game_over = True
        if score == cumulative_sum(level, 0) * FACTOR_OF_VIRUSES * 1000 and level < MAX_LEVEL:
            level += 1
            num_of_viruses = FACTOR_OF_VIRUSES * level
            initialise_level(level, virusX, virusY, collided, num_of_viruses)
            virusX_change = 1
            continue
        # left key pressed
        if keys[pygame.K_LEFT] and player.x - player_spd > 0:
            player.x -= player_spd
        # right key pressed
        if keys[pygame.K_RIGHT] and player.x + player_spd + 64 < WIDTH:
            player.x += player_spd
        # space bar pressed
        if keys[pygame.K_SPACE]:
            if not game_over:
                if bullet.state == "ready":
                    bullet.x = player. x + 15
                    bullet.y -= 20
                    player.fire_bullet()
            else:
                level = 1
                score = 0
                num_of_viruses = FACTOR_OF_VIRUSES
                initialise_level(level, virusX, virusY, collided, num_of_viruses)
                game_over = False

        # player movement
        player.draw(screen)

        # virus movement
        for i in range(num_of_viruses):

            if virusY[i] > 480:
                show_final_score(score)
                game_over = True
                for j in range(num_of_viruses):
                    if not collided[j]:
                        collided[j] = True
                break
            if collided[i]:
                continue
            virusX[i] += virusX_change
            if virusX[i] < 0:
                virusX_change = - virusX_change
                for j in range(num_of_viruses):
                    virusY[j] += virusY_change
            elif virusX[i] > 736:
                virusX_change = - virusX_change
                for j in range(num_of_viruses):
                    virusY[j] += virusY_change

            virus = Virus(virusX[i], virusY[i])
            # Collision
            hasCollided = virus.collision(bullet)
            if hasCollided:
                bullet.y = 481
                bullet.state = "ready"
                score += 1000
                collided[i] = True
                virusX[i] = -99999999
                virusY[i] = -99999999
            virus.draw()

        # Bullet movement
        if bullet.y < 0:
            bullet.y = 481
            bullet.state = "ready"

        if bullet.state == "fire":
            bullet.y -= 20
            player.fire_bullet()

        show_score(score)
        show_level(level)
        pygame.display.update()


def main_menu():
    main_menu_font = pygame.font.Font('freesansbold.ttf', 64)
    isRunning = True
    while isRunning:
        screen.blit(background, (0, 0))
        main_menu_text = main_menu_font.render("Press 'space' to start", 1, (255, 255, 255))
        screen.blit(main_menu_text, (WIDTH/2 - main_menu_text.get_width()/2, HEIGHT/2 - main_menu_text.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
    pygame.quit()


main_menu()
