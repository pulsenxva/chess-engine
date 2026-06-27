import chess
from engine import minimax

#TODO improve board

def check_game_status(board: chess.Board):
    if(board.is_checkmate()):
        if(board.turn == chess.WHITE):
            print("Black won")
        else:
            print("White won")
        return True
    elif(board.is_stalemate()):
        print("Stalemate")
        return True
    elif(board.is_insufficient_material()):
        print("Insufficient material")
        return True
    return False

def player_move(board: chess.Board):
    print(board)
    i = 1
    for move in board.legal_moves:
        print(i, move)
        i+=1
    
    idx = int(input("Your move (index):"))
    idx-=1
    
    move = list(board.legal_moves)[idx]
    board.push(move)

def engine_move(board: chess.Board, is_white: bool):
    print(board)
    bestMove, bestScore = minimax(board, 0, is_white)
    print("Engine's move: ", bestMove, bestScore)
    if(bestMove == None):
        print("helloworld im stupid(")
        board.push(list(board.legal_moves)[0])
    else:
        board.push(bestMove)

def main():
    board = chess.Board();
    white_move = True

    while 1:
        player_move(board)
        white_move = not white_move

        state = check_game_status(board)
        if state == True: return
        
        engine_move(board, white_move)
        white_move = not white_move

        state = check_game_status(board)
        if state == True: return

if __name__=="__main__":
    main()
