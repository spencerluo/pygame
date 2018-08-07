import pygame
import random
# color
import sys

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# move speed
moveSpeed = 10

moveLeft = 1
moveRight = 3


class Player:
    def __init__(self):
        self.player = [pygame.Rect(190, 390, 10, 10), pygame.Rect(200, 390, 10, 10), pygame.Rect(210, 390, 10, 10), pygame.Rect(200, 380, 10, 10)]
        self.bullet = pygame.Rect(200, 390, 10, 10)
        self.shotSpeed = 20

    def shot(self):
        self.bullet.top -= self.shotSpeed


class Bee:
    def __init__(self):
        self.bees = []
        self.beeSpeed = 1
        self.limit = 30
        self.direct = moveLeft
        for x in range(40, 360, 50):
            for y in range(10, 150, 50):
                self.bees.append(pygame.Rect(x, y, 10, 10))
        self.attack_bee = self.bees[0]

    def move(self):
        if self.direct == moveLeft:
            for bee in self.bees:
                bee.left -= self.beeSpeed
            self.limit -= 1
            if self.limit == 0:
                self.direct = moveRight

        if self.direct == moveRight:
            for bee in self.bees:
                bee.left += self.beeSpeed
            self.limit += 1
            if self.limit == 60:
                self.direct = moveLeft

    def die(self, bee):
        self.bees.remove(bee)

    def shot(self):
        orgin_top = self.attack_bee.top
        self.attack_bee.top += moveSpeed
        if self.attack_bee.top > 400:
            self.attack_bee.top = orgin_top
            self.reflush()

    def reflush(self):
        self.attack_bee = self.bees[random.randint(0, len(self.bees))]


def start_game():
    main_clock = pygame.time.Clock()

    # set up direction variables
    move_left = False
    move_right = False

    pygame.init()

    screen = pygame.display.set_mode((400, 400), 0, 32)

    player = Player()
    bees = Bee()
    shot = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                    move_right = False
                if event.key == pygame.K_RIGHT:
                    move_right = True
                    move_left = False
                if event.key == pygame.K_SPACE and shot == False:
                    shot = True
                    player.bullet.left = player.player[1].left
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False

        screen.fill(BLACK)

        # move player
        if move_left is True:
            for p in player.player:
                p.left -= moveSpeed
        if move_right is True:
            for p in player.player:
                p.left += moveSpeed

        if shot is True:
            player.shot()

        bees.shot()

        bees.move()

        # attack bee
        for bee in bees.bees:
            if player.bullet.colliderect(bee):
                bees.die(bee)
                shot = False
                player.bullet.top = 390

        for p in player.player:
            if p.colliderect(bees.attack_bee):
                while True:
                    pass

        # draw player
        for p in player.player:
            pygame.draw.rect(screen, BLUE, p)

        # draw bees
        for bee in bees.bees:
            pygame.draw.rect(screen, GREEN, bee)

        # draw bullet
        if shot is True:
            pygame.draw.rect(screen, BLUE, player.bullet)

        # update screen
        pygame.display.update()
        main_clock.tick(15)


start_game()


