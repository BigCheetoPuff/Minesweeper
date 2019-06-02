import minesweeper






resp = ""

while "easy" not in resp and "hard" not in resp:
    resp = input("Welcome to minesweeper, would you like an easy or hard board? (easy/hard)")

if "easy" in resp:
    board = minesweeper.Board(8)
else:
    board = minesweeper.Board(16)

print("Input your move with x,y (-f for flag). The top left corner is 0,0")

game_status = minesweeper.Board.PLAYING
while game_status is minesweeper.Board.PLAYING:

    board.pretty_print()

    resp = input(":")
    if board.process_comm(resp) is False:
        print("Please put in a valid move")
    else:
        info = board.process_comm(resp)
        board.do_move(info)

        game_status = board.check_game_status(info)


if game_status is minesweeper.Board.WON:
    print("You won")
else:
    print("you lost")
    board.pretty_print(show_mines= True)





