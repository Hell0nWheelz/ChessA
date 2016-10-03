import chess
import random
from operator import itemgetter

#This function is purely for testing purposes
def randomPlayer(board):
	move = random.choice(list(board.legal_moves))
	return move.uci()
	
def computerPlayer(board):
	#Call to get which move is best
	board_copy = board
	moveList = []
	bestMoves = []
	for i in board_copy.legal_moves:
		board_copy.push(i)
		score = alphaBetaMin(board_copy, float("-inf"), float("inf"), 5)
		board_copy.pop()
		moveList.append((i, score))
	
	#Get the best score from moves
	bestScore = sorted(moveList, key=itemgetter(1), reverse=True)[0][1]
	for i in moveList:
		if i[1] == bestScore:
			#Add best moves to list
			bestMoves.append(i[0])
			
	return random.choice(bestMoves) #Return random best move
	
def alphaBetaMax(board, alpha, beta, depth):
	if depth == 0 or board.is_checkmate() or board.is_stalemate():
		return evaluate(board)
	
	#Iterate through legal moves, DFS.
	for i in board.legal_moves:
		board.push(i)
		score = alphaBetaMin(board, alpha, beta, depth-1)
		board.pop()
		if score >= beta:
			return beta
		if score > alpha:
			alpha = score
	return alpha
	
def alphaBetaMin(board, alpha, beta, depth):
	if depth == 0 or board.is_checkmate() or board.is_stalemate():
		return -evaluate(board)
		
	for i in board.legal_moves:
		board.push(i)
		score = alphaBetaMax(board, alpha, beta, depth-1)
		board.pop()
		if score <= alpha:
			return alpha
		if score < beta:
			beta = score
	return beta
	
def evaluate(board):
	if board.turn != chess.WHITE:
		return heuristicX(board)
	else:
		return heuristicY(board)	

def heuristicX(board):
	score = 0
	score -= len(board.move_stack) #Number of moves
	score += 9001 if board.is_checkmate() else 0
	score += 99 if board.is_check() else 0
	score -= len(board.legal_moves) * 5
	
	for (piece, value) in [ (chess.KING, 0),
							(chess.ROOK, 300),
							(chess.KNIGHT, 100)]:
		score += len(board.pieces(piece, board.turn)) * value
		score -= len(board.pieces(piece, not board.turn)) * value
	return score

def heuristicY(board):
	score = 0
	score -= len(board.move_stack) #Number of moves
	score += 9001 if board.is_checkmate() else 0
	score += 99 if board.is_check() else 0
	score -= len(board.legal_moves) * 5
	
	for (piece, value) in [ (chess.KING, 0),
							(chess.ROOK, 300),
							(chess.KNIGHT, 100)]:
		score += len(board.pieces(piece, board.turn)) * value
		score -= len(board.pieces(piece, not board.turn)) * value
	return score