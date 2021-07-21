import random

num_people = int(input("Enter the number of friends joining (including you):\n"))
dict_full = {}

if num_people <= 0:
    print("No one is joining for the party")
else:
    print("Enter the name of every friend (including you), each on a new line:")
    for i in range(0, num_people):
        current_name = input()
        dict_full[current_name] = 0
    total_bill = int(input("Enter the total bill value:\n"))

    whos_lucky = input('Do you want to use the "Who is lucky" feature? Write Yes/No:\n')

    if whos_lucky == "Yes":
        lucky_one = random.choice(list(dict_full.keys()))
        print(f"{lucky_one} is the lucky one!")
        divided_bill = round((total_bill/(len(dict_full)-1)), 2)
        for name in dict_full:
            dict_full[name] = divided_bill
        dict_full[lucky_one] = 0
    else:
        print("No one is going to be lucky")
        divided_bill = round((total_bill / len(dict_full)), 2)
        for name in dict_full:
            dict_full[name] = divided_bill
    print(dict_full)