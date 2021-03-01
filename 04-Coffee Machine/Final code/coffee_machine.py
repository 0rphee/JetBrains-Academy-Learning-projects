water = int(input("Write how many ml of water the coffee machine has: "))
milk = int(input("Write how many ml of milk the coffee machine has: "))
beans = int(input("Write how many grams of coffee beans the coffee machine has: "))
cups = int(input("Write how many cups of coffee you will need: "))

water_cups = water // 200
milk_cups = milk // 50
bean_cups = beans // 15

cups_av = min(water_cups, milk_cups, bean_cups)

if cups == cups_av:
    print("Yes, I can make that amount of coffee")
elif cups < cups_av:
    print(f"Yes, I can make that amount of coffee (and even {cups_av-cups} more than that")
else:
    print(f"No, I can make only {cups_av} cups of coffee")