##################################
# tic-tac-toe                    #
# play against user or computer  #
# level: easy, medium            #
#                                #
##################################
import random, copy

class Game:


    def __init__(self, player1, player2):
        self.states_list = ["X wins", "O wins", "Draw"]
        self.player1 = player1
        self.player2 = player2
        self.state_matrix = [[" "," ", " "] for i in range(3)]  # initial state
        self.current_state = [False for _i in range(3)]
        self.num_empty = 9  # number of empty cells
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
    def switch_symbol(self):
        self.symbol = "X" if self.symbol == "O" else "O"
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

            # update state and pritn the field
            valid_move = True
            self.state_matrix[y_index][x_index] = self.symbol
            self.switch_symbol()
            self.print_field()

    ##################################
    #  Next move by computer easy    #
    ##################################
    def next_move_easy(self):
        empty_ind = [[i, j] for i in range(3) for j in range(3) if self.state_matrix[i][j] == " "]
        rand_ind = random.randint(0, len(empty_ind) - 1)
        self.state_matrix[empty_ind[rand_ind][0]][empty_ind[rand_ind][1]] = self.symbol
        self.switch_symbol()
        print("Making move level \"easy\"")
        self.print_field()

    ##################################
    #  Next move by computer medium  #
    ##################################

    def next_move_medium(self):
        # find empty cells
        empty_ind = [[i, j] for i in range(3) for j in range(3) if self.state_matrix[i][j] == " "]

        # save attributes before virtual move
        copy_state_matrix = copy.deepcopy(self.state_matrix)  # save the state matrix and current state
        copy_current_state = copy.deepcopy(self.current_state)

        good_move = False

        # virtual move to win or draw
        for i in range(len(empty_ind)):
            self.state_matrix[empty_ind[i][0]][empty_ind[i][1]] = self.symbol
            self.analyze_state()
            if self.isfinished:
                good_move = True # virtual move is good
                break
            # restore attributes
            self.state_matrix = copy.deepcopy(copy_state_matrix)
            self.current_state = copy.deepcopy(copy_current_state)

        # if there is no winning move then a virtual move to defend
        if not good_move:
            self.switch_symbol()
            # virtual move to defend
            for i in range(len(empty_ind)):
                self.state_matrix[empty_ind[i][0]][empty_ind[i][1]] = self.symbol
                self.analyze_state()
                if self.isfinished:
                    good_move = True  # opponent is winning in one move
                    self.switch_symbol()
                    self.state_matrix[empty_ind[i][0]][empty_ind[i][1]] = self.symbol  # defend that cell
                    self.switch_symbol()
                    self.isfinished = False
                    self.current_state = copy.deepcopy(copy_current_state)
                    break
                # restore attributes
                self.state_matrix = copy.deepcopy(copy_state_matrix)
                self.current_state = copy.deepcopy(copy_current_state)
            self.switch_symbol()

        # if no winning or defending move, then random move
        if not good_move:
            rand_ind = random.randint(0, len(empty_ind) - 1)
            self.state_matrix[empty_ind[rand_ind][0]][empty_ind[rand_ind][1]] = self.symbol
        self.switch_symbol()
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
        self.num_empty -= 1

    #######################
    # analyze the state   #
    #######################
    def analyze_state(self):  # analyzes the state and change current_state respectively, if game is finished

     # check for XXX or OOO in a raw
        for i in range(3):
            is_the_same = True
            for j in range(2):
                if self.state_matrix[i][j] != self.state_matrix[i][j + 1]:
                    is_the_same = False
            if is_the_same and self.state_matrix[i][j] == "X":
                self.current_state[0] = True
            if is_the_same and self.state_matrix[i][j] == "O":
                self.current_state[1] = True

        # check for XXX or OOO in a column
        for j in range(3):
            is_the_same = True
            for i in range(2):
                if self.state_matrix[i][j] != self.state_matrix[i + 1][j]:
                    is_the_same = False
            if is_the_same and self.state_matrix[i][j] == "X":
                self.current_state[0] = True
            if is_the_same and self.state_matrix[i][j] == "O":
                self.current_state[1] = True

        # check for XXX or OOO on both diagonals
        is_the_same1 = True
        is_the_same2 = True
        for i in range(2):
            if self.state_matrix[i][i] != self.state_matrix[i + 1][i + 1]:
                is_the_same1 = False
            if self.state_matrix[i][2 - i] != self.state_matrix[i + 1][2 - i - 1]:
                is_the_same2 = False

        if is_the_same1 and self.state_matrix[0][0] == "X":
            self.current_state[0] = True
        if is_the_same1 and self.state_matrix[0][0] == "O":
            self.current_state[1] = True

        if is_the_same2 and self.state_matrix[0][2] == "X":
            self.current_state[0] = True
        if is_the_same2 and self.state_matrix[0][2] == "O":
            self.current_state[1] = True

        if self.num_empty == 0:  # Draw
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
        if self.num_empty == 0:  # Draw
            print(self.states_list[2])

    #################################
    # play the game until finished  #
    #################################

    def play(self):
        player = self.player1
        while True:
            self.next_move(player)
            self.analyze_state()
            if self.isfinished:
                self.finish()
                break  # game is finished
            player = self.player2 if player == self.player1 else self.player1  # switch the player


####################################################################
#  Get the input and determines who plays for player1 and player2  #
####################################################################

def get_input():
    mode_options = ["user", "easy", "medium"]  # modes of game
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
    # player1, player2 = "medium", "medium"
    if exit_session:
        break
    game = Game(player1, player2)
    game.play()






