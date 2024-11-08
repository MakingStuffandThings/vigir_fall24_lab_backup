import chess
import chess.engine

def print_board(board):
    print(board)

def main():
    # Initialize the chess board and engine
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci("X:\chess_stuff\stockfish\stockfish-windows-x86-64-avx2.exe")  # Update with the correct path
    while not board.is_game_over():
        print_board(board)
        if board.turn == chess.WHITE:
            move = input("White's move:  (type 'resign' to concede)")
            if move.lower() == "resign": 
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
                if move.lower() == "resign": 
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
