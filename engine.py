import chess
from evaluate import eval

#TODO alpha-beta
#TODO add terminal points

def minimax(board: chess.Board, depth: int, iswhite: bool):
    score = eval(board)
    if depth == 4 or board.is_game_over(): return None, score
    if iswhite:
        mxScore = -1000000
        bestMove = None
        for move in board.legal_moves:
            next = board.copy()
            next.push(move)
            nmove, nscore = minimax(next, depth+1, not iswhite)
            if nscore > mxScore:
                mxScore = nscore
                bestMove = move
        return bestMove, mxScore
    else:
        mnScore = 1000000
        bestMove = None
        for move in board.legal_moves:
            next = board.copy()
            next.push(move);
            nmove, nscore = minimax(next, depth+1, not iswhite)
            if(nscore < mnScore):
                mnScore = nscore
                bestMove = move
        return bestMove, mnScore
