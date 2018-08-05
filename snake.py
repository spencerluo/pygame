import pygame, sys, random


def get_random(min, max):
    a = random.randint(min, max)
    return a - (a % 5)

pygame.init()
mainClock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

width, height = 500, 500
screen = pygame.display.set_mode((width, height), 0, 32)

basicFont = pygame.font.SysFont(None, 48)
text = basicFont.render('Game Over!', True, WHITE, GREEN)
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery

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

food = pygame.Rect(get_random(0, width - FOODSIZE), get_random(0, height - FOODSIZE), FOODSIZE,
                           FOODSIZE)


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

    screen.fill(BLACK)

    move(players[0]['rect'], current, MOVESPEED)
    for i in range(1, len(players)):
        move(players[-i]['rect'], players[-i-1]['lastdir'], 20)
        players[-i]['lastdir'] = players[-i-1]['lastdir']
    # for i in range(1, len(players)):
    #     pass
    players[0]['lastdir'] = current


    # game over
    if players[0]['rect'].left < 0 or players[0]['rect'].right > width or players[0]['rect'].top < 0 or players[0]['rect'].bottom > height:
        current = PAUSE
        screen.blit(text, textRect)
    for i in range(2, len(players)):
        if players[0]['rect'].colliderect(players[i]['rect']):
            current = PAUSE
            screen.blit(text, textRect)

    for player in players:
        pygame.draw.rect(screen, WHITE, player['rect'])

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

    pygame.draw.rect(screen, GREEN, food)

    pygame.display.update()
    mainClock.tick(10)
