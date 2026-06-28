import chess

#TODO pawn bonus, king bonus, rename eval

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 100000,
}

def eval(board: chess.Board):
    if(board.is_checkmate()):
        if(board.turn == chess.WHITE): return -100000
        return 100000
    
    if(board.is_stalemate()): return 0
    if(board.is_insufficient_material()): return 0
    
    score = 0
    for p_type, p_val in PIECE_VALUES.items():
        white = board.pieces(p_type, chess.WHITE)
        black = board.pieces(p_type, chess.BLACK)
        score += p_val*(len(white)-len(black))
    return score
