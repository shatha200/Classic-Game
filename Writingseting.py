import pygame
from Gameseting import*
pygame.init()
#writing setup
font_score=pygame.font.SysFont('swiss',30 )
font=pygame.font.SysFont('Bauhaus 93',70)
font_menu=pygame.font.SysFont('lucidasanstypewriterregular',40 )
black=(00,00,00)
blue=(0,0,255)
red=(255,0,0)

#function
def draw_text(text,font,text_col,x,y):
	img=font.render(text,True,text_col)
	win.blit(img,(x,y))