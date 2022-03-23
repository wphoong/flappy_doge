import pygame, sys, random, time, math
import numpy as np
import pandas as pd
from pygame.locals import *
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

doge_img = 'images/doge.png'
background_img = 'images/background.jpg'
base_img = 'images/base.png'
pipe_img = 'images/pipe.png'

# init screen
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
screen_width = 600
screen_height = 620
fps = 30


class Game:
	def __init__(self):
		self.game_state = True
		self.pipe_arr = []
		self.bg = None
		self.player_arr = []
		self.score = 0

	def create_pipe(self, pipe):
		self.pipe_arr.append(pipe)

	def create_bg(self, bg):
		self.bg = bg

	def create_player(self, player):
		self.player_arr.append(player)

	def check_pipes(self):
		# pipe creation
		if len(self.pipe_arr) < 1:
			self.pipe_arr.append(Pipe('bottom'))
			self.pipe_arr.append(Pipe('top'))

	def check_game_over(self):
		# win condition
		if self.score >= 50:
			print('Game Over, You Win!')
			self.game_state = False
		else:
			# lose conditions
			if (self.player_arr[0].player_y > (screen_height - 150) or self.player_arr[0].player_y <= -15):
				# self.player_arr[0].status = 0
				# self.game_state = False
				print('gameover 1')
			if (self.pipe_arr[0].kind == 'bottom' and self.player_arr[0].player_x+40 >= self.pipe_arr[0].pipe_x) and (self.player_arr[0].player_y+25 >= self.pipe_arr[0].pipe_y):
				# self.player_arr[0].status = 0
				# self.game_state = False
				print('gameover2')
			if (self.pipe_arr[0].kind == 'top' and self.player_arr[0].player_x+40 >= self.pipe_arr[0].pipe_x) and (self.player_arr[0].player_y <= self.pipe_arr[0].pipe_y+300):
				# self.player_arr[0].status = 0
				# self.game_state = False
				print('gameover3')

		# if self.pipe_arr[0].kind == 'up' and player.status == 1:
		# 	if self.pipe_arr[0].pipe_x <= 203 and self.pipe_arr[0].pipe_x >= 198:
		# 		player.score += 1

	def check_player_status(self):
		for player in selfplayer_arr:
			if player.status == 0:
				self.player_arr.remove(player)
		

class Background:
	def __init__(self):
		self.bg = pygame.image.load(background_img).convert_alpha()
		self.base = pygame.image.load(base_img).convert_alpha()
		self.rect = self.bg.get_rect()

class Pipe:
	def __init__(self, kind):
		self.kind = kind

		if self.kind == 'bottom':
			self.pipe = pygame.image.load(pipe_img).convert_alpha()
			self.rect = self.pipe.get_rect(bottomright=(screen_width, screen_height))
			self.pipe_x = self.rect.left
			self.pipe_y = random.randrange(350, screen_height-100)
			
		elif self.kind == 'top':
			d_pipe = pygame.image.load(pipe_img).convert_alpha()
			self.pipe =  pygame.transform.rotate(d_pipe, 180).convert_alpha()
			self.rect = self.pipe.get_rect(topright=(screen_width, 0))
			self.pipe_x = self.rect.left
			self.pipe_y = random.randrange(-200, 0)

	def move_pipe(self):
		if self.pipe_x > 0:
			self.pipe_x -= 5

class Doge:
	def __init__(self):
		self.player = pygame.image.load(doge_img).convert_alpha()
		self.rect = self.player.get_rect(center=(screen_width/3, random.randrange(0, screen_height)))
		self.player_x = self.rect.centerx
		self.player_y = self.rect.centery
		self.fall_vel = 5
		self.flapped = False
		self.flap_vel = 25 
		self.brain = make_pipeline(StandardScaler(), SGDClassifier(max_iter=1000, tol=1e-3))
		self.data = pd.DataFrame([[550, 600, 500, 100, True, 1], [200, 400, 450, 50, False, 0]], columns=['0','1','2','3','diff','target'])
		self.status = 1

	def flap(self):
		if self.player_y > 0:
			self.player_y -= self.flap_vel
			self.flapped = True

	def check_player_flap(self):
		# player flap control
		if not self.flapped and self.player_y <= 500:
			self.player_y += self.fall_vel

		if self.flapped:
			self.flapped = False

	def convert_diff(self, x):
		if x == True:
			return 1
		elif x == False:
			return 0


	def build_data(self, pipes):
		inputs = [self.player_y+40, pipes[0].pipe_x, pipes[0].pipe_y, pipes[1].pipe_y+320]
		inputs = pd.DataFrame([inputs], columns=['0','1','2','3'])
		inputs['diff'] = inputs['0'] > inputs['2']
		inputs['target'] = in puts['diff'].apply(self.convert_diff)
		self.data = pd.concat([self.data, inputs])
		
	def think(self, pipes):
		features = self.data.copy().iloc[:, [0,1,2]]
		
		target = self.data.copy()['target']

		self.brain.fit(features, target)
		output = self.brain.predict(features)

		if output[-1] == 1:
			self.flap()

		
def main():
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption('Flappy Doge')

	# create game background, player, and pipes
	game = Game()
	game.create_bg(Background())

	# build default pipes
	# game.pipe_arr = [Pipe('bottom'), Pipe('top')]
	game.create_pipe(Pipe('bottom'))
	game.create_pipe(Pipe('top'))

	# create player
	population = 50
	for _ in range(10):
		game.create_player(Doge())

	# initialize game loop
	while game.game_state:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			# Player flap vent	
			# if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
			# 	game.player_arr[0].flap()

		game.check_pipes()
		game.check_game_over()
		
		for player in game.player_arr:
			player.check_player_flap()

		if len(game.pipe_arr) == 2 and game.pipe_arr[0].kind == 'bottom':
			for player in game.player_arr:
					player.build_data(game.pipe_arr)
					player.think(game.pipe_arr)

		screen.blit(game.bg.bg, game.bg.rect)
		screen.blit(game.bg.base, (0,screen_height-110))

		for pipe in game.pipe_arr:
			if pipe.pipe_x < 170:
				game.pipe_arr.pop(0)
				if pipe.kind == 'top':
					game.score += 1	
			pipe.move_pipe()
			screen.blit(pipe.pipe, (pipe.pipe_x, pipe.pipe_y))

		for player in game.player_arr:
			screen.blit(player.player, (player.player_x, player.player_y))

		textsurface = myfont.render(str(game.score), True, (0, 0, 0))
		screen.blit(textsurface, (20,20))

		pygame.display.flip()
		pygame.time.Clock().tick(fps)


if __name__ == '__main__':
	main()



