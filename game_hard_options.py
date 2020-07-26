##################################
# tic-tac-toe                    #
# play against user or computer  #
# levels: easy, medium, hard     #
# easy: random moves             #
# medium: check wining/losing    #
# position in the nex move       #
# hard: check all future move    #
# using the minimax algorithm    #
##################################
import random, copy

class Game:


    def __init__(self, player1, player2):
        self.states_list = ["X wins", "O wins", "Draw"]
        self.player1 = player1
        self.player2 = player2
        self.state_matrix = [[" "," ", " "] for i in range(3)]  # initial state
        self.current_state = [False for _i in range(3)]
        self.symbol = "X"  # current symbol
        self.isfinished = "False"  # true if game is finished

        self.print_field()


    ##################################
    # Print the field                #
    ##################################
    def print_field(self):
        horizon_border = "-" * 9
        vert_border = "|"
        sp = " "

        print(horizon_border)
        for i in range(3):
            out_str = vert_border
            for j in range(3):
                out_str += sp + self.state_matrix[i][j]
            out_str += sp + vert_border
            print(out_str)
        print(horizon_border)

    ##################################
    #  Switch current symbol         #
    ##################################
    def switch_symbol(self, symbol):
        return "X" if symbol == "O" else "O"

    ##################################
    #  Find empty cells              #
    ##################################
    def find_empty(self, board):
        return [[i, j] for i in range(3) for j in range(3) if board[i][j] == " "]

    ##################################
    #  Next move by user             #
    ##################################
    def next_move_user(self):
        valid_move = False

        while not valid_move:
            coordinates = input("Enter the coordinates: > ").strip()

            # check for numerical values
            if not coordinates.replace(" ","").isnumeric():
                print("You should enter numbers!")
                continue

            x = int(coordinates.split()[0])
            y = int(coordinates.split()[1])

            x_index = x - 1  # transform x coordinate to the index of state_matrix
            y_index = 3 - y  # transform y coordinate to the index of state_matrix

            # check for range
            if x not in [1,2,3] or y not in [1,2,3]:
                print("Coordinates should be from 1 to 3!")
                continue

            # check whether the cell is occupied
            if self.state_matrix[y_index][x_index] != " ":
                print("This cell is occupied! Choose another one!")
                continue

            # update state and print the field
            valid_move = True
            self.state_matrix[y_index][x_index] = self.symbol
            self.symbol = self.switch_symbol(self.symbol)
            self.print_field()

    ##################################
    #  Next move by computer easy    #
    ##################################
    def next_move_easy(self):
        empty_ind = self.find_empty(self.state_matrix)
        rand_ind = random.randint(0, len(empty_ind) - 1)
        self.state_matrix[empty_ind[rand_ind][0]][empty_ind[rand_ind][1]] = self.symbol
        self.symbol = self.switch_symbol(self.symbol)
        print("Making move level \"easy\"")
        self.print_field()

    ##################################
    #  Next move by computer medium  #
    ##################################

    def next_move_medium(self):
        # find empty cells
        empty_ind = self.find_empty(self.state_matrix)

        # save attributes before virtual move
        copy_state_matrix = copy.deepcopy(self.state_matrix)  # save the state matrix and current state
        copy_current_state = copy.deepcopy(self.current_state)

        good_move = False

        # virtual move to win or draw
        for i in range(len(empty_ind)):
            self.state_matrix[empty_ind[i][0]][empty_ind[i][1]] = self.symbol
            self.analyze_state(self.state_matrix)
            if self.isfinished:
                good_move = True # virtual move is good
                break
            # restore attributes
            self.state_matrix = copy.deepcopy(copy_state_matrix)
            self.current_state = copy.deepcopy(copy_current_state)

        # if there is no winning move then a virtual move to defend
        if not good_move:
            self.symbol = self.switch_symbol(self.symbol)
            # virtual move to defend
            for i in range(len(empty_ind)):
                self.state_matrix[empty_ind[i][0]][empty_ind[i][1]] = self.symbol
                self.analyze_state(self.state_matrix)
                if self.isfinished:
                    good_move = True  # opponent is winning in one move
                    self.symbol = self.switch_symbol(self.symbol)
                    self.state_matrix[empty_ind[i][0]][empty_ind[i][1]] = self.symbol  # defend that cell
                    self.symbol = self.switch_symbol(self.symbol)
                    self.isfinished = False
                    self.current_state = copy.deepcopy(copy_current_state)
                    break
                # restore attributes
                self.state_matrix = copy.deepcopy(copy_state_matrix)
                self.current_state = copy.deepcopy(copy_current_state)
            self.symbol = self.switch_symbol(self.symbol)

        # if no winning or defending move, then random move
        if not good_move:
            rand_ind = random.randint(0, len(empty_ind) - 1)
            self.state_matrix[empty_ind[rand_ind][0]][empty_ind[rand_ind][1]] = self.symbol
        self.symbol = self.switch_symbol(self.symbol)
        print("Making move level \"medium\"")
        self.print_field()

    ##################################
    #  Next generic move             #
    ##################################
    def next_move(self, player):
        if player == "user":
            self.next_move_user()
        elif player == "easy":
            self.next_move_easy()
        elif player == "medium":
            self.next_move_medium()
        elif player == "hard":
            self.next_move_hard()


    ##################################
    #  Next move by computer hard    #
    ##################################
    def next_move_hard(self):

        # minimax algorithm for finding the best move
        # returns the value for the best move and the index of the corresponding cell
        def minimax(board, symbol):
            # copy_state = state[:]  # copy state, as analyze state can modify it
            self.analyze_state(board)
            # return value if terminate state, [-1.-1] for index, as there is no empty cells
            if (self.symbol == "X" and  self.current_state[0]) or (self.symbol == "O" and  self.current_state[1]):  # terminate state: win
                self.current_state = [False for _i in range(3)]  # restore state and return +10
                return 10, [-1,-1]
            if (self.symbol == "X" and  self.current_state[1]) or (self.symbol == "O" and  self.current_state[0]):  # terminate state: lose
                self.current_state = [False for _i in range(3)]  # restore state and return -10
                return -10, [-1,-1]
            if  self.current_state[2]:   # terminate state: draw
                self.current_state = [False for _i in range(3)]  # restore state and return  0
                return 0, [-1,-1]

            # else calculate the value recursively
            empty_ind_loc = self.find_empty(board)  # find empty cells

            if symbol == self.symbol:  # move of the player
                best_value = -20
                best_ind = [0, 0]
                for i in range(len(empty_ind_loc)):
                    # copy_board = board[::]  # copy board, as it will be modified
                    board[empty_ind_loc[i][0]][empty_ind_loc[i][1]] = symbol  # next virtual move
                    value, ind = minimax(board, self.switch_symbol(symbol))
                    if value > best_value:
                        best_value = value
                        best_ind = empty_ind_loc[i]
                    # board = copy_board[::]  # restore board
                    board[empty_ind_loc[i][0]][empty_ind_loc[i][1]] = " "  # undo virtual move
                return best_value, best_ind

            else:  # move of the opponent
                best_value = 20
                best_ind = [0, 0]
                for i in range(len(empty_ind_loc)):
                    # copy_board = board[::]  # copy board, as it will be modified
                    board[empty_ind_loc[i][0]][empty_ind_loc[i][1]] = symbol  # next virtual move
                    value, ind = minimax(board, self.switch_symbol(symbol))
                    if value < best_value:
                        best_value = value
                        best_ind = empty_ind_loc[i]
                    # board = copy_board[::]  # restore board
                    board[empty_ind_loc[i][0]][empty_ind_loc[i][1]] = " "  # undo virtual move
                return best_value, best_ind

        empty_ind = self.find_empty(self.state_matrix)  # find empty cells
        best_value, best_ind = minimax(self.state_matrix, self.symbol)  # call mminimax to find the best move
        self.state_matrix[best_ind[0]][best_ind[1]] = self.symbol  # make a move
        self.symbol = self.switch_symbol(self.symbol)
        print("Making move level \"hard\"")
        self.print_field()

    #######################
    # analyze the state   #
    #######################
    def analyze_state(self, board):  # analyzes the state and change current_state respectively, if game is finished

     # check for XXX or OOO in a raw
        for i in range(3):
            is_the_same = True
            for j in range(2):
                if board[i][j] != board[i][j + 1]:
                    is_the_same = False
            if is_the_same and board[i][j] == "X":
                 self.current_state[0] = True
            if is_the_same and board[i][j] == "O":
                 self.current_state[1] = True

        # check for XXX or OOO in a column
        for j in range(3):
            is_the_same = True
            for i in range(2):
                if board[i][j] != board[i + 1][j]:
                    is_the_same = False
            if is_the_same and board[i][j] == "X":
                 self.current_state[0] = True
            if is_the_same and board[i][j] == "O":
                 self.current_state[1] = True

        # check for XXX or OOO on both diagonals
        is_the_same1 = True
        is_the_same2 = True
        for i in range(2):
            if board[i][i] != board[i + 1][i + 1]:
                is_the_same1 = False
            if board[i][2 - i] != board[i + 1][2 - i - 1]:
                is_the_same2 = False

        if is_the_same1 and board[0][0] == "X":
             self.current_state[0] = True
        if is_the_same1 and board[0][0] == "O":
             self.current_state[1] = True

        if is_the_same2 and board[0][2] == "X":
             self.current_state[0] = True
        if is_the_same2 and board[0][2] == "O":
             self.current_state[1] = True

        if len(self.find_empty(board)) == 0 and not any(self.current_state[0:2]):  # Draw
             self.current_state[2] = True

        self.isfinished = any(self.current_state)
    ########################################
    # print the result if gane is finished #
    ########################################
    def finish(self):

        # print outcome of the game
        if self.current_state[0]:  # X wins
            print(self.states_list[0])
            return
        if self.current_state[1]:  # O wins
            print(self.states_list[1])
            return
        if self.current_state[2]:  # Draw
            print(self.states_list[2])

    #################################
    # play the game until finished  #
    #################################

    def play(self):
        player = self.player1
        while True:
            self.next_move(player)
            self.analyze_state(self.state_matrix)
            if self.isfinished:
                self.finish()
                break  # game is finished
            player = self.player2 if player == self.player1 else self.player1  # switch the player


####################################################################
#  Get the input and determines who plays for player1 and player2  #
####################################################################

def get_input():
    mode_options =  ["user", "easy", "medium", "hard"] # modes of game
    global exit_session, player1, player2
    while True:
        input_error = False
        inp_list = input("Input command: > ").strip().split()
        # print(inp_list[1])
        # print(inp_list[2])
        # print(inp_list[1] not in mode_options)
        if inp_list[0] == "exit":
            exit_session = True
            break
        if len(inp_list) != 3:
            input_error = True
        elif inp_list[0] != "start" or inp_list[1] not in mode_options or inp_list[2] not in mode_options:
            input_error = True
        if not input_error:
            player1, player2 = inp_list[1], inp_list[2]
            break
        print("Bad parameters!")

player1, player2 = "", ""
exit_session = False



# Main loop
while True:
    get_input()
    if exit_session:
        break
    game = Game(player1, player2)
    game.play()








