import pygame
pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800
# create "scree" that way we can load our images here once
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

TILESIZE = 16
#42 by 42 tile size

#Asteroid Sizes
BIG_ASTEROID_SIZE = TILESIZE * 7
MED_ASTEROID_SIZE = TILESIZE * 5
SM_ASTEROID_SIZE = TILESIZE * 3

#target FPS
FPS = 60

#layers
PLAYER_LAYER = 4
ASTEROID_LAYER = 3

#Lives

PLAYER_LIVES = 3


# speeds (temporary)
PLAYER_SPEED = 3
ASTEROID_SPEED = 1

#colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# saycer bullets
BULLET_SPEED = 8
BULLET_COLOR = BLACK 
BULLET_SIZE = 5
SPECIAL_BULLET_COLOR = RED
SPECIAL_BULLET_SPEED = 8

# player ship images
SHIP_A = [
    pygame.image.load('Images/ships/ship-a/ship-a1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-a/ship-a2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-a/ship-a3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-a/ship-a-damaged.png').convert_alpha()
]

SHIP_A_BUTTON = [
    pygame.transform.scale(SHIP_A[0], (200,200)),
    pygame.transform.scale(SHIP_A[1], (200,200)),
    pygame.transform.scale(SHIP_A[2], (200,200))
]

SHIP_B = [
    pygame.image.load('Images/ships/ship-b/ship-b1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-b/ship-b2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-b/ship-b3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-b/ship-b-damaged.png').convert_alpha()
]

SHIP_B_BUTTON = [
    pygame.transform.scale(SHIP_B[0], (200,200)),
    pygame.transform.scale(SHIP_B[1], (200,200)),
    pygame.transform.scale(SHIP_B[2], (200,200))
]

SHIP_C = [
    pygame.image.load('Images/ships/ship-c/ship-c1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-c/ship-c2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-c/ship-c3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-c/ship-c-damaged.png').convert_alpha()
]

SHIP_C_BUTTON = [
    pygame.transform.scale(SHIP_C[0], (200,200)),
    pygame.transform.scale(SHIP_C[1], (200,200)),
    pygame.transform.scale(SHIP_C[2], (200,200))
]

SHIP_D = [
    pygame.image.load('Images/ships/ship-d/ship-d1.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-d/ship-d2.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-d/ship-d3.png').convert_alpha(),
    pygame.image.load('Images/ships/ship-d/ship-d-damaged.png').convert_alpha()
]

SHIP_D_BUTTON = [
    pygame.transform.scale(SHIP_D[0], (200,200)),
    pygame.transform.scale(SHIP_D[1], (200,200)),
    pygame.transform.scale(SHIP_D[2], (200,200))
]

SELECTED_SHIP = 0 # default ship-a
