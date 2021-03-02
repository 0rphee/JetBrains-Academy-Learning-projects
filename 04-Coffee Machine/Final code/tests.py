money = 550
water = 400
milk = 540
beans = 120
cups = 9

items = {"money": money,
         "water": water,
         "milk": milk,
         "beans": beans,
         "cups": cups}

espresso = {"water": 250,
            "beans": 16,
            "money": 4,
            "cups": 1}
latte = {"water": 350,
         "milk": 75,
         "beans": 20,
         "money": 7,
         "cups": 1}
cappuccino = {"water": 200,
              "milk": 100,
              "beans": 12,
              "money": 6,
              "cups": 1}


def check_rcrs(dicti):
    moneys = dicti.pop("money")
    for itemy in dicti:
        if dicti[itemy] <= 0:
            dicti.update({"money": moneys})
            return "Not Enough", f"Sorry, not enough {itemy}!\n"
    dicti.update({"money": moneys})
    return "Enough", "I have enough resources, making you a coffe!\n"


def buy_coffee(typea: dict, itemss: dict, espressol: bool = False) -> dict:
    temp_items = itemss.copy()
    if espressol:
        temp_items["water"] -= typea["water"]
        temp_items["beans"] -= typea["beans"]
        temp_items["money"] += typea["money"]
        temp_items["cups"] -= typea["cups"]
    else:
        temp_items["water"] -= typea["water"]
        temp_items["milk"] -= typea["milk"]
        temp_items["beans"] -= typea["beans"]
        temp_items["money"] += typea["money"]
        temp_items["cups"] -= typea["cups"]
    check = check_rcrs(temp_items)
    if check[0] == "Enough":
        print(check[1])
        return temp_items
    elif check[0] == "Not Enough":
        print(check[1])
        return itemss


def coffee_machine(items_in: dict) -> dict:
    def print_it():
        print(f"""The coffee machine has:
{items_in["water"]} of water
{items_in["milk"]} of milk 
{items_in["beans"]} of coffee beans
{items_in["cups"]} of disposable cups
${items_in["money"]} of money\n""")

    what_to_do = input("Write action (buy, fill, take, remaining, exit):\n")
    # BUYS
    if what_to_do == "buy":
        what_to_buy = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n")
        if what_to_buy == "back":
            pass
        else:
            what_to_buy = int(what_to_buy)
            if what_to_buy == 1:
                items_in = buy_coffee(espresso, items_in, True)
            elif what_to_buy == 2:
                items_in = buy_coffee(latte, items_in)
            else:
                items_in = buy_coffee(cappuccino, items_in)
            return items_in
    # FILLS
    elif what_to_do == "fill":
        add_watter = int(input("Write how many ml of water do you want to add:\n"))
        add_milk = int(input("Write how many ml of milk do you want to add:\n"))
        add_beans = int(input("Write how many grams of coffee beans do you want to add:\n"))
        add_cups = int(input("Write how many disposable cups of coffe do you want to add:\n"))
        items_in["water"] += add_watter
        items_in["milk"] += add_milk
        items_in["beans"] += add_beans
        items_in["cups"] += add_cups
        return items_in
    # TAKES
    elif what_to_do == "take":
        print(f'I gave you ${items_in["money"]}')
        items_in["money"] = 0
        return items_in
    # SHOWS REMAINING
    elif what_to_do == "remaining":
        print_it()
        return items_in
    # EXITS
    elif what_to_do == "exit":
        return what_to_do


cycle = coffee_machine(items)
while type(cycle) != str:
    cycle = coffee_machine(cycle)
