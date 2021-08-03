import random
import ast
f_domino_set = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [3, 3], [3, 4], [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 5],
                [5, 6], [6, 6]]


class PieceSet:
    stock_pieces = f_domino_set.copy()
    instances = dict()
    snake = []

    def piece_partition(self) -> list:
        returned_pieces = random.sample(PieceSet.stock_pieces, k=7)
        for piece in returned_pieces:
            if piece in returned_pieces:
                PieceSet.stock_pieces.remove(piece)
        return returned_pieces

    def __init__(self, instance_name):
        self.pieces = self.piece_partition()
        PieceSet.instances[instance_name] = self.pieces


class AiOptions():
    def __init__(self):
        self.n_count = dict()
        self.all_pieces = PieceSet.instances["computer"] + PieceSet.snake
        for piece in self.all_pieces:
            for num in piece:
                num = str(num)
                self.n_count[num] = self.n_count.get(num, 0) + 1
        self.value_pieces()

    def value_pieces(self):
        self.comp_piece_values = dict()
        for piece in PieceSet.instances["computer"]:
            for num in piece:
                piece = str(piece)
                num = str(num)
                self.comp_piece_values[piece] = self.comp_piece_values.get(piece, 0) + self.n_count[num]
        self.ordered_pieces = list(reversed(sorted(self.comp_piece_values, key=self.comp_piece_values.__getitem__)))

        # the list of strings: ['[1,1]', '[2,2]', etc] is converted to a list of lists: [[1,1], [2,2], etc]
        index = 0
        for piece in self.ordered_pieces:
            self.ordered_pieces.pop(index)
            piece = ast.literal_eval(piece)
            self.ordered_pieces.insert(index, piece)
            index += 1


def get_starting_piece() -> list:
    double_computer_pieces = sorted([i for i in PieceSet.instances["computer"] if i[0] == i[1]], reverse=True)
    double_player_pieces = sorted([i for i in PieceSet.instances["player"] if i[0] == i[1]], reverse=True)
    high_double_computer_piece = double_computer_pieces[0] if len(double_computer_pieces) > 0 else []
    high_double_player_piece = double_player_pieces[0] if len(double_player_pieces) > 0 else []
    maxes = sorted([high_double_computer_piece, high_double_player_piece], reverse=True)
    return [maxes[0]]


def whos_turn(player_p: list, computer_p: list, starting_piece: list) -> str:
    if starting_piece in PieceSet.stock_pieces:
        return "Repeat"
    elif starting_piece in player_p:
        PieceSet.instances["player"].remove(starting_piece)
        return "computer"
    elif starting_piece in computer_p:
        PieceSet.instances["computer"].remove(starting_piece)
        return "player"


def beginning():
    PieceSet.stock_pieces = f_domino_set.copy()
    PieceSet.instances = dict()
    player_pieces = PieceSet("player")
    computer_pieces = PieceSet("computer")
    PieceSet.snake = get_starting_piece()
    status = whos_turn(player_pieces.pieces, computer_pieces.pieces, PieceSet.snake[0])
    if status == "Repeat":
        beginning()
    elif status == "computer" or status == "player":
        print_ui(status)
        change_snake(status)
        status = check_end(status)
        return status


def main():
    status = beginning()
    midgame(status)


def midgame(status):
    while status == "player" or status == "computer":
        print_ui(status)
        change_snake(status)
        status = check_end(status)
    print_ui(status)


# this will call functions to figure how to add the piece the user and computer selected,
# to then print it
def change_snake(status: str, selected_piece=None):
    selected_piece_inside = False  # checks if the selected piece was passed as an argument or assigned internally
    if selected_piece is None:
        selected_piece = check_input(status, None)  # int: 1, 2, etc
        selected_piece_inside = True
        if selected_piece == "piece_added_to_snake":
            return
    orig_flip = obtain_piece(status, selected_piece)
    original_p, flipped_p = orig_flip[0], orig_flip[1]  # list: [1, 1]
    if selected_piece_inside == True:
        while original_p == "illegal_move" and status == "player":
            selected_piece = check_input(status, original_p)
            orig_flip = obtain_piece(status, selected_piece)
            original_p, flipped_p = orig_flip[0], orig_flip[1]
            # obtain_piece(status, selected_piece)

    # if the ai is testing the pieces in their value order and the move wasn't legal, it will try with the
    # next number on the list
    if selected_piece_inside == False and original_p == "illegal_move":
        return

    if original_p == "no_stock_pieces":
        return

    if selected_piece > 0:
        PieceSet.snake.append(flipped_p)
        PieceSet.instances[status].remove(original_p)
        return "piece_added_to_snake"
    elif selected_piece < 0:
        PieceSet.snake.insert(0, flipped_p)
        PieceSet.instances[status].remove(original_p)
        return "piece_added_to_snake"
    elif selected_piece == 0:
        PieceSet.instances[status].append(original_p)
        return "piece_from_stock"
    else:
        print("error")


# checks the status, aren't valid endgame conditions, it switches the turn: comp -> user OR user -> comp
def check_end(status: str) -> str:
    user = PieceSet.instances["player"]
    comp = PieceSet.instances["computer"]
    if len(user) == 0:
        return "The game is over. You won!"
    elif len(comp) == 0:
        return "The game is over. The computer won!"
    else:
        snake = PieceSet.snake
        if snake[0][0] == snake[-1][-1]:
            sus_num = snake[0][0]
            sus_num_count = 0
            for piece in snake:
                for n in piece:
                    if n == sus_num:
                        sus_num_count += 1
            if sus_num_count >= 8:
                return "The game is over. It's a draw!"
            else:
                if status == "player":
                    return "computer"
                elif status == "computer":
                    return "player"
                else:
                    return "error"
        else:
            if status == "player":
                return "computer"
            elif status == "computer":
                return "player"
            else:
                return "error"


# function that checks if the piece (1: [1, 1,] etc) the user inputs is still in their inventory, but if
# its the computer's turn, it will return a random number
def check_input(computer_or_player, illegal: str) -> int:
    if computer_or_player == "player":
        n_of_user_pieces = len(PieceSet.instances["player"])
        while True:
            try:
                user_cmd = int(input("Illegal move. Please try again." if illegal == "illegal_move" else ""))
                if -n_of_user_pieces > user_cmd or user_cmd > n_of_user_pieces:
                    print("Invalid input. Please try again.")
                else:
                    return user_cmd
            except ValueError:
                print("Invalid input. Please try again.")
    # here the computer's selected index is generated --------------------------
    elif computer_or_player == "computer":
        ai_options = AiOptions()
        input()
        for piece in ai_options.ordered_pieces:
            curr_piece_index = PieceSet.instances["computer"].index(piece)
            if change_snake("computer", selected_piece=curr_piece_index+1) == "piece_added_to_snake":
                return "piece_added_to_snake"
            else:
                curr_piece_index = -curr_piece_index
                if change_snake("computer", selected_piece=curr_piece_index-1) == "piece_added_to_snake":
                    return "piece_added_to_snake"
        else:
            return 0
    """elif computer_or_player == "computer":
        if illegal == "illegal_move":
            n_of_comp_pieces = len(PieceSet.instances["computer"])
            rand_comp_piece = random.randint(-n_of_comp_pieces, n_of_comp_pieces)
        else:
            n_of_comp_pieces = len(PieceSet.instances["computer"])
            rand_comp_piece = random.randint(-n_of_comp_pieces, n_of_comp_pieces)
            input()
        return rand_comp_piece"""


# in case of 0 in input, retrieves a random piece, if there aren't more, returns a str. Else,
# returns the piece that the player or computer selected.
def obtain_piece(comp_or_play: str, selected_piece: int):
    if selected_piece == 0:
        if len(PieceSet.stock_pieces) > 0:
            retrieved_piece = random.choice(PieceSet.stock_pieces)
            PieceSet.stock_pieces.remove(retrieved_piece)
            return [retrieved_piece, None]
        else:
            return "no_stock_pieces", None
    else:
        start_or_end = 0 if selected_piece < 0 else -1
        selected_piece = selected_piece if selected_piece > 0 else (-1 * selected_piece)  # int, the index -> 1: [1,1]
        actual_piece = PieceSet.instances[comp_or_play][selected_piece - 1].copy()  # list: [1,2]

        for num in actual_piece:  # number from [1, 2], be it 1 or 2
            num_to_match_in_snake = PieceSet.snake[start_or_end][
                start_or_end]  # [0, 1] [1, 2] be it the 2 from [1,2] or the 0 from [0,1]
            if num == num_to_match_in_snake:
                return [actual_piece,
                        rotate_piece(actual_piece, start_or_end)]  # the original [1, 2] then the flipped one [2, 1]
                # return PieceSet.instances[comp_or_play][selected_piece-1]
        else:
            return "illegal_move", None


def rotate_piece(piece: list, start_or_end: int):  # ([1, 1]  ,  0 or -1)
    adjacent_piece_number = PieceSet.snake[start_or_end][start_or_end]  # 1, 2, 3, 4, 5, 6 <- from [1, 2]
    reversed_piece = piece.copy()
    reversed_piece.reverse()
    if start_or_end == 0:
        return piece if piece[-1] == adjacent_piece_number else reversed_piece
    elif start_or_end == -1:
        return piece if piece[0] == adjacent_piece_number else reversed_piece
    else:
        return "error"


def print_ui(status):
    snake_str = ''
    # this conditional arranges the order of the snake, and adds the (...) if necessary
    if len(PieceSet.snake) > 6:
        first_three = ''
        last_three = ''
        for domino_p in PieceSet.snake[:3]:
            first_three += f"[{domino_p[0]}, {domino_p[1]}]"
        for domino_p in PieceSet.snake[-3:]:
            last_three += f"[{domino_p[0]}, {domino_p[1]}]"
        snake_str = f"{first_three}...{last_three}"
    else:
        for domino_p in PieceSet.snake:
            snake_str += f"[{domino_p[0]}, {domino_p[1]}]"

    print("======================================================================")
    print(f"Stock size: {len(PieceSet.stock_pieces)}")
    print(f"Computer pieces: {len(PieceSet.instances['computer'])}\n")
    print(f"{snake_str}\n")
    print("Your pieces:")
    for index in range(len(PieceSet.instances['player'])):
        print(f"{index + 1}:{PieceSet.instances['player'][index]}")
    if status == "computer":
        print(f"\nStatus: {status.capitalize()} is about to make a move. Press Enter to continue...")
    elif status == "player":
        print("\nStatus: It's your turn to make a move. Enter your command.")
    else:
        print(f"\nStatus: {status}")


# -------------------------- code execution --------------------------
main()