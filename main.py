
import pygame
from pygame.locals import *


pygame.init()

W,H=800,800
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("classic game")
FPS=60
clock = pygame.time.Clock()
vel=5
new_icon=pygame.image.load("Data\i.png")
pygame.display.set_icon(new_icon)

bg_img = pygame.image.load('Data/sprites/background/1.png')
restart_img = pygame.image.load('Data/sprites/butons/restart.png')
start_img = pygame.image.load('Data/sprites/butons/start.png')
exit_img = pygame.image.load('Data/sprites/butons/exit.png')

char1_img=pygame.image.load('Data/sprites/Characters/Char1/standing .png')
char2_img=pygame.image.load('Data/sprites/Characters/Char2/standing.png')
char3_img=pygame.image.load('Data/sprites/Characters/Char3/standing.png')
char4_img=pygame.image.load('Data/sprites/Characters/Char4/standing.png')


tile_size = 40
game_over=0
main_menu=True
Character_menu=True


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


		#draw button
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


class Player():
	def __init__(self, x, y,n):
		self.reset(x,y,n)

	def update(self,game_over):
			dx = 0
			dy = 0
			walk_cooldown = 5

			if game_over==0:
				#get keypresses
				key = pygame.key.get_pressed()
				if key[pygame.K_UP] and self.jumped == False and self.in_air == False:
					self.vel_y = -3*vel
					self.jumped = True
				if key[pygame.K_UP] == False:
					self.jumped = False
				if key[pygame.K_LEFT]:
					dx -= vel
					self.counter += 1
					self.direction = -1
				if key[pygame.K_RIGHT]:
					dx += vel
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
					#check if below the ground i.e. jumping
						if self.vel_y < 0:
							dy = tile[1].bottom - self.rect.top
							self.vel_y = 0
					#check if above the ground i.e. falling
						elif self.vel_y >= 0:
							dy = tile[1].top - self.rect.bottom
							self.vel_y = 0
							self.in_air =False 


				#check  for collition with enemies
				if pygame.sprite.spritecollide(self,slime_group,False):
					game_over=-1;		

				if pygame.sprite.spritecollide(self,lava_group ,False):
					game_over=-1;	

				#update player coordinates
				self.rect.x+=dx
				self.rect.y+=dy

			elif game_over ==-1:
				self.image = self.dead_image
				
			#draw player onto screen
			win.blit(self.image,self.rect)
			pygame.draw.rect(win,(255,255,255),self.rect,2)

			return game_over

	def reset(self,x,y,n):
			self.images_right=[]
			self.images_left=[]
			self.index=0
			self.counter=0
		
			for num in range(1,10):
				img_right=pygame.image.load(f'Data/sprites/Characters/Char{n}/R{num}.png')
				#img_right = pygame.transform.scale(img_right, (50,80))
				img_Left=pygame.transform.flip(img_right, True, False)
				#img_Left = pygame.transform.scale(img_Left, (50,80))
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

class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('Data\sprites\Block\dirt2.png')
		grass_img = pygame.image.load('Data\sprites\Block\green2.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					slime= Enemy(col_count * tile_size, row_count * tile_size + 15)
					slime_group.add(slime)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			win.blit(tile[0], tile[1])
			pygame.draw.rect(win,(255,255,255),tile[1],2)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Data/sprites/Characters/E/3.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0
	
	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Data/sprites/Characters/E/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y




world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


#main

slime_group=pygame.sprite.Group()   
lava_group = pygame.sprite.Group()

world = World(world_data)

restart_button = Button(W // 2 -10, H // 2 , restart_img)
start_button = Button(W // 2 - 200, H // 2, start_img)
exit_button = Button(W // 2 + 60, H // 2, exit_img)

c1 = Char(W // 2 - 300,H // 2 +100, char1_img)
c2 = Char(W // 2 - 120,H // 2 +95, char2_img)
c3 = Char(W // 2 + 80,H // 2 +100 , char3_img)
c4 = Char(W // 2 + 230,H // 2 +100, char4_img)

run = True
n=1
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

			player = Player(40,H-120,n)

		else:
			world.draw()

			if game_over == 0:
				slime_group.update()
		
			slime_group.draw(win)
			lava_group.draw(win)

			game_over = player.update(game_over)

			#if player has died
			if game_over == -1:
				if restart_button.draw():
					player.reset(100, H - 130,n)
					game_over = 0

	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()