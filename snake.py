import pygame, sys, random


def get_random(min, max):
    a = random.randint(min, max)
    return a - (a % 5)

pygame.init()
mainClock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
width, height = 500, 500
screen = pygame.display.set_mode((width, height), 0, 32)

# game over font
basicFont = pygame.font.SysFont(None, 48)
text = basicFont.render('Game Over!', True, WHITE, GREEN)
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery

# play again font
againtext = basicFont.render('click space to play again', True, WHITE, BLUE)
againtextRect = againtext.get_rect(center=(250, 400))

# set up direction variables
moveLeft = 1
moveRight = 3
moveUp = 7
moveDown = 9
PAUSE = 10
current = moveLeft

MOVESPEED = 20

# set up food data structures
FOODSIZE = 20

players = []
first_player = {'rect': pygame.Rect(200, 120, 20, 20), 'lastdir': moveDown}
players.append(first_player)

food = pygame.Rect(get_random(0, width - FOODSIZE), get_random(0, height - FOODSIZE), FOODSIZE, FOODSIZE)


def again():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    global players
                    players = []
                    players.append({'rect': pygame.Rect(200, 120, 20, 20), 'lastdir': moveDown})
                    return

        screen.fill(BLACK)
        screen.blit(text, textRect)
        screen.blit(againtext, againtextRect)
        pygame.display.update()


def move(rect, cur, speed):
    if cur == moveDown:
        rect.top += speed
    if cur == moveUp:
        rect.top -= speed
    if cur == moveLeft:
        rect.left -= speed
    if cur == moveRight:
        rect.left += speed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current = moveLeft
            if event.key == pygame.K_RIGHT:
                current = moveRight
            if event.key == pygame.K_UP:
                current = moveUp
            if event.key == pygame.K_DOWN:
                current = moveDown
            if event.key == pygame.K_SPACE:
                players.clear()
                players.append({'rect': pygame.Rect(200, 120, 20, 20), 'lastdir': moveDown})

    screen.fill(BLACK)

    # stem opposite action
    if players[0]['lastdir'] == moveLeft and current == moveRight:
        current = moveLeft
    if players[0]['lastdir'] == moveRight and current == moveLeft:
        current = moveRight
    if players[0]['lastdir'] == moveUp and current == moveDown:
        current = moveUp
    if players[0]['lastdir'] == moveDown and current == moveUp:
        current = moveDown

    # move snake
    move(players[0]['rect'], current, MOVESPEED)
    for i in range(1, len(players)):
        move(players[-i]['rect'], players[-i-1]['lastdir'], 20)
        players[-i]['lastdir'] = players[-i-1]['lastdir']
    players[0]['lastdir'] = current

    # game over
    if players[0]['rect'].left < 0 or players[0]['rect'].right > width or players[0]['rect'].top < 0 or players[0]['rect'].bottom > height:
        again()
    for i in range(2, len(players)):
        if players[0]['rect'].colliderect(players[i]['rect']):
            again()

    # draw snake
    for player in players:
        pygame.draw.rect(screen, WHITE, player['rect'])

    # eat food
    if players[0]['rect'].colliderect(food):
        food = pygame.Rect(random.randint(0, width - FOODSIZE), random.randint(0, height - FOODSIZE), FOODSIZE,
                           FOODSIZE)
        lef, t = players[-1]['rect'].left, players[-1]['rect'].top
        lastdir = players[-1]['lastdir']
        new_player = ''
        if lastdir == moveLeft:
            lef = lef + 20
        if lastdir == moveRight:
            lef = lef - 20
        if lastdir == moveUp:
            t = t + 20
        if lastdir == moveDown:
            t = t - 20
        players.append({'rect': pygame.Rect(lef, t, 20, 20), 'lastdir': lastdir})

    # draw food
    pygame.draw.rect(screen, GREEN, food)

    # update screen
    pygame.display.update()
    mainClock.tick(10)
