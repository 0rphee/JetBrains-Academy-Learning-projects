AV_FORMATTERS = ['plain', 'bold', 'italic', 'header', 'link', 'inline-code', 'new-line',  'ordered-list', 'unordered-list']
RETURN_SYMBOL = {'plain': "", 'bold': "**", "italic": "*", 'inline-code': "`"}

COMMANDS = ["!help", "!done"]


def main():
    complete_text = ""
    while True:
        formatter = input("Choose formatter:")
        if formatter == '!help':
            help_c()
        elif formatter == '!done':
            done_c(complete_text)
            break
        else:
            if formatter in AV_FORMATTERS:
                complete_text = apply_formatting(formatter, complete_text)
                print(complete_text)
            else:
                print("Unknown formatting type or command")


def help_c():
    print("Available formatters: " + " ".join(AV_FORMATTERS))
    print("Special commands: " + " ".join(COMMANDS))


def done_c(complete_text: str):
    with open('output.md', 'w') as file:
        lines = complete_text.splitlines(True)
        file.writelines(lines)


def apply_formatting(formatter, complete_txt) -> str:
    if formatter == 'plain' or formatter == 'bold' or formatter == 'italic' or formatter == "inline-code":
        complete_txt += RETURN_SYMBOL[formatter] + input("Text: ") + RETURN_SYMBOL[formatter]
    elif formatter == 'header':
        level = int(input("Level: "))
        while level > 6:
            print("The level should be within the range of 1 to 6")
            level = int(input("Level: "))
        text = input("Text: ")
        complete_txt += ("#" * level) + " " + text + "\n"
    elif formatter == "new-line":
        complete_txt += "\n"
    elif formatter == "link":
        label = input("Label: ")
        url = input("URL: ")
        complete_txt += f"[{label}]({url})"
    elif formatter == 'ordered-list' or formatter == 'unordered-list':
        ordered = True if formatter == 'ordered-list' else False
        complete_txt = append_list(ordered, complete_txt)
    return complete_txt


def append_list(ordered: bool, complete_txt):
    n_rows = int(input('Number of rows: '))
    while n_rows <= 0:
        print('The number of rows should be greater than zero')
        n_rows = int(input('Number of rows:'))
    if ordered:
        for i in range(1, n_rows+1):
            curr_row = input(f'Row #{i}')
            complete_txt += f'{i}. {curr_row}\n'
    else:
        for i in range(1, n_rows+1):
            curr_row = input(f'Row #{i}')
            complete_txt += f'* {curr_row}\n'
    return complete_txt


# --------------------- code execution ---------------------
main()
