from hstest.stage_test import *
from hstest.test_case import TestCase
import numpy as np


def remember_data(data, count_dict):
    for i in range(len(data) - COMBO_LENGTH):
        comb = data[i:i + COMBO_LENGTH]
        next_input = int(data[i + COMBO_LENGTH])
        count_dict[comb][next_input] += 1

    return count_dict


def make_prediction(data, count_dict):
    pred = str()
    for i in range(COMBO_LENGTH):
        res = str(np.random.choice([0, 1]))
        pred += res

    for i in range(len(data) - COMBO_LENGTH):
        comb = data[i:i + COMBO_LENGTH]
        try:
            if count_dict[comb][0] > count_dict[comb][1]:
                probas = [1, 0]
            elif count_dict[comb][0] < count_dict[comb][1]:
                probas = [0, 1]
            else:
                probas = [0.5, 0.5]

            

        except Exception:
            probas = [0.5, 0.5]

        res = str(np.random.choice([0, 1], p=probas))
        pred += res

    return pred


def estimate_prediction_accuracy(pred, data):
    pr = [bool(int(elem)) for elem in pred]
    gt = [bool(int(elem)) for elem in data]
    pred_correct = ~np.bitwise_xor(pr, gt)
    return sum(pred_correct.astype(int))


CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

COMBO_LENGTH = 3
MIN_DATA_STR_LEN = 100
INSTRUCTION = 'Print a random string containing 0 or 1'
GAME_END = 'Game over!'

keys = []
for i in range(2 ** COMBO_LENGTH):
    keys.append(str((bin(i)[2:].zfill(3))))

values = [[0, 0] for _ in range(2 ** COMBO_LENGTH)]
count_dict = dict(zip(keys, values))
inp = '1010101101010101010011100101001010100101010000101000101010000100101011010001001000101011101000101010010100101'
count_dict = remember_data(inp, count_dict)

appr_pred_set = set()
for i in range(1000):
    pred = make_prediction(inp, count_dict)
    appr_pred_set = appr_pred_set | set([pred[COMBO_LENGTH:]])

appr_pred_output_dict = {}
appr_pred_count_dict = {}
for appr_pred in appr_pred_set:
    correct_guesses = estimate_prediction_accuracy(appr_pred, inp[COMBO_LENGTH:])
    ideal_output = 'Computer guessed right {} out of {} symbols ({:03.2f} %)'.format(correct_guesses,
                                                                                        len(inp) - COMBO_LENGTH,
                                                                                        100 * correct_guesses / (len(
                                                                                            inp) - COMBO_LENGTH))
    appr_pred_output_dict[appr_pred] = ideal_output
    appr_pred_count_dict[appr_pred] = correct_guesses


class GenRandTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [TestCase(stdin=["1010101101010",
                                "1010100111001010010101001010100001010001",
                                '01010000100101011010001001000101011101000101010010100101',
                                inp,
                                'enough'],
                         attach=[109, appr_pred_output_dict, appr_pred_count_dict, inp, 1]),

                TestCase(stdin=["1010101101010_some_wrong_symbols",
                                "1010100111001010010101001010100001010001_some_more_wrong_symbols",
                                '01010000100101011010001001000101011101000101010010100101',
                                'some_irrelevant_symbols_in_the_game',
                                inp,
                                'enough'],
                         attach=[109, appr_pred_output_dict, appr_pred_count_dict, inp, 1]),

                TestCase(stdin=["1010101101010",
                                "1010100111001010010101001010100001010001",
                                '01010000100101011010001001000101011101000101010010100101',
                                inp,
                                inp,
                                'enough'],
                         attach=[109, appr_pred_output_dict, appr_pred_count_dict, inp, 2])
                ]

    def check(self, output: str, attach) -> CheckResult:
        correct_len, appr_pred_output_dict, appr_pred_count_dict, inp, game_iterations = attach
        strings = [s for s in output.split('\n') if s != '']

        if not strings:
            return CheckResult.wrong("The output seems to be empty.")
        
        if len(strings) < 3:
            return CheckResult.wrong("Your program is supposed to output at least 3 lines.\n"
                                     "However, there are less than 3 lines.")

        instructions = strings[2]
        data_string = inp

        if INSTRUCTION.lower() not in instructions.lower():
            return CheckResult.wrong('Please give instructions to user in the form "{}"\n'
                                     'The instruction should be given in the third line of the program.'.format(INSTRUCTION))

        if len(data_string) < MIN_DATA_STR_LEN:
            return CheckResult.wrong('Data string \"{}\" is too short, it should have length >={}'.format(data_string,
                                                                                                          MIN_DATA_STR_LEN))
        if len(data_string) != correct_len:
            return CheckResult.wrong(
                "The string \"{}\" of your output is supposed to contain the final data string. \n"
                "However, it contains wrong number of symbols".format(data_string)
            )

        game_finish = strings[-1]
        final_instruction = strings[-2]

        if 'game' not in game_finish.lower() or 'over' not in game_finish.lower():
            return CheckResult.wrong(
                "The final string \"{}\" of your output is supposed to contain game ending indicator in the form {}".format(
                    game_finish, GAME_END)
            )

        if INSTRUCTION.lower() not in final_instruction.lower():
            return CheckResult.wrong(
                "The pre-final string \"{}\" of your output is supposed to contain instructions in the form {}".format(
                    final_instruction, INSTRUCTION)
            )

        cap = 1000
        for iter in range(game_iterations):
            
            start_ind = -2 - game_iterations * 5
            prediction_declaration = strings[start_ind + iter * 5 + 1]
            prediction = strings[start_ind + iter * 5 + 2]
            result = strings[start_ind + iter * 5 + 3]
            capital_info = strings[start_ind + iter * 5 + 4]
            capital_info = capital_info.strip('.')
            capital_info = capital_info.strip(' ')
            
            if '(' not in result or ')' not in result:
                return CheckResult.wrong("The last line of your output is supposed "
                                         "to contain the percentage of correct guesses.\n"
                                         "This number should be put in parentheses.")
            percentage = result[result.index('(') + 1:result.index(')')].replace('%', '').replace(' ', '')
            if '.' in percentage:
                percentage = percentage[:percentage.index('.')]

            if 'prediction' not in prediction_declaration.lower():
                return CheckResult.wrong("Please use the word \"prediction\" in a line before the predictor output")

            if len(prediction) != correct_len:
                return CheckResult.wrong(
                    "The string \"{}\" of your output is supposed to contain the predictor output. \n"
                    "However, it contains wrong number of symbols".format(prediction)
                )

            pred_success = prediction[COMBO_LENGTH:] in appr_pred_output_dict.keys()
            if pred_success != True:
                return CheckResult.wrong(
                    "The string \"{}\" of your output is supposed to contain the predictor output. \n"
                    "However, it cannot be generated by prediction algorithm described".format(prediction)
                )

            if 'computer' not in result.lower() or 'guessed right' not in result.lower():
                return CheckResult.wrong(
                    "The string \"{}\" of your output is supposed to contain the prediction result. \n"
                    "However, it does not meet the requirements".format(result)
                )

            ideal_result = appr_pred_output_dict[prediction[COMBO_LENGTH:]]
            ideal_percentage = ideal_result[result.index('(') + 1:result.index(')')].replace('%', '').replace(' ', '')
            if '.' in ideal_percentage:
                ideal_percentage = ideal_percentage[:ideal_percentage.index('.')]
            if percentage != ideal_percentage:
                return CheckResult.wrong(
                    "The string \"{}\" of your output is supposed to contain the prediction result. \n"
                    "However, the prediction accuracy does not coincide with the expected one".format(result)
                )

            if 'capital' not in capital_info or '$' not in capital_info:
                return CheckResult.wrong(
                    "The string \"{}\" of your output is supposed to contain the information about user capital. \n"
                    "However, it does not meet the requirements".format(capital_info)
                )

            try:
                output_cap = int(capital_info[capital_info.index('$') + 1:])
                correct_guesses = appr_pred_count_dict[prediction[COMBO_LENGTH:]]
                cap += len(inp) - 2 * correct_guesses - COMBO_LENGTH

                if output_cap != cap:
                    return CheckResult.wrong(
                        "The string \"{}\" of your output is supposed to contain the information about user capital. \n"
                        "However, its value does not coincide with the expected one".format(capital_info)
                    )
            except ValueError:
                return CheckResult.wrong(
                    "The string \"{}\" of your output is supposed to contain the information about user capital. \n"
                    "However, the symbols after the $ sign cannot be turned into an integer value".format(capital_info)
                )
        return CheckResult.correct()


if __name__ == '__main__':
    GenRandTest('predictor.predictor').run_tests()
