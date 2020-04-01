from core.tic_tac_toe import Game

if __name__ == '__main__':
    while True:
        game = Game(online=True)
        game.start()
        enter = input('Enter any key to start a new round. Enter q to quit.')
        if enter == 'q':
            break
