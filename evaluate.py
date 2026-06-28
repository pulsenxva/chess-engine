import chess

#TODO king bonus, piece tables

PIECE_VALUES = {
  chess.PAWN: 100,
  chess.KNIGHT: 320,
  chess.BISHOP: 330,
  chess.ROOK: 500,
  chess.QUEEN: 900,
  chess.KING: 100000,
}

def material_bonus(board: chess.Board):
  score = 0
  for p_type, p_val in PIECE_VALUES.items():
    white = board.pieces(p_type, chess.WHITE)
    black = board.pieces(p_type, chess.BLACK)
    score += p_val * (len(white) - len(black))
  return score

def doubled_pawns(board: chess.Board):
  white = [0] * 8
  black = [0] * 8

  for square in board.pieces(chess.PAWN, chess.WHITE):
    file = chess.square_file(square)
    white[file] += 1

  for square in board.pieces(chess.PAWN, chess.BLACK):
    file = chess.square_file(square)
    black[file] += 1

  score = 0
  for i in range(0, 8):
    if white[i] > 1: score -= 40 * (white[i] - 1)
    if black[i] > 1: score += 40 * (black[i] - 1)

  return score

def mobility_bonus(board: chess.Board):
  score = 0;
  if board.turn == chess.WHITE:
    score += len(list(board.legal_moves)) * 1
    cpy = board.copy()
    cpy.turn = chess.BLACK
    score -= len(list(cpy.legal_moves)) * 1
  else:
    score -= len(list(board.legal_moves)) * 1
    cpy = board.copy()
    cpy.turn = chess.WHITE
    score += len(list(cpy.legal_moves)) * 1
  return score

def pawn_bonus(board: chess.Board):
  white_vals = [
    [0, 50, 50, 50, 50, 50, 50, 50],
    [40, 40, 40, 40, 40, 40, 40, 40],
    [30, 30, 30, 30, 30, 30, 30, 30],
    [20, 20, 20, 20, 20, 20, 20, 20],
    [13, 14, 15, 15, 15, 15, 14, 13],
    [8, 9, 10, 10, 10, 10, 9, 8],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
  ]

  score = 0
  for square in board.pieces(chess.PAWN, chess.WHITE):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    score += white_vals[rank][file]

  for square in board.pieces(chess.PAWN, chess.BLACK):
    rank = 7 - chess.square_rank(square)
    file = chess.square_file(square)
    score -= white_vals[rank][file]

  return score

def evaluate(board: chess.Board):
  if(board.is_checkmate()):
    if(board.turn == chess.WHITE): return -100000
    return 100000

  if(board.is_stalemate()): return 0
  if(board.is_insufficient_material()): return 0

  score = 0
  score += material_bonus(board)
  score += doubled_pawns(board)
  score += mobility_bonus(board)
  score += pawn_bonus(board)

  return score
