import pygame
from os import path
import pickle
from pygame.locals import *
from EnemyClasses import *
from Gameseting import*
from Images import*
from Menu import*
from Sound import*
from World import *
from Writingseting import*

def reset_level(level):
	player.reset(100,H-130,n)
	slime_group.empty()
	lava_group.empty()
	platform_group.empty()
	coin_group.empty()
	exit_group.empty()

	#loading  level 
	if path.exists(f'Data/levels/level{level}_data'):
		pickle_in = open(f'Data/levels/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)

	world = World(world_data)

	return world
class Player():
	def __init__(self, x, y,n):
		self.reset(x,y,n)
		
	def update(self,game_over):
			dx = 0
			dy = 0
			walk_cooldown = 5
			col_thresh = 20

			if game_over==0:
				#get keypresses
				key = pygame.key.get_pressed()
				if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
					jump_fx.play()
					self.vel_y = -3*speed
					self.jumped = True
				if key[pygame.K_UP] == False:
					self.jumped = False
				if key[pygame.K_LEFT]:
					dx -= speed
					self.counter += 1
					self.direction = -1
				if key[pygame.K_RIGHT]:
					dx += speed
					self.counter += 1
					self.direction = 1
				if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
					self.counter = 0
					self.index = 0
					if self.direction == 1:
						self.image = self.images_right[self.index]
					if self.direction == -1:
						self.image = self.images_left[self.index]


				#handle animation
				if self.counter > walk_cooldown:
					self.counter = 0	
					self.index += 1
					if self.index >= len(self.images_right):
						self.index = 0
					if self.direction == 1:
						self.image = self.images_right[self.index]
					if self.direction == -1:
						self.image = self.images_left[self.index]
				#add gravity
				self.vel_y+=1
				if self.vel_y > 10:
					self.vel_y = 10
				dy+=self.vel_y
				#check for collision
				self.in_air = True
				for tile  in world.tile_list:
					#check for collision in x direction
					if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
						dx = 0
					#check for collision in y direction
					if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground : jumping
						if self.vel_y < 0:
							dy = tile[1].bottom - self.rect.top
							self.vel_y = 0
					#check if above the ground : falling
						elif self.vel_y >= 0:
							dy = tile[1].top - self.rect.bottom
							self.vel_y = 0
							self.in_air =False 


				#check  for collition with enemies
				if pygame.sprite.spritecollide(self,slime_group,False):
					game_over_fx.play()
					game_over=-1;		

				if pygame.sprite.spritecollide(self,lava_group ,False):
					game_over_fx.play()
					game_over=-1;	
				
				if pygame.sprite.spritecollide(self,exit_group ,False):
					level_won_fx.play()
					game_over=+1;	
				
				#check for collision with platforms
				for platform in platform_group:
					#collision in the x direction
					if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
						dx = 0
					#collision in the y direction
					if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
						#check if below platform
						if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
							self.vel_y = 0
							dy = platform.rect.bottom - self.rect.top
						#check if above platform
						elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
							self.rect.bottom = platform.rect.top - 1
							self.in_air = False
							dy = 0
						#move sideways with the platform
						if platform.move_x != 0:
							self.rect.x += platform.move_direction
				#update player coordinates
				self.rect.x+=dx
				self.rect.y+=dy

			elif game_over ==-1:
				self.image = self.dead_image
				
			#draw player onto screen
			win.blit(self.image,self.rect)
			

			return game_over

	def reset(self,x,y,n):
			self.images_right=[]
			self.images_left=[]
			self.index=0
			self.counter=0
		
			for num in range(1,10):
				img_right=pygame.image.load(f'Data/sprites/Characters/Char{n}/R{num}.png')
				img_Left=pygame.transform.flip(img_right, True, False)
				self.images_right.append(img_right)
				self.images_left.append(img_Left)
			self.dead_image=pygame.image.load('Data/sprites/Characters/Dead/Dead.png')
			self.image=self.images_right[self.index]
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y
			self.width = self.image.get_width()
			self.height = self.image.get_height()
			self.vel_y=0
			self.jumped=False
			self.direction=0
			self.in_air = True	

#main loop
if path.exists(f'Data/levels/level{level}_data'):
	pickle_in = open(f'Data/levels/level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)

world = World(world_data)
run = True
n=1
player=Player(100,H-130,n)
while run:
	clock.tick(FPS)
	win.blit(bg_img, (0, 0))

	if main_menu==True:
		if exit_button.draw():
			run =False
		if start_button.draw():
			main_menu=False
	
	else:
		if Character_menu==True:
			if c1.draw():
				c1.nc=1
				n=c1.get_nc()
				Character_menu=False
			if c2.draw():
				c2.nc=2
				n=c2.get_nc()
				Character_menu=False
			if c3.draw():
				c3.nc=3
				n=c3.get_nc()
				Character_menu=False
			if c4.draw():
				c4.nc=4
				n=c4.get_nc()
				Character_menu=False
			draw_text('Chose your character: ',font_menu,black,W//2-220,H//2-100)
			player = Player(40,H-120,n)

		else:
			world.draw()

			if game_over == 0:
				slime_group.update()
				platform_group.update()
				if pygame.sprite.spritecollide(player,coin_group,True):
					coin_fx.play()
					score+=1
				draw_text('Score: '+str(score*5),font_score,black,tile_size-10,10)

			slime_group.draw(win)
			platform_group.draw(win)
			lava_group.draw(win)
			coin_group.draw(win)
			exit_group.draw(win)

			game_over = player.update(game_over)

			#if player has died
			if game_over == -1:
				if restart_button.draw():
					world_data = []
					world=reset_level(level)
					game_over = 0
					score=0
				draw_text('GAME OVER ',font,red,W//2-180,H//2-200)
			if game_over==1:
				level+=1
				if level<=max_levels:
					world_data = []
					world=reset_level(level)
					game_over = 0
				else:
					draw_text('YOU WIN!!',font,blue,W//2-200,H//2-200)
					if restart_button.draw():
						level=1
						world_data=[]
						world=reset_level[level]
						game_over=0
						score=0
						
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()