'''
water_cups = water // 200
milk_cups = milk // 50
bean_cups = beans // 15

cups_av = min(water_cups, milk_cups, bean_cups)

if cups <= cups_av:
    print("Yes, I can make that amount of coffee")
else:
    print(f"No, I can make only {cups_av} cups of coffee")
'''

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

print(f"""The coffee machine has:
{water} of water
{milk} of milk
{beans} of coffee beans
{cups} of disposable cups
{money} of money
""")

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


def buy_coffee(type: dict, itemss: list, espressol: bool = False) -> dict:
    if espressol == True:
        itemss["water"] -= type["water"]
        itemss["beans"] -= type["beans"]
        itemss["money"] += type["money"]
        itemss["cups"] -= type["cups"]
    else:
        itemss["water"] -= type["water"]
        itemss["milk"] -= type["milk"]
        itemss["beans"] -= type["beans"]
        itemss["money"] += type["money"]
        itemss["cups"] -= type["cups"]
    return itemss


def coffee_machine(items_in: dict) -> dict:
    what_to_do = input("Write action (buy, fill, take): ")

    if what_to_do == "buy":
        what_to_buy = int(input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: "))
        if what_to_buy == 1:
            items_in = buy_coffee(espresso, items_in, True)
        elif what_to_buy == 2:
            items_in = buy_coffee(latte, items_in)
        else:
            items_in = buy_coffee(cappuccino, items_in)
    elif what_to_do == "fill":
        add_watter = int(input("Write how many ml of water do you want to add: "))
        add_milk = int(input("Write how many ml of milk do you want to add: "))
        add_beans = int(input("Write how many grams of coffee beans do you want to add: "))
        add_cups = int(input("Write how many disposable cups of coffe do you want to add: "))
        items_in["water"] += add_watter
        items_in["milk"] += add_milk
        items_in["beans"] += add_beans
        items_in["cups"] += add_cups
    elif what_to_do == "take":
        print(f'I gave you ${items_in["money"]}')
        items_in["money"] = 0
    print(f"""The coffee machine has:
    {items_in["water"]} of water
    {items_in["milk"]} of milk
    {items_in["water"]} of coffee beans
    {items_in["cups"]} of disposable cups
    {items_in["money"]} of money
    """)
    return items_in


items = coffee_machine(items)
