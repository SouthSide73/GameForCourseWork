import sys
import pygame
from tkinter.messagebox import showinfo
from tkinter import Tk


# Постоянные
WIDTH = 512
HEIGHT = 512
rows = 8
cols = 8
DIMENSHION = 8   # Размер доски 8х8
SQ_SIZE = HEIGHT // DIMENSHION
IMAGES = {}


class Game:
	def __init__(self):
		self.turn = 0
		self.token_black = 0
		self.token_white = 0
		self.players = ['wc', 'bc']
		self.selected_token = None
		self.flag_win = False
		self.not_jump = False
		self.jumping = False
		self.str4 = ""
		self.flag_black_add = False
		self.flag_white_add = False
		self.board = [['++', 'bc', '++', 'bc', '++', 'bc', '++', 'bc'],
					  ['bc', '++', 'bc', '++', 'bc', '++', 'bc', '++'],
					  ['++', 'bc', '++', 'bc', '++', 'bc', '++', 'bc'],
					  ['--', '++', '--', '++', '--', '++', '--', '++'],
					  ['++', '--', '++', '--', '++', '--', '++', '--'],
					  ['wc', '++', 'wc', '++', 'wc', '++', 'wc', '++'],
					  ['++', 'wc', '++', 'wc', '++', 'wc', '++', 'wc'],
					  ['wc', '++', 'wc', '++', 'wc', '++', 'wc', '++']]

	def evaluate_click(self, mouse_pos):

		'''
		Функция для работы с координатами
		'''

		to_loc = get_clicked_row(mouse_pos), get_clicked_column(mouse_pos)
		if self.flag_black_add:
			to_loc = get_clicked_row(mouse_pos), get_clicked_column(mouse_pos)
			if self.board[to_loc[0]][to_loc[1]] == "--" and get_clicked_row(mouse_pos) <= 3:
				self.board[to_loc[0]][to_loc[1]] = "bc"
				self.token_black -= 1
				self.next_turn()
			self.flag_black_add = False
		if self.flag_white_add:
			to_loc = get_clicked_row(mouse_pos), get_clicked_column(mouse_pos)
			if self.board[to_loc[0]][to_loc[1]] == "--" and get_clicked_row(mouse_pos) >= 4:
				self.board[to_loc[0]][to_loc[1]] = "wc"
				self.token_white -= 1
				self.next_turn()
			self.flag_white_add = False
		player = self.players[self.turn % 2]
		if mouse_pos[0] > 550 and mouse_pos[0] < 730 and mouse_pos[1] > 30 and mouse_pos[1] < 110 and player == "bc":
			if self.token_black > 0:
				self.flag_black_add = True
		if mouse_pos[0] > 550 and mouse_pos[0] < 730 and mouse_pos[1] > 400 and mouse_pos[1] < 480 and player == "wc":
			if self.token_white > 0:
				self.flag_white_add = True
		if self.selected_token and mouse_pos[0] < 512 and mouse_pos[1] < 512:
			move = self.is_valid_move(player, self.selected_token, to_loc)
			if move[0]:
				self.play(player, self.selected_token, to_loc, move[1])
			else:
				self.selected_token = None
				if self.jumping:
					self.jumping = False
					self.next_turn()
		elif not self.selected_token and mouse_pos[0] < 512 and mouse_pos[1] < 512:
			if self.board[to_loc[0]][to_loc[1]].lower() == player:
				self.selected_token = to_loc

	def is_valid_move(self, player, from_loc, to_loc):

		'''
		Проверка хода
		'''

		from_row = from_loc[0]
		from_col = from_loc[1]
		to_row = to_loc[0]
		to_col = to_loc[1]
		token_char = self.board[from_row][from_col]

		if self.board[to_row][to_col] != '--':
			return False, None
		if (((token_char.isupper() and abs(from_row - to_row) == 1) or (player == 'bc' and to_row - from_row == 1) or
			(player == 'wc' and from_row - to_row == 1)) and abs(from_col - to_col) == 1) and not self.jumping:
			return True, None
		if (((token_char.isupper() and abs(from_row - to_row) == 2) or (player == 'bc' and to_row - from_row == 2) or
			(player == 'wc' and from_row - to_row == 2)) and abs(from_col - to_col) == 2):
			jump_row = (to_row - from_row) / 2 + from_row
			jump_col = (to_col - from_col) / 2 + from_col
			if self.board[int(jump_row)][int(jump_col)].lower() not in ['--']:
				return True, [jump_row, jump_col]
		return False, None

	# Обозначение клеток от a до h и от 1 до 8.
	ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}

	def play(self, player, from_loc, to_loc, jump, auto=False):

		'''
		Перемещение и проверка конца игры
		'''

		from_row = from_loc[0]
		from_col = from_loc[1]
		to_row = to_loc[0]
		to_col = to_loc[1]
		token_char = self.board[from_row][from_col]
		self.board[to_row][to_col] = token_char
		self.board[from_row][from_col] = '--'

		if not jump:
			self.not_jump = True
			self.str4 += " " + str(self.colsToFiles[from_col] + self.rowsToRanks[from_row] + "-" + self.colsToFiles[to_col] + self.rowsToRanks[to_row])

		if (player == 'bc' and to_row == 7) or (player == 'wc' and to_row == 0):
			self.board[to_row][to_col] = token_char.upper()

		if auto and jump is not None:
			for j in jump:
				self.board[int(j[0])][int(j[1])] = '--'
			self.selected_token = None
			self.jumping = False
			self.next_turn()
		elif jump:
			self.str4 += " " + str(self.colsToFiles[from_col] + self.rowsToRanks[from_row] + ":" + self.colsToFiles[to_col] + self.rowsToRanks[to_row])
			if (self.board[int(jump[0])][int(jump[1])] == "bc" and player == "bc") or \
					(self.board[int(jump[0])][int(jump[1])] == "BC" and player == "BC") or \
					(self.board[int(jump[0])][int(jump[1])] == "BC" and player == "bc") or \
					(self.board[int(jump[0])][int(jump[1])] == "bc" and player == "BC"):
				self.token_black += 1
			if (self.board[int(jump[0])][int(jump[1])] == "wc" and player == "wc") or \
				(self.board[int(jump[0])][int(jump[1])] == "WC" and player == "WC") or\
				(self.board[int(jump[0])][int(jump[1])] == "WC" and player == "wc") or\
				(self.board[int(jump[0])][int(jump[1])] == "wc" and player == "WC"):
				self.token_white += 1
			self.board[int(jump[0])][int(jump[1])] = '--'
			self.selected_token = [to_row, to_col]
			self.jumping = True
		else:
			self.selected_token = None
			self.next_turn()
		num = 0
		for row in range(DIMENSHION):
			for col in range(DIMENSHION):
				if self.board[row][col] == "bc" or self.board[row][col] == "BC":
					num = num + 1
		if num == 0:
			check_win("Победили белые")
			sys.exit()
		num = 0
		for row in range(DIMENSHION):
			for col in range(DIMENSHION):
				if self.board[row][col] == "wc" or self.board[row][col] == "WC":
					num = num + 1
		if num == 0:
			check_win("Победили черные")
			sys.exit()

	def next_turn(self):
		self.turn += 1

	def drawBoard(self):
		if self.not_jump:
			font = pygame.font.Font(None, 15)
			text = font.render(str(self.str4), True, (0, 0, 0), (200, 200, 200))
			place = text.get_rect(center=(635, 170))
			screen.blit(text, place)

		font = pygame.font.Font(None, 24)
		self.str = ""
		self.str = "В запасе черных:" + " " + str(self.token_black)
		text = font.render(str(self.str), True, (0, 0, 0))
		place = text.get_rect(center=(638, 70))
		screen.blit(text, place)

		font = pygame.font.Font(None, 24)
		self.str2 = ""
		self.str2 = "В запасе белых:" + " " + str(self.token_white)
		text = font.render(str(self.str2), True, (0, 0, 0))
		place = text.get_rect(center=(638, 440))
		screen.blit(text, place)

		font = pygame.font.Font(None, 40)
		self.str3 = ""
		player = self.players[self.turn % 2]
		if player == "bc":
			self.str3 = "Сейчас ходят:" + " черные"
		if player == "wc":
			self.str3 = "Сейчас ходят:" + " белые"
		text = font.render(str(self.str3), True, (0, 0, 0))
		place = text.get_rect(center=(220, 580))
		screen.blit(text, place)

		'''
		Создание графики игрового поля.
		'''

		colors = [pygame.Color('WHITE'), pygame.Color('DARK GRAY')]
		for row in range(DIMENSHION):
			for col in range(DIMENSHION):
				if row % 2 == 0:
					if col % 2 == 0:
						pygame.draw.rect(screen, colors[0], (row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE))
					else:
						pygame.draw.rect(screen, colors[1], (row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE))
				if row % 2 != 0:
					if col % 2 == 0:
						pygame.draw.rect(screen, colors[1], (row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE))
					else:
						pygame.draw.rect(screen, colors[0], (row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE))

		'''
		Рисует фигуры на доске, используя текущее состояние доски.
		'''

		IMAGES['bc'] = pygame.transform.scale(pygame.image.load("images/BlackCircle.png"), (SQ_SIZE, SQ_SIZE - 1))
		IMAGES['wc'] = pygame.transform.scale(pygame.image.load("images/WhiteCircle.png"), (SQ_SIZE, SQ_SIZE - 1))
		IMAGES['BC'] = pygame.transform.scale(pygame.image.load("images/BlackCrown.png"), (SQ_SIZE, SQ_SIZE - 1))
		IMAGES['WC'] = pygame.transform.scale(pygame.image.load("images/WhiteCrown.png"), (SQ_SIZE, SQ_SIZE - 1))
		# Теперь мы можем обратиться к изображению. Например, 'IMAGES['WC']'.

		for row in range(DIMENSHION):
			for col in range(DIMENSHION):
				piece = self.board[row][col]
				if piece != "--" and piece != "++":    # Не пустой квадрат
					screen.blit(IMAGES[piece], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
				if piece == "wc" and row == 0:
					self.board[row][col] = "WC"
					screen.blit(IMAGES["WC"], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
				if piece == "bc" and row == 7:
					self.board[row][col] = "BC"
					screen.blit(IMAGES["BC"], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
				if self.selected_token:
					if self.selected_token[0] == row and self.selected_token[1] == col:
						x = SQ_SIZE
						y = SQ_SIZE
						pygame.draw.rect(screen, "YELLOW", (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
				pygame.draw.rect(screen, "BLACK", (550, 30, 180, 80), 3)
				pygame.draw.rect(screen, "BLACK", (550, 400, 180, 80), 3)

# Определение строки и столбца
def get_clicked_column(mouse_pos):
	x = mouse_pos[0]
	for i in range(1, rows):
		if x < i * SQ_SIZE:
			return i - 1
	return rows - 1

def get_clicked_row(mouse_pos):
	y = mouse_pos[1]
	for i in range(1, cols):
		if y < i * SQ_SIZE:
			return i - 1
	return cols - 1

def check_win(message):
	root = Tk()  # Создаем главное окно
	root.withdraw()   # Cкрываем его
	answer = showinfo(title="Итог игры", message=message)


def main():
	global screen
	pygame.init()
	size = (WIDTH + 250, HEIGHT + 150)
	pygame.display.set_caption('Русские циклические шашки')
	screen = pygame.display.set_mode(size)
	game = Game()   # Старт игры
	running = True   # Флаг для проверки окончания работы программы
	clock = pygame.time.Clock()

	while running:
		for event in pygame.event.get():   # Пользователь что-то делает
			if event.type == pygame.QUIT:   # Если закрывает программу
				running = False   # Смена флага окончания программы
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				game.evaluate_click(pygame.mouse.get_pos())
		screen.fill("DARK GRAY")   # Фон окна
		pygame.draw.line(screen, "BLACK", [513, 513], [513, 0], 3)
		pygame.draw.line(screen, "BLACK", [0, 513], [513, 513], 3)
		game.drawBoard()   # Графика
		pygame.display.flip()   # Обновление окна
		clock.tick(60)   # 60 кадров в секунду

	pygame.quit()   # Закрытие программы

if __name__ == "__main__":
	main()
