import pygame
from Gameseting import*
from Images import *

class Char():
	def __init__(self, x, y, image):
		self.nc=0
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def get_nc(self):
		nc=self.nc
		return nc
	
	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw char
		win.blit(self.image, self.rect)

		return action



class Button():
	def __init__(self, x, y, image):
		
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False
	
	
	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		win.blit(self.image, self.rect)

		return action

restart_button = Button(W // 2 -120, H // 2-40 , restart_img)
start_button = Button(W // 2 - 280, H // 2, start_img)
exit_button = Button(W // 2 + 40, H // 2, exit_img)
c1 = Char(W // 2 - 300,H // 2 +50, char1_img)
c2 = Char(W // 2 - 120,H // 2 +45, char2_img)
c3 = Char(W // 2 + 80,H // 2 +50 , char3_img)
c4 = Char(W // 2 + 230,H // 2 +50, char4_img)


			