import chess
from engine import minimax
from evaluate import evaluate
from evaluate import get_bonuses

#TODO improve board

def check_game_status(board: chess.Board, game):
  if board.is_checkmate():
    print(board)

    if(board.turn == chess.WHITE):
      print("Black won")
    else:
      print("White won")

    print(game)
    return True
  elif(board.is_stalemate()):
    print(board)
    print("Stalemate")
    print(game)
    return True
  elif(board.is_insufficient_material()):
    print(board)
    print("Insufficient material")
    print(game)
    return True
  return False

def print_evaluation(board: chess.Board):
  bonuses = get_bonuses(board)
  print(bonuses)
  print(evaluate(board))

def player_move(board: chess.Board, game):
  print(board)
  i = 1
  out = []
  for move in board.legal_moves:
    out.append(f"{i}:{move}")
    i+=1
  print("Legal moves:")
  print(" ".join(out))
  
  val = input("Your move (index/string):").strip()
  if val == "exit":
    return False

  try:
    val = int(val)

    if val > len(list(board.legal_moves)) or val < 1:
      print("Error")
      return player_move(board, game)

    val-=1
    move = list(board.legal_moves)[val]
    board.push(move)
    game.append(move)
    print(evaluate(board))
    return True
  except ValueError:
    try:
      move = chess.Move.from_uci(str(val))
      if move in board.legal_moves:
        board.push(move)
        game.append(move)
        print(evaluate(board))
        return True
      else:
        print("Error")
        return player_move(board,game)
    except chess.InvalidMoveError:
      print("Error")
      return player_move(board, game)

def engine_move(board: chess.Board, game):
  print(board)
  bestMove, bestScore = minimax(board, 0, -1000000, 1000000)
  print("Engine's move: ", bestMove, bestScore)
  if(bestMove == None):
    print("helloworld im stupid(")
    board.push(list(board.legal_moves)[0])
  else:
    board.push(bestMove)
    game.append(bestMove)
    print_evaluation(board)

def main():
  board = chess.Board()
  print_evaluation(board)
  game = []

  while 1:
    continues = player_move(board, game)
    print_evaluation(board)
    if not continues:
      print(game)
      return

    state = check_game_status(board, game)
    if state == True: return
    
    engine_move(board, game)

    state = check_game_status(board, game)
    if state == True: return

if __name__=="__main__":
  main()
