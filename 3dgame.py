import pygame
import math

WIDTH = 1200
HALF_WIDTH = 600
HEIGHT = 800
HALF_HEIGHT = 400
fps = 60
tile = 50
fps_pos = (WIDTH - 65, 5)


#minimap
minimap_scale = 5
minimap_tile = tile // minimap_scale
map_pos = (0, HEIGHT - HEIGHT // minimap_scale)


FOW = math.pi // 3
HALF_FOW = FOW / 2
num_rays = 300
#max_dist = 800
delta_angle = FOW / num_rays
dist = num_rays / (2 * math.tan(HALF_FOW))
proj_coeff = dist * tile * 2
scale = WIDTH // num_rays

#texture settings (1200, 1200)
texture_width = 1200
texture_height = 1200
texture_scale = texture_width / tile

#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (220, 0, 0)
green = (0, 220, 0)
blue = (48, 193, 230)
gray = (150, 150, 150)
purpure = (120, 0, 120)
floor = (70, 70, 70)
yellow = (220, 220, 0)

#player
player_pos = (WIDTH // 2, HEIGHT // 2)
player_angle = 0
player_speed = 2

class Drawing:
	def __init__(self, win, miniwin):
		self.win = win
		self.miniwin = miniwin
		self.font = pygame.font.SysFont('Comic Sans MS', 36, bold=True)
		self.texture = pygame.image.load('текстура кота.png').convert()


	def background(self):
		pygame.draw.rect(self.win, blue, (0, 0, WIDTH, HALF_HEIGHT))
		pygame.draw.rect(self.win, floor, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

	def cast(self, player_pos, player_angle):
		ray_casting(self.win, player_pos, player_angle, self.texture)

	def fps(self, clock):
		display_fps = str(int(clock.get_fps()))
		render = self.font.render(display_fps, 0, red)
		self.win.blit(render, fps_pos)

	def map_draw(self, player):
		self.miniwin.fill(black)
		map_x, map_y = (player.x // minimap_scale, player.y // minimap_scale)
		pygame.draw.circle(self.miniwin, red, (int(map_x), int(map_y)), 6)
		pygame.draw.line(self.miniwin, yellow, (map_x, map_y), 
					(map_x + 12 * math.cos(player.angle), 
					(map_y + 12 * math.sin(player.angle))))

		for t,u in mini_map:
			pygame.draw.rect(self.miniwin, green, (t, u, minimap_tile, minimap_tile))
		self.win.blit(self.miniwin, map_pos)

class Player:
	def __init__(self):
		self.x, self.y = player_pos
		self.angle = player_angle
	@property
	def pos(self):
		return (self.x, self.y)
	
	def movement(self):
		sin_a = math.sin(self.angle)
		cos_a = math.cos(self.angle)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.x += player_speed * cos_a
			self.y += player_speed * sin_a
		if keys[pygame.K_s]:
			self.x += -player_speed * cos_a
			self.y += -player_speed * sin_a
		if keys[pygame.K_a]:
			self.y -= player_speed * cos_a
			self.x += player_speed * sin_a
		if keys[pygame.K_d]:
			self.y += player_speed * cos_a
			self.x -= player_speed * sin_a
		if keys[pygame.K_LEFT]:
			self.angle -= 0.04
		if keys[pygame.K_RIGHT]:
			self.angle += 0.04
		if keys[pygame.K_q]:
			self.x, self.y = 600, 400
"""
text_map = [
'WWWWWWWWWWWWWWWWWWWWWWWW',
'W....W.....WW....W.....W',
'W...WW....W.....WW....WW',
'W.......W..W........W..W',
'W........W..W........W.W',
'W..W..WW...WW..W..WW...W',
'W......W...........W...W',
'W....W...........W.....W',
'W...WW..........WW....WW',
'W.......W..WW.......W..W',
'W........W...........W.W',
'W..W..WW.......W..WW...W',
'W......W...WW......W...W',
'W......................W',
'W......................W',
'WWWWWWWWWWWWWWWWWWWWWWWW'
]
"""

text_map = [
'WWWWWWWWWWWWWWWWWWWWWWWW',
'W..........WW..........W',
'W..........WW..........W',
'W..WW......WW..........W',
'W..........WW..........W',
'W..........WW..........W',
'W..........WW..........W',
'W......................W',
'W...............WW.....W',
'W.....WW...............W',
'W......................W',
'W......................W',
'W...WW.....WW..........W',
'W..........WW.....WW...W',
'W..........WW..........W',
'WWWWWWWWWWWWWWWWWWWWWWWW'
]

world_map = set()
mini_map = set()
for j, row in enumerate(text_map):
	for i, char in enumerate(row):
		if char == 'W':
			world_map.add((i * tile, j * tile)) #100 is size of block in pixels
			mini_map.add((i * minimap_tile, j * minimap_tile))

def our_rect(a, b):
	return (a // tile) * tile, (b // tile) * tile

def ray_casting(win, player_pos, player_angle, texture):
	ox, oy = player_pos
	xm, ym = our_rect(ox, oy)
	cur_angle = player_angle - HALF_FOW
	for ray in range(num_rays):
		sin_a = math.sin(cur_angle)
		cos_a = math.cos(cur_angle)
		#verticals
		x, dx = (xm + tile, 1) if cos_a >= 0 else (xm, -1)
		for i in range(0, WIDTH, tile):
			depth_v = (x - ox) / cos_a
			yv = oy + depth_v * sin_a
			if our_rect(x + dx, yv) in world_map:
				break
			x += (dx * tile)

		#horisontal
		y, dy = (ym + tile, 1) if sin_a >= 0 else (ym, -1)
		for i in range(0, HEIGHT, tile):
			depth_h = (y - oy) / sin_a
			xh = ox + depth_h * cos_a
			if our_rect(xh, y + dy) in world_map:
				break
			y += (dy * tile)

		#proj
		depth, offset = (depth_v, yv) if depth_v < depth_h else (depth_h, xh)
		offset = int(offset) % tile
		depth *= math.cos(player_angle - cur_angle)
		proj_height = min(int(proj_coeff / depth), HEIGHT + 100)

		wall_column = texture.subsurface(offset * texture_scale, 0, texture_scale, texture_height)
		wall_column = pygame.transform.scale(wall_column, (scale, proj_height))
		win.blit(wall_column, (ray * scale, HALF_HEIGHT - proj_height // 2))

		
		cur_angle += delta_angle

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
miniwin = pygame.Surface((WIDTH // minimap_scale, HEIGHT // minimap_scale))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(win, miniwin)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
	player.movement()
	drawing.background()
	drawing.cast(player.pos, player.angle)
	drawing.fps(clock)
	drawing.map_draw(player)
	
	pygame.display.flip()
	clock.tick(fps)