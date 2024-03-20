
import pygame

#game setup
W,H=800,800
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("classic game")
FPS=60
clock = pygame.time.Clock()
new_icon=pygame.image.load("Data\i.png")
pygame.display.set_icon(new_icon)

#game variable
game_over=0
main_menu=True
Character_menu=True
level=1
max_levels = 7
score=0
speed=5
tile_size = 40
