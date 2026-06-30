import chess
from evaluate import evaluate

#transposotion_table = {}

def ordered_moves(board: chess.Board):
  moves = list(board.legal_moves)
  def move_key(move):
    score = 0
    if board.is_capture(move): score += 10
    if move.promotion: score += 20
    if board.gives_check(move): score += 15
    return -score
  return sorted(moves, key = move_key)

def ordered_captures(board: chess.Board):
  moves = [m for m in board.legal_moves if board.is_capture(m)]
  def move_key(move):
    score = 0
    if move.promotion: score += 20
    if board.gives_check(move): score += 15
    return -score
  return sorted(moves, key=move_key)

def quiesce(board: chess.Board, alpha: int, beta: int, depth: int):
  if depth > 6: return evaluate(board)
  stand_pat = evaluate(board)

  if board.turn == chess.WHITE:
    if stand_pat >= beta: return beta
    alpha = max(alpha, stand_pat)
    for move in ordered_captures(board):
      board.push(move)
      score = quiesce(board, alpha, beta, depth+1)
      board.pop()

      alpha = max(alpha, score)

      if score >= beta:
        return beta
    return alpha
  else:
    if stand_pat <= alpha: return alpha
    beta = min(beta, stand_pat)
    for move in ordered_captures(board):
      board.push(move)
      score = quiesce(board, alpha, beta, depth+1)
      board.pop()

      beta = min(beta, score)

      if score <= alpha:
        return alpha
    return beta

def minimax(board: chess.Board, depth: int, alpha: int, beta: int):
  if depth == 4 or board.is_game_over(): return None, quiesce(board, alpha, beta, 0)

  #key = board.fen, depth
  #if key in transposotion_table:
  #  return transposotion_table[key]

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

    #transposotion_table[key] = bestMove, mxScore
    return bestMove, mxScore
  else:
    mnScore = 1000000
    bestMove = None

    for move in ordered_moves(board):
      board.push(move)
      nmove, nscore = minimax(board, depth+1, alpha, beta)
      board.pop()

      if(nscore < mnScore):
        mnScore = nscore
        bestMove = move

      if mnScore <= alpha:
        break
      beta = min(beta, mnScore)

    #transposotion_table[key] = bestMove, mnScore
    return bestMove, mnScore
