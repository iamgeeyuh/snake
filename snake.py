import pygame
import random
from collections import deque

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
GRID_SIZE = 20

BORDER_WIDTH = 600
BORDER_WIDTH_OFFSET = 200
BORDER_HEIGHT = 400
BORDER_HEIGHT_OFFSET = 100


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

STARTING_POS = pygame.Rect(
    BORDER_WIDTH // 2 + BORDER_HEIGHT_OFFSET,
    BORDER_HEIGHT // 2 + BORDER_HEIGHT_OFFSET,
    GRID_SIZE,
    GRID_SIZE,
)
player_pos = {
    (
        BORDER_WIDTH // 2 + BORDER_HEIGHT_OFFSET,
        BORDER_HEIGHT // 2 + BORDER_HEIGHT_OFFSET,
    ): STARTING_POS
}
player_body = deque([STARTING_POS])

border_pos = {}

for width in range(BORDER_WIDTH_OFFSET, BORDER_WIDTH + BORDER_WIDTH_OFFSET, GRID_SIZE):
    border_pos[(width, BORDER_HEIGHT_OFFSET)] = pygame.Rect(
        width, BORDER_HEIGHT_OFFSET, GRID_SIZE, GRID_SIZE
    )
    border_pos[(width, BORDER_HEIGHT + BORDER_HEIGHT_OFFSET)] = pygame.Rect(
        width, BORDER_HEIGHT + BORDER_HEIGHT_OFFSET, GRID_SIZE, GRID_SIZE
    )

for height in range(
    BORDER_HEIGHT_OFFSET, BORDER_HEIGHT + BORDER_HEIGHT_OFFSET, GRID_SIZE
):
    border_pos[(BORDER_WIDTH_OFFSET, height)] = pygame.Rect(
        BORDER_WIDTH_OFFSET, height, GRID_SIZE, GRID_SIZE
    )
    border_pos[(BORDER_WIDTH + BORDER_WIDTH_OFFSET - GRID_SIZE, height)] = pygame.Rect(
        BORDER_WIDTH + BORDER_WIDTH_OFFSET - GRID_SIZE, height, GRID_SIZE, GRID_SIZE
    )

prev_time = pygame.time.get_ticks()
speed = 1000
MIN_SPEED = 200


def spawn_apple():
    apple_x = random.randrange(
        BORDER_WIDTH_OFFSET + GRID_SIZE,
        BORDER_WIDTH + BORDER_WIDTH_OFFSET - GRID_SIZE,
        GRID_SIZE,
    )
    apple_y = random.randrange(
        BORDER_HEIGHT_OFFSET + GRID_SIZE,
        BORDER_HEIGHT + BORDER_HEIGHT_OFFSET,
        GRID_SIZE,
    )
    while (apple_x, apple_y) in player_pos:
        apple_x = random.randrange(
            BORDER_WIDTH_OFFSET + GRID_SIZE,
            BORDER_WIDTH + BORDER_WIDTH_OFFSET - GRID_SIZE,
            GRID_SIZE,
        )
    apple_y = random.randrange(
        BORDER_HEIGHT_OFFSET + GRID_SIZE,
        BORDER_HEIGHT + BORDER_HEIGHT_OFFSET,
        GRID_SIZE,
    )
    return pygame.Rect(apple_x, apple_y, GRID_SIZE, GRID_SIZE)


apple_pos = spawn_apple()

distance = GRID_SIZE
distance_x = 0
distance_y = -distance

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                distance_x = distance
                distance_y = 0
            elif event.key == pygame.K_LEFT:
                distance_x = -distance
                distance_y = 0
            elif event.key == pygame.K_UP:
                distance_x = 0
                distance_y = -distance
            if event.key == pygame.K_DOWN:
                distance_x = 0
                distance_y = distance
    screen.fill("white")

    curr_time = pygame.time.get_ticks()
    if curr_time - prev_time > speed:
        new_player_pos = (player_body[0].x + distance_x, player_body[0].y + distance_y)
        if new_player_pos in player_pos or new_player_pos in border_pos:
            running = False
            print("game over")
        player_pos[new_player_pos] = pygame.Rect(
            new_player_pos[0], new_player_pos[1], GRID_SIZE, GRID_SIZE
        )
        player_body.appendleft(player_pos[new_player_pos])
        if player_body[0] != apple_pos:
            pop = player_body.pop()
            player_pos.pop((pop.x, pop.y))
        else:
            apple_pos = spawn_apple()
            pygame.draw.rect(screen, "red", apple_pos)
            speed = max(MIN_SPEED, speed - 100)
        prev_time = curr_time

    for border in border_pos.keys():
        pygame.draw.rect(screen, "black", border_pos[border], 2)

    for pos in player_body:
        pygame.draw.rect(screen, "green", pos, 2)

    pygame.draw.rect(screen, "red", apple_pos)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
