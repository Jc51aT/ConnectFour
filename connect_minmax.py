#!/usr/bin/env python3
# This program implements the game Connect 4 with an AI that runs on Minimax
import math
import time

class Board:
	rows = 6
	cols = 7

	def __init__(self):
		self.the_board = [[' ' for i in range(self.cols)] for j in range(self.rows)]
		
	#displays current board configuration
	def display_board(self):
		num_cols = [i for i in range(self.cols)]
		print("",*num_cols, sep=" ")

		for i in range(self.rows):
			print("|", end="")
			for j in range(self.cols):
				print(self.the_board[i][j]+"|", end="")
			print('\n')
		print('\n')

	# Checks to see if given column is full
	def is_column_full(self, col):
		for i in range(self.rows):
			if self.the_board[i][col] == " ":
				return False
			return True
	
	#Checks to see if the board is full
	def is_board_full(self):
		for c in range(self.cols):
			if not self.is_column_full(c):
				return False
		return True

	#Adds piece to current board at given column
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

	#Removes last piece from board at given column
	def remove_piece(self, col):
		i = 0
		while(i < self.rows and self.the_board[i][col] == ' '):
			i += 1

		if i == self.rows:
			return None
		else:
			self.the_board[i][col] = ' '

	#Returns a list of columns with available space
	def empty_spaces(self):
		empty = []
		
		for j in range(self.cols):
			if not self.is_column_full(j):
				empty.append((j))
		return empty

	#checks to see if given player has won the game
	def has_won(self, player):
		
		player = 'X' if player == 0 else 'O'

		#horizontal win
		for c in range(self.cols-3):
			for r in range(self.rows):
				if self.the_board[r][c] == ' ':
					continue
				elif self.the_board[r][c] == player and self.the_board[r][c+1] == player and self.the_board[r][c+2] == player and self.the_board[r][c+3] == player:
					return True

		#vertical win
		for c in range(self.cols):
			for r in range(self.rows-3):
				if self.the_board[r][c] == ' ':
					continue
				elif self.the_board[r][c] == player and self.the_board[r+1][c] == player and self.the_board[r+2][c] == player and self.the_board[r+3][c] == player:
					return True

		#pos diaganols win
		for c in range(self.cols-3):
			for r in range(self.rows-3):
				if self.the_board[r][c] == ' ':
					continue
				elif self.the_board[r][c] == player and self.the_board[r+1][c+1] == player and self.the_board[r+2][c+2] == player and self.the_board[r+3][c+3] == player:
					return True

		#neg diaganols win
		for c in range(self.cols-3):
			for r in range(3, self.rows):
				if self.the_board[r][c] == ' ':
					continue
				elif self.the_board[r][c] == player and self.the_board[r-1][c+1] == player and self.the_board[r-2][c+2] == player and self.the_board[r-3][c+3] == player:
					return True

	#This method returns the number of pieces in the center of the board for a given player
	def number_middle_pieces(self, player):
		player = 'X' if player == 0 else 'O'
		num_pieces = 0

		for r in range(self.rows):
			for c in range(2,5):
				if self.the_board[r][c] == player:
					num_pieces += 1
		return num_pieces

	#Checks if given player has won the game if not checks to see if player has more piece in center of the board
	def evaluate(self, player):
		opponet = 1 if player == 0 else 0
		 
		if player == 0: 
			if self.has_won(player):
				return 100
			elif self.number_middle_pieces(player) > self.number_middle_pieces(opponet):
				return 50
			else:
				return 0
		elif player == 1: 
			if self.has_won(player):
				return -100
			elif self.number_middle_pieces(player) > self.number_middle_pieces(opponet):
				return -50
			else:
				return 0

	#Finds the best move biased off of evaluation function
	def minimax(self, depth, player):
		
		if player == 0:
			best_move = [None, -math.inf]
		else:
			best_move = [None, math.inf]

		if depth == 0 or self.has_won(player) or self.is_board_full():
			score = self.evaluate(player)
			return [None,score]

		for emp_space in self.empty_spaces():
			
			col = emp_space
			self.add_piece(col, player)
			score = self.minimax(depth-1, (player+1) % 2)
			self.remove_piece(col)
			score[0] = col

			if player == 0 and score[1] > best_move[1]:
					 best_move = score
			elif player != 0 and score[1] < best_move[1]:
					 best_move = score
		
		return best_move

def main():
	new_board = Board()
	new_board.display_board()
	#Player 1 is always the human
	current_player = 1
	game_done = False

	while(not game_done):

		if current_player == 1:
			# get current player input
			while True:
				
				try:
					print("Enter Column:", end=' ')
					user_move = int(input())
				except ValueError:
					print("Not an integer!")
					continue
				else:
					break

			while user_move > new_board.cols or user_move < 0 or new_board.is_column_full(user_move):
				print("Enter a valid column")
				print("Enter Column:", end=' ')
				user_move = int(input())

			new_board.add_piece(user_move, current_player)
			new_board.display_board()
			
		else:
			#get cpu move
			cpu_move = new_board.minimax(5, current_player)
			new_board.add_piece(cpu_move[0], current_player)
			print("The computer played in column {}".format(cpu_move[0]))
			new_board.display_board()
			
		#check for winner
		if new_board.has_won(current_player):
			game_done = True
			print("{current_player} has won!".format(current_player = "CPU" if current_player == 0 else "Player 1"))
		#switch player turn
		else:
			current_player = (current_player + 1) % 2

if __name__ == "__main__":
	main()

	
	
