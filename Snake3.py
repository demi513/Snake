#https://wallpapersafari.com/windows-start-wallpaper/ for bg
#https://opengameart.org/content/chill-lofi-inspired for music
#https://opengameart.org/content/life-heart-and-rainbow-star-gifs star
import pygame as pg
import random
import random
from os import path
from time import sleep
import tkinter as tk


snd_folder = path.join(path.dirname(__file__), 'Snd')
img_folder = path.join(path.dirname(__file__), 'Img')

WIDTH = 600
FPS = 60
TITLE = 'Snake by Dean'
ROWS = 20

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (220,20,60)
GREEN = (124,252,0)
LIGHTBLUE = (22, 73, 154)
BLUE = (0,0,255)
GREY = (128,128,128)
PINK = (255,105,180)
DARKERPINK = (255,20,147)
DARKPINK = (199,21,133)
pg.init()
pg.mixer.init()
win = pg.display.set_mode((WIDTH+100,WIDTH))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()


font_name = pg.font.match_font('arial')

def draw_text(surf,x,y,text,size, color):
	font = pg.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.center = (x,y)
	surf.blit(text_surface, text_rect)

def show_go_screen():
	win.fill(BLUE)
	win.blit(bg, bg_rect)
	txt = 'Snake by Dean'
	if won:
		txt = 'YOU WON!'
	draw_text(win, WIDTH//2+50, WIDTH//10*4, txt, 50, WHITE)
	draw_text(win, WIDTH//2+50, WIDTH * 5/10, 'Arrow Keys to move', 20, WHITE)
	draw_text(win, WIDTH//2+50, WIDTH *6/10, 'Right click to place block, left click to remove block', 20, WHITE)
	draw_text(win, WIDTH//2+50, WIDTH *7/10, 'Press any key to start after placing your blocks', 20, WHITE)
	draw_text(win, WIDTH//2+50, WIDTH *8/10, 'Press any key to start', 15, WHITE)
	pg.display.flip()
	sleep(1)
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				waiting = False
				pg.quit()
			if event.type == pg.KEYUP:
				waiting = False

def action():
	global dict_blocks, available
	dict_blocks = {}
	for i in range(ROWS):
		for j in range(ROWS):
			d = Blocks(WIDTH//ROWS * i, WIDTH//ROWS * j, WIDTH//ROWS)
			dict_blocks[d.position()] = d
	available = dict_blocks.copy()	

def settings():
	def do():
		global FPS, ROWS, win, how_many_food
		fine = True
		try:
			FPS = int(configurations[0][2].get().strip())
		except:
			configurations[0][2].delete(0, tk.END)
			configurations[0][2].insert(0, 'Invalid')
			fine = False
		try:
			q.maxlength = int(configurations[1][2].get().strip())
		except:
			configurations[1][2].delete(0, tk.END)
			configurations[1][2].insert(0, 'Invalid')			
			fine = False
		try:
			q.reload = int(configurations[2][2].get().strip())
		except:
			configurations[2][2].delete(0, tk.END)
			configurations[2][2].insert(0, 'Invalid')
			fine = False
		try:
			ROWS = int(configurations[3][2].get().strip())
		except:
			configurations[3][2].delete(0, tk.END)
			configurations[3][2].insert(0, 'Invalid')
			fine = False
		try:
			how_many_food = int(configurations[4][2].get().strip())
		except:
			configurations[4][2].delete(0, tk.END)
			configurations[4][2].insert(0, 'Invalid')
			fine = False
		if fine:
			root.destroy()
			action()
	configurations = [['Fps', FPS], ['Starting Length', q.maxlength], ['Mouvement Speed', q.reload], ['Rows', ROWS],['How much food after one', how_many_food]]
	new_list = []

	root = tk.Tk()
	root.protocol('WM_DELETE_WINDOW', do)
	root.geometry('+300+300')
	root.title('Settings')
	root.rowconfigure([i for i in range(len(configurations))], weight=1)
	root.columnconfigure([i for i in range(len(configurations[0]))],weight=1)
	for i in range(len(configurations)):
		lbl = tk.Label(master=root, text=configurations[i][0])
		lbl.grid(row=i, column=0, padx=10, pady=10, sticky='nsew')
		txt = tk.Entry(master=root, width=20)
		configurations.insert(i, configurations.pop(i) + [txt])
		txt.insert(0, configurations[i][1])
		txt.grid(row=i, column=1)
	while True:
		for event in pg.event.get():	
			if event.type == pg.QUIT:
				pg.quit()
				exit()
		try:
			root.update_idletasks()
			root.update()
		except:
			break

class Blocks():
	def __init__(self, x, y, width):
		self.x = x
		self.y = y
		self.row = self.y//(WIDTH//ROWS)
		self.col = self.x//(WIDTH//ROWS)
		self.color = GREY
		self.width = width

	def is_snake(self):
		return self.color == GREEN

	def is_food(self):
		return self.color == RED

	def is_reset(self):
		return self.color == GREY

	def hit_wall(self):
		return self.x < 0 or self.x + self.width > WIDTH or self.y < 0 or self.y + self.width > WIDTH

	def position(self):
		return (self.row, self.col)

	def make_snake(self):
		self.color = GREEN

	def make_food(self):
		self.color = RED

	def make_reset(self):
		self.color = GREY

	def make_wall(self):
		self.color = BLACK

	def draw(self, win):
		pg.draw.rect(win, self.color, pg.Rect(self.x, self.y, self.width, self.width))

class Snake():
	def __init__(self, maxlength, reloade):
		self.x = WIDTH//ROWS*(ROWS//2)+(WIDTH//ROWS//2)
		self.y = WIDTH//ROWS*(ROWS//2)+(WIDTH//ROWS//2)
		self.row = self.y//(WIDTH//ROWS)
		self.col = self.x//(WIDTH//ROWS)
		self.reload = reloade
		self.last_movement = pg.time.get_ticks()
		self.default_speed = WIDTH//ROWS
		self.vx = 0
		self.vy = self.default_speed
		self.maxlength = maxlength
		self.face = {(self.default_speed, 0):'Right', (-self.default_speed, 0):'Left', (0, self.default_speed):'Down', (0, -self.default_speed):'Up'}
		self.facing = self.face[(self.vx, self.vy)]
		self.snake_list = [(self.row, self.col)]
		self.last_direction = 'Up'

	def position(self):
		return (self.row, self.col)

	def left(self):
		self.vx = -self.default_speed
		self.vy = 0
		self.facing = self.face[(self.vx, self.vy)]	

	def right(self):
		self.vx = self.default_speed
		self.vy = 0
		self.facing = self.face[(self.vx, self.vy)]

	def down(self):
		self.vx = 0
		self.vy = self.default_speed
		self.facing = self.face[(self.vx, self.vy)]

	def up(self):
		self.vx = 0
		self.vy = -self.default_speed
		self.facing = self.face[(self.vx, self.vy)]

	def update(self):
		keystate = pg.key.get_pressed()
		if keystate[pg.K_RIGHT] and self.facing != 'Left':
			self.last_direction = 'Right'
		elif keystate[pg.K_LEFT] and self.facing != 'Right':
			self.last_direction = 'Left'
		elif keystate[pg.K_UP] and self.facing != 'Down':
			self.last_direction = 'Up'
		elif keystate[pg.K_DOWN] and self.facing != 'Up':
			self.last_direction = 'Down'

		if pg.time.get_ticks() - self.last_movement > self.reload:
			self.last_movement = pg.time.get_ticks()
			if self.last_direction == 'Left':
				self.left()
			elif self.last_direction == 'Right':
				self.right()
			elif self.last_direction == 'Down':
				self.down()
			elif self.last_direction == 'Up':
				self.up()
			self.x += self.vx
			self.y += self.vy
			self.row = self.y//(WIDTH//ROWS)
			self.col = self.x//(WIDTH//ROWS)

			self.snake_list.append((self.row, self.col))

			if len(self.snake_list) > self.maxlength:
				coord_end = self.snake_list.pop(0)
				dict_blocks[coord_end].make_reset()
				available[coord_end] = dict_blocks[coord_end]

			if self.snake_list.count((self.row, self.col)) > 1:
				return True

class Button():
	def __init__(self,x,y,text, width, height, color, hover_color, act_color, func, isImage, *arg):
		self.x = x
		self.y = y
		self.text = text 
		self.width = width
		self.height = height
		self.color = color
		self.resting_color = color
		self.hover_color = hover_color
		self.act_color = act_color
		self.func = func
		self.isImage = isImage
		self.image = list(arg)
		self.changed_img = []
		if self.isImage:
			for image in self.image:
				image = pg.transform.scale(image, (self.width, self.height))
				image.set_colorkey(BLACK)
				self.changed_img.append(image)

	def update(self):
		mousex, mousey = pg.mouse.get_pos()

		if (pg.mouse.get_pressed()[0]) and (mousex > self.x) and (mousex < self.x+self.width) and (mousey>self.y) and (mousey<self.y+self.height):
			if not self.isImage:
				self.color = self.act_color
			else:
				self.image = self.changed_img[2]
			self.action()
		elif (mousex > self.x) and (mousex < self.x+self.width) and (mousey>self.y) and (mousey<self.y+self.height):
			if not self.isImage:
				self.color = self.hover_color
			else:
				self.image = self.changed_img[1]
		else:
			if not self.isImage:
				self.color = self.resting_color
			else:
				self.image = self.changed_img[0]

	def draw(self, win):	
		pg.draw.rect(win, self.color, pg.Rect(self.x,self.y,self.width, self.height))
		if not self.isImage:
			draw_text(win, self.x+self.width/2, self.y+self.height/2,self.text, 20,WHITE)
		else:
			win.blit(self.image, pg.Rect(self.x,self.y,self.width, self.height))
	def action(self):
		self.func()

def draw_grid(win):
	for i in range(ROWS):
		pg.draw.line(win, BLACK, (WIDTH//ROWS * i, 0), (WIDTH//ROWS * i, WIDTH))
		pg.draw.line(win, BLACK, (0, WIDTH//ROWS * i), (WIDTH, WIDTH//ROWS * i))

def checkWinner():
	win_flag = True
	for block in dict_blocks.values():
		if block.is_reset() or block.is_food():
			win_flag = False
	return win_flag

def food_list(how_many):
	new_foods = []
	for i in range(how_many):
		try:
			new_food = random.choice(list(available.items()))
			new_foods.append(new_food[1])
			available.pop(new_food[0])
			if not available:
				break
		except IndexError:
			break
	return new_foods

def make_food_block(how_many_food):	
	new_foods = food_list(how_many_food)
	if not new_foods:
		return
	for food in new_foods:
		food.make_food()

def make_wall(pos):
	x , y = pos 
	row = y//(WIDTH//ROWS)
	col = x//(WIDTH//ROWS)
	remove = dict_blocks.pop((row, col))
	available.pop((row,col))
	remove.make_wall()
	removed[row,col] = remove

def make_normal(pos):
	x, y = pos
	row = y//(WIDTH//ROWS)
	col = x//(WIDTH//ROWS)
	added = removed.pop((row, col))
	available[(row, col)] = added
	dict_blocks[(row, col)] = added
	added.make_reset()


#load images
bg = pg.image.load(path.join(img_folder, 'bg.jpg')).convert()
bg_rect = bg.get_rect()

star = pg.image.load(path.join(img_folder, 'Magical rainbow star.png')).convert()
star2 = pg.image.load(path.join(img_folder, 'Magical rainbow star2.png')).convert()
star3 = pg.image.load(path.join(img_folder, 'Magical rainbow star3.png')).convert()

#load music
collect = pg.mixer.Sound(path.join(snd_folder, 'Pickup_Coin31.wav'))
collect.set_volume(0.4)
smash = pg.mixer.Sound(path.join(snd_folder, 'Hit_Hurt.wav'))
smash.set_volume(0.4)

pg.mixer.music.load(path.join(snd_folder, 'ChillLofiR.mp3'))
pg.mixer.music.set_volume(0.9)
pg.mixer.music.play(loops=-1)

removed = {}
won = False
game_over = True
running = True
how_many_food = 1
while running:
	if game_over:
		show_go_screen()
		dict_blocks = {}
		for i in range(ROWS):
			for j in range(ROWS):
				d = Blocks(WIDTH//ROWS * i, WIDTH//ROWS * j, WIDTH//ROWS)
				dict_blocks[d.position()] = d
		available = dict_blocks.copy()
		try:
			q = Snake(og, og2)
		except:
			q = Snake(5,200)
		b= Button(WIDTH+10, WIDTH//9*8,'Clear', 80, 30, PINK, DARKERPINK, DARKPINK,action,False, None)
		setting = Button(WIDTH+70, WIDTH//2-15, '',30,30, LIGHTBLUE, LIGHTBLUE, LIGHTBLUE,settings,True,star,star2, star3)
		score = 0
		temp_running = True
		for i in removed.keys():
			remove = dict_blocks.pop(i)
			available.pop(i)
			remove.make_wall()
		while temp_running:
			for event in pg.event.get():	
				if event.type == pg.QUIT:
					pg.quit()
					exit()
				if event.type == pg.KEYDOWN:
					temp_running = False
					break


			if pg.mouse.get_pressed()[0]:
				try:
					make_wall(pg.mouse.get_pos())
				except KeyError:
					pass
			if pg.mouse.get_pressed()[2]:
				try:
					make_normal(pg.mouse.get_pos())
				except KeyError:
					pass
			b.update()
			setting.update()
			win.fill(BLUE)
			win.blit(bg,bg_rect)
			for block in dict_blocks.values():
				block.draw(win)
			draw_grid(win)
			draw_text(win, WIDTH+50, WIDTH/6, 'Score', 30, WHITE)
			draw_text(win, WIDTH+50, WIDTH/6+40, str(score), 20, WHITE)
			b.draw(win)
			setting.draw(win)
			#after drawing everything
			pg.display.flip()
		og = q.maxlength
		og2 = q.reload
		s = Snake(og, og2)
		del q
		make_food_block(how_many_food)
		del b
		game_over = False
		won = False
	#running at right speed
	clock.tick(FPS)
	#process input(event)
	for event in pg.event.get():	
		if event.type == pg.QUIT:
			running = False 
	#update

	try:
		snake_on = dict_blocks[s.position()]
		if snake_on.is_reset():
			snake_on.make_snake()
			available.pop(s.position())

		elif snake_on.is_food():
			collect.play()
			snake_on.make_snake()
			s.maxlength += 1
			make_food_block(how_many_food)
			score += 1
	except KeyError:
		smash.play()
		game_over = True
		sleep(1)

	if checkWinner():
		won = True
		game_over = True
		sleep(1)
	collide = s.update()
	if collide:
		smash.play()
		game_over = True
		sleep(1)
	#draw/render
	win.fill(BLUE)
	win.blit(bg,bg_rect)
	for block in dict_blocks.values():
		block.draw(win)
	draw_grid(win)
	draw_text(win, WIDTH+50, WIDTH/6, 'Score', 30, WHITE)
	draw_text(win, WIDTH+50, WIDTH/6+40, str(score), 20, WHITE)
	#after drawing everything
	pg.display.flip()

pg.quit()