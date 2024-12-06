#import chess
#import chess.engine

'''def Zs_for_Pieces(board,square):
    piece=board.piece_at(square)
    pieces=[]
'''
zoffset=0
travel_z=0
#pass moves as follows piece symbol,
#p=pawn
#r=rook
#n=knight
#b=bishop
#q=queen
#k=king

#use 90 90 30 OAT when grabbing

OAT=" 90 90 30"
Robot_board = [
    [(390, 140), (390, 120), (390, 80), (390, 40), (390, 0), (390, -40), (390, -80), (390, -120)],
    [(350, 140), (350, 120), (350, 80), (350, 40), (350, 0), (350, -40), (350, -80), (350, -120)],
    [(310, 140), (310, 120), (310, 80), (310, 40), (310, 0), (310, -40), (310, -80), (310, -120)],
    [(270, 140), (270, 120), (270, 80), (270, 40), (270, 0), (270, -40), (270, -80), (270, -120)],
    [(230, 140), (230, 120), (230, 80), (230, 40), (230, 0), (230, -40), (230, -80), (230, -120)],
    [(190, 140), (190, 120), (190, 80), (190, 40), (190, 0), (190, -40), (190, -80), (190, -120)],
    [(150, 140), (150, 120), (150, 80), (150, 40), (150, 0), (150, -40), (150, -80), (150, -120)],
    [(120, 140), (120, 120), (120, 80), (120, 40), (120, 0), (120, -40), (120, -80), (120, -120)]
]

def get_chess_piece_value(piece_char):
    # Define a dictionary to map chess pieces to specific values
    piece_values = {
        'p': -145+zoffset,
        'r': -145+zoffset,
        'n': -135+zoffset,
        'b': -135+zoffset,   
        'q': -120+zoffset,
        'k': -120+zoffset

    }
    
    # Check if the character is one of the specified chess pieces
    if piece_char in piece_values:
        return piece_values[piece_char]
    else:
        return 'Invalid piece'

def letter_to_number(letter):
    # Convert the letter (a-h) to a number (1-8)
    return ord(letter.lower()) - ord('a')


def play_move(move):
    z=get_chess_piece_value(move[0])
    if(z=="Invalid piece"):
        return "Fail"
    
   
    fPos=Robot_board[letter_to_number(move[1])][int(move[2])-1]
    fPos=fPos+(z,)
    print(fPos)
    
    
    #print(Robot_board[0][2])
    
    
    first_command="Puma_MovetoXYZOAT "+str(fPos[0])+" "+str(fPos[1])+" "+str(fPos[2])+OAT
    print(first_command)


def main():
   play_move( input("Enter a move in the form pe2e4 where p is the piece symbol, and e2e4 is the start space and end space\n>"))





#move z height = 0
#pawn grab = -140   Drop -120
#king grab = -120   Drop -100

#x range 120 to 390
#y range -120 to 120
#min z = -140

#far right corner x 390  y  -120 

#MIN X =170
#MAX X =400
 
#max x y = 355 205
#min x y =





#to get robot ready, use 



'''def chess_move_to_position(move):

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

# def main():
#     # Initialize the chess board and engine
#     board = chess.Board()
#     engine = chess.engine.SimpleEngine.popen_uci("X:\chess_stuff\stockfish\stockfish-windows-x86-64-avx2.exe")  # Update with the correct path
#     while not board.is_game_over():
#         print_board(board)
#         if board.turn == chess.WHITE:
#             move = input("White's move:  (type 'resign' to concede or 'inspect' to inspect a square) ")
#             if move=="inspect":
#               inspect_piece_at_square(board)
#               continue

#             if move == "resign": 
#                 print("You have resigned.") 
#                 board.turn=chess.BLACK
#                 #board.push("Null")
#                 break
                
#             try:
#                 # Convert player move to a chess.Move object
#                 move = chess.Move.from_uci(move)
#                 board.push(move)
#             except ValueError:
#                 print("Invalid move! Please try again.")
#                 continue
#         else:
#             result = engine.play(board, chess.engine.Limit(time=2.0))
#             print(f"AI raw move: {chess.Move.from_uci(result.move.uci())}")  # Debug print for the AI move
#             try:
#                 # Convert AI move to a chess.Move object
#                 move = chess.Move.from_uci(result.move.uci())
#                 if move == "resign": 
#                     print("Black has resigned.") 
#                     board.turn=chess.WHITE
#                     #board.push("Null")
#                     break
#                 board.push(move)
#                 print(f"Black's move: {result.move.uci()}")
#             except ValueError:
#                 print("Invalid move from AI!")
#                 continue

#     print("Game over!")
    
#     print(board.result())
#     engine.quit()
#     if(board.turn==chess.WHITE):
#         print("The winner is white")
#     else:
#         print("The winner is black")

if __name__ == "__main__":
    main()
