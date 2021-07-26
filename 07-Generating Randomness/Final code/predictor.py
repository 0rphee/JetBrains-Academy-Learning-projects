import random

triad_log = {'000': {'0': 0, '1': 0},
             '001': {'0': 0, '1': 0},
             '010': {'0': 0, '1': 0},
             '011': {'0': 0, '1': 0},
             '100': {'0': 0, '1': 0},
             '101': {'0': 0, '1': 0},
             '110': {'0': 0, '1': 0},
             '111': {'0': 0, '1': 0}}


# function to convert decimal numbers to binary
def dec_to_bin(n: int) -> str:
    binary = bin(n).replace("0b", "")
    missing_digits = 3 - len(binary)
    for digit in range(missing_digits):
        binary = '0' + binary
    return binary


# this class manages the strings given by the user
class UserString:
    complete_string = ""

    def __init__(self):
        if len(UserString.complete_string) == 0:
            print("Please give AI some data to learn...")
            print("The current data length is 0, 100 symbols left")
        self.raw_string = input("Print a random string containing 0 or 1:\n")
        self.processed_string = "".join([digit for digit in self.raw_string if digit == "0" or digit == "1"])
        UserString.complete_string += self.processed_string.strip()
        # The code below cuts the string down to 100 characters if bigger
        # if len(UserString.complete_string) > 100:
        #    UserString.complete_string = UserString.complete_string[0:100]


# this function decides to ask or not for more strings
def ask_or_stop():
    current_len = len(UserString.complete_string)
    if current_len < 100:
        UserString()
        current_len = len(UserString.complete_string)
        print(f"Current data length is {current_len}, {100 - current_len} symbols left\n")
        ask_or_stop()
    else:
        # in case there are more than 100 characters, the cycle finishes
        print(f"Final data string:\n{UserString.complete_string}\n")
        count_triads()
        print(
            '''You have $1000. Every time the system successfully predicts your next press, you lose $1.\nOtherwise, you earn $1. Print "enough" to leave the game. Let's go!''')
        prediction_phase(1000)
        # now the triad stats aren't going to be printed
        # print_triads()


# this function counts every triad, registering occurrences of 0 and 1 after each triad
def count_triads():
    for index in range(len(UserString.complete_string) - 3):
        curr_triad = UserString.complete_string[index] + UserString.complete_string[index + 1] + \
                     UserString.complete_string[index + 2]
        curr_next_n = UserString.complete_string[index + 3]
        triad_log[curr_triad][curr_next_n] += 1


# this function prints the triads and their occurrences by the decimal order according to them
def print_triads():
    for x in range(8):
        binary_equivalent = dec_to_bin(x)
        print(f"{binary_equivalent}: {triad_log[binary_equivalent]['0']},{triad_log[binary_equivalent]['1']}")


# this function generates a random triad to begin the string prediction
def triad_generator() -> str:
    return random.choice(list(triad_log.keys()))


def next_digit_pr(triad: str) -> str:
    num_of_zeroes = triad_log[triad]["0"]
    num_of_ones = triad_log[triad]["1"]
    if num_of_zeroes > num_of_ones:
        return "0"
    elif num_of_ones > num_of_zeroes:
        return "1"
    else:
        return random.choice(["0", "1"])


def corr_answers_printer(complete_predicted_string: str, complete_user_string: str):
    processed_computer_str = complete_predicted_string[3:]
    processed_user_str = complete_user_string[3:]
    correct_n = 0
    total_digits = len(processed_computer_str)
    for digit in range(total_digits):
        if processed_user_str[digit] == processed_computer_str[digit]:
            correct_n += 1
    correct_percentage = round((correct_n / total_digits * 100), 2)
    # the amount of money to add or subtract from the user is determined here
    money_change = (total_digits - correct_n) - correct_n
    print(f"\nComputer guessed right {correct_n} out of {total_digits} symbols ({correct_percentage}%)\n")
    return money_change


def prediction_phase(initial_money: int):
    amount_of_money = initial_money
    new_user_string = input("\nPrint a random string containing 0 or 1:\n")
    processed_string = "".join([digit for digit in new_user_string if digit == "0" or digit == "1"])
    if new_user_string == "enough":
        print("Game over!")
    elif len(processed_string) <= 3:
        prediction_phase(amount_of_money)
    else:
        predicted_string = triad_generator()
        for number in range(len(processed_string[3:])):
            triad_to_predict = new_user_string[number: 3 + number]
            predicted_string += next_digit_pr(triad_to_predict)
        print(f"\nPrediction:\n{predicted_string}")
        amount_of_money += corr_answers_printer(predicted_string, new_user_string)
        print((f"Your capital is now ${amount_of_money}"))
        prediction_phase(amount_of_money)


# ------------------------------ code execution ------------------------------
ask_or_stop()
