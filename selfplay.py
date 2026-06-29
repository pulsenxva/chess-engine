import chess
from engine import minimax
from main import print_evaluation, check_game_status

def main():
  board = chess.Board()
  game = []
  while 1:
    state = check_game_status(board, game)
    if state == True: return
    print(board)
    bestMove, bestScore = minimax(board, 0, -1000000, 1000000)
    print(bestMove)
    board.push(bestMove)
    game.append(bestMove)
    print_evaluation(board)

if __name__=="__main__":
  main()
