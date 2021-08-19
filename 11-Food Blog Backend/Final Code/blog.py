import argparse
import sqlite3

# argument config
parser = argparse.ArgumentParser()
parser.add_argument("db_name")
parser.add_argument("--ingredients")  # gets a list separated by commas
parser.add_argument("--meals")  # gets a list separated by commas

# var assigning for arguments
args = parser.parse_args()
db_name = args.db_name
if args.ingredients:
    entered_ingredients = [ing.strip() for ing in args.ingredients.split(",")]
    entered_meals = args.meals.split(",")
else:
    entered_ingredients, entered_meals = None, None

conn = sqlite3.connect(db_name)
cur = conn.cursor()

# creation of the tables
cur.execute('PRAGMA foreign_keys = ON;')
cur.execute('CREATE TABLE IF NOT EXISTS meals (meal_id INTEGER PRIMARY KEY, meal_name TEXT NOT NULL UNIQUE)')
cur.execute(
    'CREATE TABLE IF NOT EXISTS ingredients (ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT NOT NULL UNIQUE)')
# noinspection DuplicatedCode
cur.execute('CREATE TABLE IF NOT EXISTS measures (measure_id INTEGER PRIMARY KEY, measure_name TEXT UNIQUE)')
cur.execute(
    'CREATE TABLE IF NOT EXISTS recipes (recipe_id INTEGER PRIMARY KEY, recipe_name TEXT NOT NULL, recipe_description TEXT)')
cur.execute(
    '''CREATE TABLE IF NOT EXISTS serve (serve_id INTEGER PRIMARY KEY, recipe_id INTEGER NOT NULL, meal_id INTEGER NOT NULL, FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id), FOREIGN KEY(meal_id) REFERENCES meals(meal_id));''')
cur.execute(
    'CREATE TABLE IF NOT EXISTS quantity (quantity_id INTEGER PRIMARY KEY, quantity INTEGER NOT NULL, recipe_id INTEGER NOT NULL, measure_id INTEGER NOT NULL, ingredient_id INTEGER NOT NULL, FOREIGN KEY (measure_id) REFERENCES measures (measure_id), FOREIGN KEY (ingredient_id) REFERENCES ingredients (ingredient_id), FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id))')
conn.commit()

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


# db db setup >>>>>>>>>>>>>>>>>>>
def insert_data_to(table_name):
    for i in data[table_name]:
        cur.execute(f'''INSERT INTO {table_name} ({table_name[:-1] + "_name"}) VALUES ("{i}")''')
    conn.commit()


# inserts ingredients to db
def insert_ingredients(quantity: tuple, recipe_id: int, ingredient_id: int, measure_id=None):
    if measure_id:
        cur.execute(
            f"INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id) VALUES ({quantity}, {recipe_id}, {measure_id}, {ingredient_id})")
    else:
        cur.execute(
            f'INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id) VALUES ({quantity}, {recipe_id}, 8, {ingredient_id})')  # 8 is the id of the empty column
    conn.commit()


def set_recipe_serve_times(recipe_id):
    av_meals = cur.execute('SELECT meal_name FROM meals')
    av_meals = av_meals.fetchall()
    print(get_meal_opts_string(av_meals))
    serve_times = input('Enter proposed meals separated by a space: ').split()
    for time in serve_times:
        insert_serve(recipe_id, time)


def insert_serve(recipe_id, meal_id):
    cur.execute(f'''INSERT INTO serve (recipe_id, meal_id) VALUES ({recipe_id}, {meal_id})''')
    conn.commit()


def get_meal_opts_string(av_meals):
    av_meals = list(enumerate(av_meals, 1))
    string = ''
    for num, meal_name in av_meals:
        string += f'{num}) {meal_name[0]} '
    return string


# db setup >>>>>>>>>>>>>>>>>>>


def get_input_ids(rep_ml_ing: str, entered_list: list = None):
    cur.execute(f"SELECT {rep_ml_ing}_id, {rep_ml_ing}_name FROM {rep_ml_ing}s")
    set_of_dicts = dict(cur.fetchall())
    # print(set_of_dicts)
    if entered_list:
        return_list = [key for i in entered_list for key in set_of_dicts if set_of_dicts[key] == i]
        if len(entered_list) != len(return_list) and rep_ml_ing == "ingredient":
            return_list.append("missing_ing")
            return return_list
    else:
        return_list = set_of_dicts.keys()
    return set(return_list)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def get_ingredients_of(recipe_id_list: set, our_ingredients: list):
    recipe_id_list = set([x[0] for x in recipe_id_list])
    our_ingredients = set(int(x) for x in our_ingredients)

    corroborated_recipes = set()
    for recipe_id in recipe_id_list:
        cur.execute(f'SELECT ingredient_id FROM quantity WHERE recipe_id = {recipe_id}')
        y = cur.fetchall()  # list of ingredient_ids that have current recipe_id
        y = set([i[0] for i in y])  # formatting ((1,), (2,), etc)
        intersection = our_ingredients.intersection(y)
        if intersection == our_ingredients:
            corroborated_recipes.add(recipe_id)
    return corroborated_recipes


def get_meals_of(recipe_id_list: set, our_meals: list):
    recipe_id_list = set([x[0] for x in recipe_id_list])
    our_meals = set(int(x) for x in our_meals)
    corroborated_meals = set()
    for recipe_id in recipe_id_list:
        cur.execute(f'SELECT meal_id FROM serve WHERE recipe_id = {recipe_id}')
        y = cur.fetchall()  # list of ingredient_ids that have current recipe_id
        y = set([i[0] for i in y])  # formatting ((1,), (2,), etc)
        intersection = our_meals.intersection(y)
        for element in intersection:
            if element in our_meals:
                corroborated_meals.add(recipe_id)
    return corroborated_meals


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def get_recipes(ingredients: list, meals: list) -> set:
    meal_ids = get_input_ids("meal", meals)
    ingredient_ids = get_input_ids("ingredient",
                                   ingredients)  # "missing_ing will be added to list/set if an ingredient isn't found in the db"

    # because theres there isn't an ingredient in the db, the search will be cut short
    if "missing_ing" in ingredient_ids:
        return set()

    # format meals and ingredients
    meal_ids = ", ".join((str(id) for id in meal_ids)).replace("{", "").replace("}", "")
    ingredient_ids = ", ".join((str(id) for id in ingredient_ids)).replace("{", "").replace("}", "")

    #  -------------------- VALIDATION --------------------
    # select recipe_ids from the quantity table
    cur.execute(f"SELECT recipe_id FROM quantity WHERE ingredient_id IN ({ingredient_ids})")
    recipe_ids_with_ingredients = set(cur.fetchall())
    recipe_ids_with_ingredients = get_ingredients_of(recipe_ids_with_ingredients, ingredient_ids.split(", "))

    # select recipe_ids from the serve table
    cur.execute(f"SELECT recipe_id FROM serve WHERE meal_id IN ({meal_ids})")
    recipe_ids_with_meals = set(cur.fetchall())
    recipe_ids_with_meals = get_meals_of(recipe_ids_with_meals, meal_ids.split(", "))
    # -------------------- VALIDATION --------------------

    valid_recipe_ids = recipe_ids_with_ingredients.intersection(recipe_ids_with_meals)
    return valid_recipe_ids


def insert_recipe():
    name = input('Recipe name: ')
    if name == '':
        return 'break'
    description = input('Recipe description: ')
    cur.execute(f'''INSERT INTO recipes (recipe_name, recipe_description) VALUES ("{name}", "{description}")''')
    conn.commit()
    recipe_id = cur.execute(f'''SELECT recipe_id FROM recipes''').lastrowid
    set_recipe_serve_times(recipe_id)  # inserts the serve times into the db
    set_ingredients(recipe_id)  # asks for input for the quantity table and inserts if correct


def set_ingredients(
        recipe_id: int):  # asks for ingredients to insert to the quantity table and inserts them if they are correct
    ing_elements = input('Input quantity of ingredient <press enter to stop>: ').split()
    if len(ing_elements) == 3:
        quantity, measure, ingredient = ing_elements
        measure = search_measure(measure)
        ingredient = search_ingredients(ingredient)
        if ingredient == "inconclusive" or measure == "inconclusive":
            val = "measure" if measure == "inconclusive" else "ingredient"
            print(f"The {val} is not conclusive!")
            set_ingredients(recipe_id)
        else:
            insert_ingredients(quantity, recipe_id, ingredient, measure_id=measure)
            set_ingredients(recipe_id)

    elif len(ing_elements) == 2:
        quantity, ingredient = ing_elements
        ingredient = search_ingredients(ingredient)
        if ingredient == "inconclusive":
            print("The ingredient is not conclusive!")
            set_ingredients(recipe_id)
        else:
            insert_ingredients(quantity, recipe_id, ingredient)
            set_ingredients(recipe_id)

    elif len(ing_elements) == 0:
        return
    else:
        print("Inconclusive - (not accounted for in examples)")
        set_ingredients(recipe_id)


# the input is evaluated to search fo it in the ingredients list
def search_ingredients(ingredient_name) -> int or list:
    cur.execute(f"SELECT ingredient_id, ingredient_name FROM ingredients")
    available_ingredients = cur.fetchall()
    finds = {}  # registers how many times the inputted ingredient name was found in the ingredient list
    for ing_id, ingredient in available_ingredients:
        if ingredient_name in ingredient:
            finds[ing_id] = ingredient
    if len(finds) == 0:
        return "inconclusive"
    elif len(finds) == 1:
        return list(finds.keys())[0]  # gets the id of the measure
    elif len(finds) >= 2:
        return "inconclusive"


# the start of the measure is searched to be matched
def search_measure(measure_name) -> int or list:
    cur.execute("SELECT measure_id, measure_name from measures")
    available_measures = cur.fetchall()
    finds = {}
    for measure_id, measure in available_measures:
        if measure.startswith(measure_name):
            finds[measure_id] = measure
    if len(finds) == 0:
        return "inconclusive"
    elif len(finds) == 1:
        return list(finds.keys())[0]  # gets the id of the measure
    elif len(finds) >= 2:
        return "inconclusive"


def get_recipe_names(recipe_ids):
    cur.execute(f"SELECT recipe_id, recipe_name FROM recipes")
    all_recipes = set(cur.fetchall())
    names_to_return = []
    for id, name in all_recipes:
        for valid_id in recipe_ids:
            if id == valid_id:
                names_to_return.append(name)
    return list(names_to_return)


def main():
    if entered_ingredients and entered_meals:
        valid_recipe_ids = get_recipes(entered_ingredients, entered_meals)
        recipe_names = get_recipe_names(valid_recipe_ids)
        if len(recipe_names) == 0:
            print("There are no such recipes in the database.")
        else:
            recipe_names = ", ".join(recipe_names)
            print(f"Recipes selected for you: {recipe_names}")
    else:
        for table in data:
            insert_data_to(table)
        while True:
            if insert_recipe() == 'break':
                conn.close()
                break


# ----------------------------------- execution -----------------------------------
main()
