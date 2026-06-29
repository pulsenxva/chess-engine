import chess
from evaluate import evaluate

def ordered_moves(board: chess.Board):
  moves = list(board.legal_moves)
  def move_key(move):
    score = 0
    if board.is_capture(move): score += 10
    if move.promotion: score += 20
    if board.gives_check(move): score += 15
    return -score
  return sorted(moves, key = move_key)

def minimax(board: chess.Board, depth: int, alpha: int, beta: int):
  if depth == 4 or board.is_game_over(): return None, evaluate(board)

  if board.turn == chess.WHITE:
    mxScore = -1000000
    bestMove = None

    for move in ordered_moves(board):
      board.push(move)
      nmove, nscore = minimax(board, depth+1, alpha, beta)
      board.pop()

      if nscore > mxScore:
        mxScore = nscore
        bestMove = move

        # can prune this 
      if mxScore >= beta:
        break
      alpha = max(alpha, mxScore)

    return bestMove, mxScore
  else:
    mnScore = 1000000
    bestMove = None

    for move in board.legal_moves:
      board.push(move)
      nmove, nscore = minimax(board, depth+1, alpha, beta)
      board.pop()

      if(nscore < mnScore):
        mnScore = nscore
        bestMove = move

      if mnScore <= alpha:
        break
      beta = min(beta, mnScore)

    return bestMove, mnScore
