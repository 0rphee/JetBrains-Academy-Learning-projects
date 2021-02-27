def linear_search(array, to_find):
    for i in range(0, len(array)):
        if array[i] == to_find:
            return i
    return -1


def print_game(game):
    print(f'''---------
| {game[0]} {game[1]} {game[2]} |
| {game[3]} {game[4]} {game[5]} |
| {game[6]} {game[7]} {game[8]} |
---------''')


gs = [x for x in "         "]
winner = [[gs[0], gs[1], gs[2]],  # 0 Row
          [gs[3], gs[4], gs[5]],  # 1 Row
          [gs[6], gs[7], gs[8]],  # 2 Row
          [gs[0], gs[4], gs[8]],  # 3 Diagonal
          [gs[6], gs[4], gs[2]],  # 4 Diagonal
          [gs[0], gs[3], gs[6]],  # 5 Column
          [gs[1], gs[4], gs[7]],  # 6 Column
          [gs[2], gs[5], gs[8]]]  # 7 Column
print_game(gs)

perma_coords = [["1", "1"], ["1", "2"], ["1", "3"],
                ["2", "1"], ["2", "2"], ["2", "3"],
                ["3", "1"], ["3", "2"], ["3", "3"]]
# Valid inputs without taking into account occupied coordinates
valid_coordinates = [x for x in perma_coords]

# Example game, to be replaced with input() as its value
perm_gs = [x for x in gs]


# Obtains the available coordinates, i.e. the unoccupied ones
def obtain_actual_valid_coordinates(game, valid_coordinates):
    # Tracks where's the last free space in the game given
    av_space_index_in_valid_coordinates = 0
    # Stores the indeces where there's no "X", nor "O"
    available_spaces_indeces = []
    while av_space_index_in_valid_coordinates != -1:
        av_space_index_in_valid_coordinates = linear_search(game, " ")
        if av_space_index_in_valid_coordinates != -1:
            available_spaces_indeces.append(av_space_index_in_valid_coordinates)
            game[av_space_index_in_valid_coordinates] = "R"

    # Var with the coordinates available to use in format [1, 1], as a list
    ultimate_val_coordinates = []
    for index in available_spaces_indeces:
        ultimate_val_coordinates.append(valid_coordinates[index])

    # Removes the free spaces from the original 9x9 available coordinates, to obtain
    # a list with the occupied spaces
    for coordinate in ultimate_val_coordinates:
        valid_coordinates.remove(coordinate)
    return ultimate_val_coordinates, valid_coordinates


# Analyzes the input to obtain unoccupied coordinates
def valid_input(valid_coordinates, perma_coords):
    user_coords = input("Enter the coordinates: ")
    # Checks if the input are not digits
    not_digit = not user_coords.replace(" ", "").isdigit()
    # Checks if the input is not within the 9x9 grid
    temp_var = user_coords.split()
    found = linear_search(perma_coords, temp_var)
    not_inside_grid = linear_search(perma_coords, temp_var) == -1
    # Checks if the input is not a free space in the grid
    not_free_space = linear_search(valid_coordinates, user_coords.split()) == -1
    if not_digit:
        print("You should enter numbers!")
        return valid_input(valid_coordinates, perma_coords)
    elif not_inside_grid:
        print("Coordinates should be from 1 to 3!")
        return valid_input(valid_coordinates, perma_coords)
    elif not_free_space:
        print("This cell is occupied! choose another one!")
        return valid_input(valid_coordinates, perma_coords)
    else:
        return user_coords.split()


def insert_move(coordinates, game, x_or_o):
    game_index_to_insert = linear_search(perma_coords, coordinates)
    game[game_index_to_insert] = x_or_o
    return game


def replace_R(gs):
    R_index = 0
    # Stores the indeces where there's no "X", nor "O"
    R_indeces = []
    while R_index != -1:
        R_index = linear_search(gs, "R")
        if R_index != -1:
            R_indeces.append(R_index)
            gs[R_index] = " "
    return gs


def check_win(kk):
    winners = [[kk[0], kk[1], kk[2]],  # 0 Row
               [kk[3], kk[4], kk[5]],  # 1 Row
               [kk[6], kk[7], kk[8]],  # 2 Row
               [kk[0], kk[4], kk[8]],  # 3 Diagonal
               [kk[6], kk[4], kk[2]],  # 4 Diagonal
               [kk[0], kk[3], kk[6]],  # 5 Column
               [kk[1], kk[4], kk[7]],  # 6 Column
               [kk[2], kk[5], kk[8]]]  # 7 Column
    white_counter = kk.count(" ")

    if ["X", "X", "X"] in winners:
        print("X wins")
        return "finished"
    elif ["O", "O", "O"] in winners:
        print("O wins")
        return "finished"
    elif white_counter > 0:
        return "no"
    else:
        print("Draw")
        return "finished"


def move(gs, valid_coordinates, turn) -> bool:
    # The occupied coordinates and unoccupied ones are assigned to their respective variables
    valid_and_occupied_coordinates = obtain_actual_valid_coordinates(gs, valid_coordinates)
    valid_coordinates = valid_and_occupied_coordinates[0]
    occupied_coordinates = valid_and_occupied_coordinates[1]

    # Checks the input given the spaces available in the grid
    gs = insert_move(valid_input(valid_coordinates, perma_coords), perm_gs, turn)
    print_game(gs)


won = False
X_goes = "X"
while not won:
    move(gs, valid_coordinates, X_goes)
    gs = [x for x in perm_gs]
    valid_coordinates = [x for x in perma_coords]
    if check_win(gs) == "finished":
        won = True
    if X_goes == "X":
        X_goes = "O"
    else:
        X_goes = "X"
