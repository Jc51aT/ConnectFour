

class Board:
	rows = 6
	cols = 7

	def __init__(self):
		self.the_board = [[' ' for i in range(self.cols)] for j in range(self.rows)]
		#print(self.the_board)

	def display_board(self):
		num_cols = [i for i in range(self.cols)]
		print("",*num_cols, sep=" ")

		for i in range(self.rows):
			print("|", end="")
			for j in range(self.cols):
				print(self.the_board[i][j]+"|", end="")
			print('\n')

	def clear_board(self):
		self.the_board = [[' ' for i in range(self.cols)] for j in range(self.rows)]

	def is_column_full(self, col):
		for i in range(self.rows):
			if self.the_board[i][col] == " ":
				return False
			return True

	def add_piece(self, col, piece):
		
		i = 0
		to_place = i -1
		while(i < self.rows and self.the_board[i][col] == ' '):
			to_place = i
			i += 1
			
		if piece == 0:
			self.the_board[to_place][col] = 'X'   
		else: 
			self.the_board[to_place][col] = 'O'

	def has_won(self, player):
		
		player = 'X' if player == 0 else 'O'

		#vertical win
		for c in range(self.cols-3):
			for r in range(self.rows):
				if self.the_board[r][c] == player and self.the_board[r][c+1] == player and self.the_board[r][c+2] == player and self.the_board[r][c+3] == player:
					return True

	# Check vertical locations for win
		for c in range(self.cols):
			for r in range(self.rows-3):
				if self.the_board[r][c] == player and self.the_board[r+1][c] == player and self.the_board[r+2][c] == player and self.the_board[r+3][c] == player:
					return True

		# Check positively sloped diaganols
		for c in range(self.cols-3):
			for r in range(self.rows-3):
				if self.the_board[r][c] == player and self.the_board[r+1][c+1] == player and self.the_board[r+2][c+2] == player and self.the_board[r+3][c+3] == player:
					return True

		# Check negatively sloped diaganols
		for c in range(self.cols-3):
			for r in range(3, self.rows):
				if self.the_board[r][c] == player and self.the_board[r-1][c+1] == player and self.the_board[r-2][c+2] == player and self.the_board[r-3][c+3] == player:
					return True

	
			

if __name__ == "__main__":
	new_board = Board()
	new_board.display_board()

	current_player = 0
	game_done = False

	while(not game_done):
	# get current player input

		user_move = 111

		while True:
			try:
				print("Enter Column:", end=' ')
				user_move = int(input())
			except ValueError:
				print("Not an integer!")
				continue
			else:
				break

		while user_move > new_board.cols or user_move < 0:
			print("Enter a valid column")
			print("Enter Column:", end=' ')
			user_move = int(input())

		while(new_board.is_column_full(user_move)):
				print("Column full, Try another column.")
				print("Enter Column:", end=' ')
				user_move = int(input())

		new_board.add_piece(user_move, current_player)
		new_board.display_board()
		if new_board.has_won(current_player):
			game_done = True
			print("Player {current_player} has won!".format(current_player = "Player 1" if current_player == 0 else "Player 2"))
		else:
			current_player = (current_player + 1) % 2