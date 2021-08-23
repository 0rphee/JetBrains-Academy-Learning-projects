import random

OPERANDS = set("*+-")


def rand_easy_operation():
    n1, n2 = random.randint(2, 9), random.randint(2, 9)
    operation_symbol = random.choice(tuple(OPERANDS))
    function_handler = OPERATIONS[operation_symbol]

    op_string = " ".join((str(n1), operation_symbol, str(n2)))
    result = function_handler(n1, n2)
    return op_string, result


def rand_dif_operation():
    root = random.randint(11, 29)
    result = root ** 2
    return root, result


def basic_func_gen(operation: str):
    if operation == "addi":
        return lambda a, b: a + b
    elif operation == "sub":
        return lambda a, b: a - b
    elif operation == "multi":
        return lambda a, b: a * b

OPERATIONS = {"*": basic_func_gen("multi"), "+": basic_func_gen("addi"), "-": basic_func_gen("sub")}


def check_input(result: int) -> bool:
    while True:
        try:
            user_input = int(input())
            if user_input == result:
                print("Right!")
                return True
            else:
                print("Wrong!")
                return False
        except ValueError:
            print("Incorrect format.")


def easy_task() -> bool:
    op_string, result = rand_easy_operation()
    print(op_string)
    is_right = check_input(result)
    return is_right


# todo maybe merge this two functions ↑


def dif_task() -> bool:  # todo insert into main function
    op_string, result = rand_dif_operation()
    print(op_string)
    is_right = check_input(result)
    return is_right


def level_select() -> (dict, bool, str):
    print("""
Which level do you want? Enter a number:
1 - simple operations with numbers 2-9
2 - integral squares of 11-29
    """)
    while True:
        try:
            user_input = int(input())
            if user_input == 1:
                return run_tests(easy_task)
            elif user_input == 2:
                return run_tests(dif_task)
            else:
                print("Incorrect format.\n")
        except ValueError:
            print("Incorrect format.\n")


EASY_DESC = "level 1 (simple operations with numbers 2-9"
DIF_DESC = "level 2 (integral squares of 11-29"


def run_tests(task) -> (dict, bool, str):
    description = EASY_DESC if task == easy_task else DIF_DESC
    results = {i: task() for i in range(5)}
    n_of_correct = list(results.values()).count(True)
    save_result = input(f"Your mark is {n_of_correct}/5. Would you like to save the result? Enter yes or no.\n").lower()
    save_result = True if save_result == "yes" or save_result == "y" else False
    return n_of_correct, save_result, description


def main():
    results, save_result, description = level_select()
    if save_result:
        name = input("What is your name:\n")
        FILENAME = "results.txt"
        with open(FILENAME, "a") as file:
            file.write(f"{name}: {results}/5 in {description}\n")
        print(f'The results are saved in "{FILENAME}"')


# ---------------------------- code execution ----------------------------
main()
