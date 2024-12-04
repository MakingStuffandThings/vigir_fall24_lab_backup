import chess
import chess.engine

'''def Zs_for_Pieces(board,square):
    piece=board.piece_at(square)
    pieces=[]
'''
Robot_world=[300,300]

'''def chess_move_to_position(move):

    #square size is 4 mm, so middle of square is 2mm x 2mm
    file_to_x = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    rank_to_y = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}

    if len(move) != 4:
        raise ValueError("Invalid move format. Moves must be in the format 'e4e2', 'd5d7', etc.")
    start_piece=[file_to_x[move[0]]*4,rank_to_y[move[1]]*4]

    x = file_to_x[move[2]]
    y = rank_to_y[move[3]]

    return x, y
'''

def inspect_piece_at_square(board):
    square=input("Enter a squre to know what piece is there> ")
    square_UCI = chess.square(ord(square[0]) - ord('a'), int(square[1])-1)
    
    piece=board.piece_at(square_UCI)
    if piece is None:
        print("There is no piece here")
        return
    else:
        color=piece.color
        if(color):
            color="white"
        else:
            color="black"

        symbol=piece.symbol()
        print("The piece at",square,"is a",color,symbol)
    return color,symbol


















def print_board(board):
    print(board)

def main():
    # Initialize the chess board and engine
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("X:\chess_stuff\stockfish\stockfish-windows-x86-64-avx2.exe")  # Update with the correct path
    while not board.is_game_over():
        print_board(board)
        if board.turn == chess.WHITE:
            move = input("White's move:  (type 'resign' to concede or 'inspect' to inspect a square) ")
            if move=="inspect":
              inspect_piece_at_square(board)
              continue

            if move == "resign": 
                print("You have resigned.") 
                board.turn=chess.BLACK
                #board.push("Null")
                break
                
            try:
                # Convert player move to a chess.Move object
                move = chess.Move.from_uci(move)
                board.push(move)
            except ValueError:
                print("Invalid move! Please try again.")
                continue
        else:
            result = engine.play(board, chess.engine.Limit(time=2.0))
            print(f"AI raw move: {chess.Move.from_uci(result.move.uci())}")  # Debug print for the AI move
            try:
                # Convert AI move to a chess.Move object
                move = chess.Move.from_uci(result.move.uci())
                if move == "resign": 
                    print("Black has resigned.") 
                    board.turn=chess.WHITE
                    #board.push("Null")
                    break
                board.push(move)
                print(f"Black's move: {result.move.uci()}")
            except ValueError:
                print("Invalid move from AI!")
                continue

    print("Game over!")
    
    print(board.result())
    engine.quit()
    if(board.turn==chess.WHITE):
        print("The winner is white")
    else:
        print("The winner is black")

if __name__ == "__main__":
    main()

