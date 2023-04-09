import pygame, sys
import math
from queue import PriorityQueue
import random

pygame.init()

#set screen size
SCREEN_WIDTH = 800
SCREEN = pygame.display.set_mode((1024,SCREEN_WIDTH))
pygame.display.set_caption('Path-Finding Algorithms Visualizer')

#color options
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LGREEN = (101, 224, 101)
BLUE = (0, 0, 255)
LBLUE = (61, 100, 168)
ORANGE = (255,127,80)
GREY = (36, 36, 36)
BUTTON_OUTLINE_COLOR = (161, 178, 181)

#class for UI buttons
class Button():
	def __init__(self, win, color, x, y, width, height, text = ""):
		self.win = win
		self.color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.g = 0
		self.h = 0
		self.f = 0

	def create_button(self, tsize, button_outline = None):
		if button_outline:
			pygame.draw.rect(self.win, button_outline, (self.x - 4, self.y - 4, self.width + 8, self.height + 8))
		pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
		if self.text != "":
			font = pygame.font.SysFont('Arial', tsize)
			text = font.render(self.text, 1, (0, 0, 0))
			self.win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

#class for each node of the grid
class Node:
	def __init__(self, row, col, width, row_total):
		self.row = row
		self.col = col
		self.width = width
		self.row_total = row_total
		self.x = 224 + (row * width)
		self.y = col * width
		self.color = WHITE
		self.previous = None

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

	def make_start(self):
		self.color = GREEN
	def make_end(self):
		self.color = RED
	def make_barrier(self):
		self.color = BLACK
	def clear(self):
		self.color = WHITE
	def current_position(self):
		return self.row, self.col
	def considered(self):
		return self.color == RED

#clears the grid back to default
def clear(grid, rows, cols):
	for i in range(rows):
		for j in range(cols):
			grid[i][j].color = WHITE

#initally sets up the grid
def create_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)
	print(grid)
	return grid

#uses pygame methods to draw the lines of the grid
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (224, i * gap), (1024, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (224 + (j * gap), 0), (224 + (j * gap), width))

#draws all the nodes and then the grid lines to update the grid visually
def draw(win, grid, rows, width):
	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

#get mouse position when clicked
def get_clicked_position(pos, rows, width):
	gap = width // rows
	x = pos[0] - 225
	y = pos[1]
	row = x // gap
	col = y // gap
	return row, col

#draws a path from the current to start node
#used to visualize the path once the end node has been found
def draw_path(grid, start, end, win, rows, width):
	current = end.previous
	while current.previous and current != start:
		current.color = LGREEN
		current.draw(win)
		draw_grid(win, rows, width)
		pygame.display.update()
		current = current.previous
	return

#cleans the grid by leaving the obstacles and start/end point but clearing the searched nodes
def clean_grid(grid, rows, cols):
	for i in range(rows):
		for j in range(cols):
			if grid[i][j].color != BLACK and grid[i][j].color != GREEN and grid[i][j].color != RED:
				grid[i][j].color = WHITE

#algorithm for depth first search
def dfs(grid, rows, cols, start, end, win, width):
	clean_grid(grid, rows, cols)
	rowModifier = [-1, 1, 0, 0]
	colModifier = [0, 0, -1, 1]
	visited = []
	stack = []
	stack.append(start)
	while len(stack) > 0:
		current = stack.pop()
		if current == end:
			draw_path(grid, start, end, win, rows, width)
			return
		if current not in visited:
			visited.append(current)
			if current != start:
				current.color = LBLUE
				current.draw(win)
				draw_grid(win, rows, width)
				pygame.display.update()
		row = current.row
		col = current.col

		for i in range(4):
			adjx = row + rowModifier[i]
			adjy = col + colModifier[i]
			if (adjx >= 0 and adjy >= 0 and adjx < rows and adjy < cols) and (grid[adjx][adjy] not in visited) and (grid[adjx][adjy].color != BLACK):
				grid[adjx][adjy].previous = current
				stack.append(grid[adjx][adjy])

#algorithm for breadth first search
def bfs(grid, rows, cols, start, end, win, width):
	clean_grid(grid, rows, cols)
	rowModifier = [-1, 1, 0, 0]
	colModifier = [0, 0, -1, 1]
	visited = []
	queue = []
	queue.append(start)
	while len(queue) > 0:
		current = queue.pop(0)
		if current == end:
			draw_path(grid, start, end, win, rows, width)
			return
		if current != start and current != end:
				current.color = LBLUE
				current.draw(win)
				draw_grid(win, rows, width)
				pygame.display.update()

		row = current.row
		col = current.col

		for i in range(4):
			adjx = row + rowModifier[i]
			adjy = col + colModifier[i]
			if (adjx >= 0 and adjy >= 0 and adjx < rows and adjy < cols) and (grid[adjx][adjy] not in visited) and (grid[adjx][adjy].color != BLACK):
				grid[adjx][adjy].previous = current
				visited.append(grid[adjx][adjy])
				queue.append(grid[adjx][adjy])


# def djikstra(grid, rows, cols, start, end, win, width):
# 	pass

#def astar(grid, rows, cols, start, end, win, width):
#	pass

#creates and renders the visuals for the main menu
def create_menu(win):
	win.fill((101, 126, 130))
	title_rect = pygame.draw.rect(win, (75, 96, 99), (150, 40, 725, 175))
	title_rect2 = pygame.draw.rect(win, (115, 132, 135), (165, 55, 695, 145))
	font = pygame.font.SysFont('Arial', 64)
	credit_font = pygame.font.SysFont('Arial', 24)
	pfa_text = font.render("Path-Finding Algorithms", 1, (0, 0, 0))
	pfa_text_rect = pfa_text.get_rect(center=(1024/2, 800/2))
	win.blit(pfa_text, (pfa_text_rect[0], 55))
	v_text = font.render("Visualizer", 1, (0, 0, 0))
	v_text_rect = v_text.get_rect(center=(1024/2, 800/2))
	win.blit(v_text, (v_text_rect[0], 125))
	credit_text = credit_font.render("Created by Nathan Stanfield", 1, (0, 0, 0))
	win.blit(credit_text, (715, 770, 180, 50))

#repeated loop to run menu and visualization logic as well as draw update visuals
def main(win, width):
	place_start = place_end = place_barrier = False

	win.fill((101, 126, 130))
	ROWS = 50
	grid = create_grid(ROWS, width)

	start = None
	end = None
	menu = True
	dfs_selected = bfs_selected = astar_selected = False
	algorithm_running = False


	run = True
	found = False

	create_menu(win)

	while run:
		if menu:
			dfs_button_rect = pygame.Rect(422, 280, 180, 50)
			bfs_button_rect = pygame.Rect(422, 380, 180, 50)
			dijkstra_button_rect = pygame.Rect(422, 480, 180, 50)
			astar_button_rect = pygame.Rect(422, 580, 180, 50)
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()
				if dfs_button_rect.collidepoint(pos):
					dfs_button = Button(win, (227, 227, 227), 422, 280, 180, 50, "DFS")
					dfs_button.create_button(48, (138, 153, 156))
				else:
					dfs_button = Button(win, WHITE, 422, 280, 180, 50, "DFS")
					dfs_button.create_button(48, BUTTON_OUTLINE_COLOR)
				if bfs_button_rect.collidepoint(pos):
					bfs_button = Button(win, (227, 227, 227), 422, 380, 180, 50, "BFS")
					bfs_button.create_button(48, (138, 153, 156))
				else:
					bfs_button = Button(win, WHITE, 422, 380, 180, 50, "BFS")
					bfs_button.create_button(48, BUTTON_OUTLINE_COLOR)
				if dijkstra_button_rect.collidepoint(pos):
					dijkstra_button = Button(win, (227, 227, 227), 422, 480, 180, 50, "Dijkstra")
					dijkstra_button.create_button(48, (138, 153, 156))
				else:
					dijkstra_button = Button(win, WHITE, 422, 480, 180, 50, "Dijkstra")
					dijkstra_button.create_button(48, BUTTON_OUTLINE_COLOR)
				if astar_button_rect.collidepoint(pos):
					astar_button = Button(win, (227, 227, 227), 422, 580, 180, 50, "A*")
					astar_button.create_button(48, (138, 153, 156))
				else:
					astar_button = Button(win, WHITE, 422, 580, 180, 50, "A*")
					astar_button.create_button(48, BUTTON_OUTLINE_COLOR)
				if event.type == pygame.QUIT:
					run = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if dfs_button_rect.collidepoint(event.pos):
							win.fill((101, 126, 130))
							draw(win, grid, ROWS, width)
							menu = False
							dfs_selected = True
							bfs_selected = False
							astar_selected = False
						elif bfs_button_rect.collidepoint(event.pos):
							win.fill((101, 126, 130))
							draw(win, grid, ROWS, width)
							menu = False
							bfs_selected = True
							dfs_selected = False
							astar_selected = False
			pygame.display.update()
		elif not menu:
			run_button_rect = pygame.Rect(42, 210, 150, 35)
			sp_button_rect = pygame.Rect(42, 270, 150, 35)
			ep_button_rect = pygame.Rect(42, 330, 150, 35)
			barrier_button_rect = pygame.Rect(42, 390, 150, 35)
			clear_button_rect = pygame.Rect(42, 450, 150, 35)
			back_button_rect = pygame.Rect(42, 650, 150, 35)
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()
				if run_button_rect.collidepoint(pos):
					run_button = Button(win, (227, 227, 227), 42, 210, 150, 35, "Visualize")
					run_button.create_button(28, (138, 153, 156))
				else:
					run_button = Button(win, WHITE, 42, 210, 150, 35, "Visualize")
					run_button.create_button(28, BUTTON_OUTLINE_COLOR)
				if sp_button_rect.collidepoint(pos):
					sp_button = Button(win, (227, 227, 227), 42, 270, 150, 35, "Start Point")
					sp_button.create_button(28, (138, 153, 156))
				else:
					sp_button = Button(win, WHITE, 42, 270, 150, 35, "Start Point")
					sp_button.create_button(28, BUTTON_OUTLINE_COLOR)
				if ep_button_rect.collidepoint(pos):
					ep_button = Button(win, (227, 227, 227), 42, 330, 150, 35, "End Point")
					ep_button.create_button(28, (138, 153, 156))
				else:
					ep_button = Button(win, WHITE, 42, 330, 150, 35, "End Point")
					ep_button.create_button(28, BUTTON_OUTLINE_COLOR)
				if barrier_button_rect.collidepoint(pos):
					barrier_button = Button(win, (227, 227, 227), 42, 390, 150, 35, "Wall Barrier")
					barrier_button.create_button(28, (138, 153, 156))
				else:
					barrier_button = Button(win, WHITE, 42, 390, 150, 35, "Wall Barrier")
					barrier_button.create_button(28, BUTTON_OUTLINE_COLOR)
				if clear_button_rect.collidepoint(pos):
					clear_button = Button(win, (227, 227, 227), 42, 450, 150, 35, "Clear")
					clear_button.create_button(28, (138, 153, 156))
				else:
					clear_button = Button(win, WHITE, 42, 450, 150, 35, "Clear")
					clear_button.create_button(28, BUTTON_OUTLINE_COLOR)
				if back_button_rect.collidepoint(pos):
					back_button = Button(win, (227, 227, 227), 42, 650, 150, 35, "Back")
					back_button.create_button(28, (138, 153, 156))
				else:
					back_button = Button(win, WHITE, 42, 650, 150, 35, "Back")
					back_button.create_button(28, BUTTON_OUTLINE_COLOR)
				if event.type == pygame.QUIT:
					run = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if run_button_rect.collidepoint(event.pos):
							if dfs_selected and start != None and end != None:
								algorithm_running = True
								dfs(grid, ROWS, ROWS, start, end, win, width)
								algorithm_running = False
							elif bfs_selected and start != None and end != None:
								algorithm_running = True
								bfs(grid, ROWS, ROWS, start, end, win, width)
								algorithm_running = False
						if sp_button_rect.collidepoint(event.pos) and not algorithm_running:
							place_start = True
							place_end = place_barrier = False
						elif ep_button_rect.collidepoint(event.pos) and not algorithm_running:
							place_end = True
							place_start = place_barrier = False
						elif barrier_button_rect.collidepoint(event.pos) and not algorithm_running:
							place_barrier = True
							place_start = place_end = False
						elif clear_button_rect.collidepoint(event.pos) and not algorithm_running:
							clear(grid, ROWS, ROWS)
							draw(win, grid, ROWS, width)
							start = None
							end = None
						elif back_button_rect.collidepoint(event.pos) and not algorithm_running:
							clear(grid, ROWS, ROWS)
							start = None
							end = None
							create_menu(win)
							menu = True
					if (place_start or place_end) and pos[0] > 224:
						row, col = get_clicked_position(pos, ROWS, width)
						node = grid[row][col]
						if not start and node != end and place_start:
							start = node
							start.make_start()
							start.draw(win)
						elif start and node != end and place_start:
							start.clear()
							start = node
							start.make_start()
							start.draw(win)
						elif not end and node != start and place_end:
							end = node
							end.make_end()
						elif end and node != start and place_end:
							end.clear()
							end = node
							end.make_end()
						draw(win, grid, ROWS, width)
				if pygame.mouse.get_pressed()[0] and pos[0] > 224:
					row, col = get_clicked_position(pos, ROWS, width)
					node = grid[row][col]
					if node != end and node != start and place_barrier:
						node.make_barrier()
						draw(win, grid, ROWS, width)
				if not algorithm_running:
					pygame.display.update()
	pygame.quit()

main(SCREEN, SCREEN_WIDTH)