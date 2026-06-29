import chess

#TODO more king safety

PIECE_VALUES = {
  chess.PAWN: 100,
  chess.KNIGHT: 320,
  chess.BISHOP: 330,
  chess.ROOK: 500,
  chess.QUEEN: 900,
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
    if white[i] > 1: score -= 30 * (white[i] - 1)
    if black[i] > 1: score += 30 * (black[i] - 1)

  return score

def mobility_bonus(board: chess.Board):
  score = 0
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
    [50, 50, 50, 50, 50, 50, 50, 50],
    [40, 40, 40, 40, 40, 40, 40, 40],
    [25, 25, 25, 25, 25, 25, 25, 25],
    [13, 14, 15, 15, 15, 15, 14, 13],
    [7, 8, 9, 10, 10, 9, 8, 7],
    [8, 9, 9, 9, 9, 9, 9, 8],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
  ]

  score = 0
  for square in board.pieces(chess.PAWN, chess.WHITE):
    rank = 7-chess.square_rank(square)
    file = chess.square_file(square)
    if board.fullmove_number < 40: score += white_vals[rank][file]
    else: score += 2*white_vals[rank][file]

  for square in board.pieces(chess.PAWN, chess.BLACK):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    if board.fullmove_number < 40: score -= white_vals[rank][file]
    else: score -= 2*white_vals[rank][file]

  return score

def castling_bonus(board: chess.Board):
  score = 0
  w_king = board.king(chess.WHITE)
  b_king = board.king(chess.BLACK)

  if w_king == chess.G1:
    score += 50
    for square in board.pieces(chess.ROOK, chess.WHITE):
      if chess.square_file(square) == 7 and chess.square_rank(square) == 0:
        score -= 80
        break
  elif w_king == chess.C1:
    score += 50
    for square in board.pieces(chess.ROOK, chess.WHITE):
      if ((chess.square_file(square) == 0 or chess.square_file(square) == 1)
        and chess.square_rank(square) == 0):
        score -= 80
        break

  if b_king == chess.G8:
    score -= 50
    for square in board.pieces(chess.ROOK, chess.BLACK):
      if chess.square_file(square) == 7 and chess.square_rank(square) == 7:
        score += 80
        break
  elif b_king == chess.C8:
    score -= 50
    for square in board.pieces(chess.ROOK, chess.BLACK):
      if ((chess.square_file(square) == 0 or chess.square_file(square) == 1)
        and chess.square_rank(square) == 7):
        score += 80
        break

  return score

def knight_bonus(board: chess.Board):
  vals = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 0, 15, 15, 0, 10, 0],
    [0, 0, 7, 7, 7, 7, 0, 0],
    [0, 0, 10, 0, 0, 10, 0, 0],
    [0, 0, 0, 5, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
  ]

  # <= ~30 moves
  if board.fullmove_number > 30: return 0

  score = 0
  for square in board.pieces(chess.KNIGHT, chess.WHITE):
    rank = 7-chess.square_rank(square)
    file = chess.square_file(square)
    score += vals[rank][file]
  
  for square in board.pieces(chess.KNIGHT, chess.BLACK):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    score -= vals[rank][file]

  return score

def bishop_bonus(board: chess.Board):
  vals = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 15, 0, 0, 0, 0, 15, 0],
    [0, 0, 10, 0, 0, 10, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 10, 0, 0, 0, 0, 10, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
  ]

  if board.fullmove_number > 30: return 0

  score = 0
  for square in board.pieces(chess.BISHOP, chess.WHITE):
    rank = 7-chess.square_rank(square)
    file = chess.square_file(square)
    score += vals[rank][file]
  
  for square in board.pieces(chess.BISHOP, chess.BLACK):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    score -= vals[rank][file]

  return score


def get_bonuses(board: chess.Board):
  bonuses = []
  bonuses.append(material_bonus(board))
  bonuses.append(doubled_pawns(board))
  #bonuses.append(mobility_bonus(board))
  bonuses.append(pawn_bonus(board))
  bonuses.append(castling_bonus(board))
  bonuses.append(knight_bonus(board))
  bonuses.append(bishop_bonus(board))
  return bonuses


def evaluate(board: chess.Board):
  if(board.is_checkmate()):
    if(board.turn == chess.WHITE): return -100000
    return 100000

  if(board.is_stalemate()): return 0
  if(board.is_insufficient_material()): return 0
  if board.is_repetition(2): return 0
  
  score = 0
  score += material_bonus(board)
  score += doubled_pawns(board)
  score += mobility_bonus(board)
  score += pawn_bonus(board)
  score += castling_bonus(board)
  score += knight_bonus(board)
  score += bishop_bonus(board)

  return score
