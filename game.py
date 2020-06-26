##################################
# tic-tac-toe                    #
##################################

horizon_border = "-" * 9
vert_border = "|"
sp = " "

state_matrix = [[" "," ", " "] for i in range(3)]  # initial state
states_list = ["X wins", "O wins", "Draw"]
current_state = [False for _i in range(3)]



##################################
# Print the field                #
##################################
def print_field():
    print(horizon_border)
    for i in range(3):
        out_str = vert_border
        for j in range(3):
            out_str += sp + state_matrix[i][j]
        out_str += sp + vert_border
        print(out_str)
    print(horizon_border)

##################################
#  Next move                     #
##################################
def next_move():
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
        if state_matrix[y_index][x_index] != " ":
            print("This cell is occupied! Choose another one!")
            continue

        # update state and pritn the field
        valid_move = True
        state_matrix[y_index][x_index] = symbol
        print_field()

#######################
# analyze the state
########################




# num_un = inp_string.count(" ")



X_move = True  # X or O move
num_empty = 9  # number of empty cells

while True:
    print_field()
    symbol = "X" if X_move else "O"
    next_move()
    X_move = not X_move
    num_empty -= 1
    ########################
    # analyze the state    #
    ########################

    # check for XXX or OOO in a raw
    for i in range(3):
        is_the_same = True
        for j in range(2):
            if state_matrix[i][j] != state_matrix[i][j + 1]:
                is_the_same = False
        if is_the_same and state_matrix[i][j] == "X":
            current_state[0] = True
        if is_the_same and state_matrix[i][j] == "O":
            current_state[1] = True

    # check for XXX or OOO in a column
    for j in range(3):
        is_the_same = True
        for i in range(2):
            if state_matrix[i][j] != state_matrix[i + 1][j]:
                is_the_same = False
        if is_the_same and state_matrix[i][j] == "X":
            current_state[0] = True
        if is_the_same and state_matrix[i][j] == "O":
            current_state[1] = True

    # check for XXX or OOO on both diagonals
    is_the_same1 = True
    is_the_same2 = True
    for i in range(2):
        if state_matrix[i][i] != state_matrix[i + 1][i + 1]:
            is_the_same1 = False
        if state_matrix[i][2 - i] != state_matrix[i + 1][2 - i - 1]:
            is_the_same2 = False

    if is_the_same1 and state_matrix[0][0] == "X":
        current_state[0] = True
    if is_the_same1 and state_matrix[0][0] == "O":
        current_state[1] = True

    if is_the_same2 and state_matrix[0][2] == "X":
        current_state[0] = True
    if is_the_same2 and state_matrix[0][2] == "O":
        current_state[1] = True

    ###############################################
    # classify possible states
    if current_state[0]:  # X wins
        print(states_list[0])
        break
    if current_state[1]:  # O wins
        print(states_list[1])
        break
    if num_empty == 0:  # Draw
        print(states_list[2])
        break




