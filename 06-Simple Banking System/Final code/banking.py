import random
import sqlite3

# sql initialization
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS card(
id INTEGER,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0)''')
conn.commit()

# texts from option menus
menu_txt1 = """\n1. Create an account\n2. Log into account\n0. Exit\n"""
menu_txt2 = """\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n"""


# function to calculate with the luhn algorithm the last digit of the card
def luhn(number):
    counter = 1
    step1 = ''
    for digit in number:
        if counter % 2 != 0:
            curr_d = int(digit) * 2
            if curr_d > 9:
                curr_d -= 9
            step1 += str(curr_d)
            counter += 1
        else:
            step1 += digit
            counter += 1
    step2 = 0
    for digit in step1:
        step2 += int(digit)
    for n in range(0, 10):
        if (n + step2) % 10 == 0:
            return str(n)


# function to check luhn algorithm
def l_checker(complete_n):
    according_last_digit = luhn(complete_n[0:-1])
    real_last_digit = complete_n[-1]
    return according_last_digit == real_last_digit


# class managing creation of cards
class Card:
    all_cards = {}
    all_balances = {}

    def __init__(self):
        # generates unique id
        self.id = self.rand_digits(4)
        cur.execute('''SELECT id FROM card''')
        rows = cur.fetchall()
        for row in rows:
            if self.id in row:
                while self.id in row:
                    self.id = self.rand_digits(4)

        # generates unique credit car number
        self.fifteen = "400000" + self.rand_digits(9)
        self.number = (self.fifteen + luhn(self.fifteen))
        cur.execute('''SELECT number FROM card''')
        rows = cur.fetchall()
        # checks for doubled card numbers in tuple
        for row in rows:
            if self.number in row:
                while self.number in row:
                    self.fifteen = "400000" + self.rand_digits(9)
                    self.number = (self.fifteen + luhn(self.fifteen))

        # generates the PIN of the card
        self.pin = str(self.rand_digits(4))
        # here the new card is inserted into the db
        cur.execute(f'INSERT INTO card (id, number, pin, balance) VALUES ({self.id}, {self.number}, "{str(self.pin)}", 0)')
        conn.commit()
        print(f"""\nYour card has been created\nYour card number:\n{self.number}\nYour card PIN:\n{self.pin}""")

    def rand_digits(self, n_digits):
        digits = str()
        for _ in range(n_digits):
            digits = str(digits) + str(random.randint(0, 9))
        return digits


# class managing interior and exterior menus
class Supermenu:
    def __init__(self):
        self.ext_menu_state = None
        self.int_menu_state = None

    def main(self):
        self.ext()

    def ext(self):
        self.ext_menu_state = input(menu_txt1)
        if self.ext_menu_state == "1":
            Card()
            self.ext()
        elif self.ext_menu_state == "2":
            log_num = input("Enter your card number:\n")
            log_PIN = input("Enter your PIN:\n")
            # check in db for card and pin
            cur.execute('''SELECT number, pin, balance FROM card''')
            rows = cur.fetchall()
            print(rows)

            # checks every tuple for the number and pin given in the input
            for row in rows:
                if log_num in row:
                    if log_PIN in row:
                        print("You have successfully logged in!")
                        self.intir((row[0], row[2]))
                        break
            else:
                # if the number or pin are invalid the exterior menu runs again
                if self.ext_menu_state != "0":
                    print("Wrong card number or PIN!")
                    self.ext()
        # exit
        elif self.ext_menu_state == "0":
            print('Bye!')
        # runs again in case of invalid input
        else:
            self.ext()

    # interior menu method
    def intir(self, number_balance):
        self.int_menu_state = input(menu_txt2)
        # shows balance
        if self.int_menu_state == "1":
            print(f"Balance: {number_balance[1]}")
            self.intir(number_balance)
        # adds income to balance
        elif self.int_menu_state == "2":
            income = int(input("\nEnter income:\n"))
            cur.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {number_balance[0]}')
            conn.commit()
            print("Income was added!")

            # the balances are updated for the method
            cur.execute(f'SELECT balance FROM card WHERE number = {number_balance[0]}')
            number_balance_updated = cur.fetchall()[0][0]

            self.intir((number_balance[0], number_balance_updated))
        # transfer between cards
        elif self.int_menu_state == "3":
            card_to_transfer = input("\nTransfer\nEnter card number:\n")
            # checks if it isn't the same card number
            if card_to_transfer == number_balance[0]:
                print("You can't transfer money to the same account!")
                self.intir(number_balance)
            else:
                # the last number is checked with luhn algorithm
                if l_checker(card_to_transfer):
                    cur.execute('''SELECT number, balance FROM card''')
                    rows = cur.fetchall()
                    # checks every tuple for the card number to transfer
                    for row in rows:
                        if card_to_transfer in row:
                            amount_to_transfer = int(input("Enter how much money you want to transfer:\n"))
                            if amount_to_transfer > number_balance[1]:
                                # not enough money, goes back to interior menu
                                print("Not enough money!\n")
                                self.intir(number_balance)
                                break
                            else:  # there's enough money to transfer
                                # retire money from sender
                                cur.execute(
                                    f'UPDATE card SET balance = balance - {amount_to_transfer} WHERE number = {number_balance[0]}')
                                conn.commit()
                                # add money to the other card
                                cur.execute(
                                    f'UPDATE card SET balance = balance + {amount_to_transfer} WHERE number = {card_to_transfer}')
                                conn.commit()
                                print("Success!")

                                # the balances are updated for the method
                                cur.execute(f'SELECT balance FROM card WHERE number = {number_balance[0]}')
                                number_balance_updated = cur.fetchall()[0][0]

                                self.intir((number_balance[0], number_balance_updated))
                                break
                    else:
                        # this runs if the card to transfer isn't found in the db
                        print("Such a card does not exist.")
                        self.intir(number_balance)

                else:
                    # if luhn's algorithm doesn't checks out, interior menu runs
                    print("Probably you made a mistake in the card number. Please try again")
                    self.intir(number_balance)
        # Close account
        elif self.int_menu_state == "4":
            cur.execute(f'DELETE FROM card WHERE number = {number_balance[0]}')
            conn.commit()
            print("The account has been closed!")
            self.ext()
        # logs out, exterior menu runs
        elif self.int_menu_state == "5":
            print("You have successfully logged out!")
            self.ext()
        # both exterior and interior menus stop
        elif self.int_menu_state == "0":
            print("Bye!")
            self.ext_menu_state = "0"
        # runs again in case of invalid input
        else:
            self.intir(number_balance)


menu = Supermenu()
menu.main()
