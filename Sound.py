from Gameseting import *
from pygame import mixer
# sound library 
pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()
#loading sounds
pygame.mixer.music.load('Data/sound/game.mp3')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('Data/sound/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('Data/sound/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('Data/sound/Die.wav')
game_over_fx.set_volume(0.5)
level_won_fx=pygame.mixer.Sound('Data/sound/game_won.wav')
level_won_fx.set_volume(1)