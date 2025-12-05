import flask
import creds
from sql import create_connection, execute_query, execute_read_query
from flask import jsonify
from flask import request

# Setting up the application
app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Show errors in browser

# Default home route
@app.route('/', methods=['GET'])
def home():
    return "<h1>WELCOME TO OUR RECIPE API!</h1>"

# Display all ingredients 
@app.route('/api/ingredient/all', methods=['GET'])
def get_all_ingredients():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    query = "SELECT * FROM ingredient"
    ingredients = execute_read_query(conn, query)
    return jsonify(ingredients)

# Obtains ingredient by ID
@app.route('/api/ingredient', methods=['GET'])
def get_ingredient_by_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    query = "SELECT * FROM ingredient WHERE id = %s" % id
    ingredients = execute_read_query(conn, query)
    return jsonify(ingredients)

# Add new ingredient
@app.route('/api/ingredient', methods=['POST'])
def add_ingredient():
    request_data = request.get_json()
    name = request_data['ingredientname']
    amount = request_data['totalamount']

    query = "INSERT INTO ingredient (ingredientname, totalamount) VALUES ('%s', '%s')" % (name, amount)

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    execute_query(conn, query)

    return "Ingredient added successfully"

# Delete ingredient by ID
@app.route('/api/ingredient', methods=['DELETE'])
def delete_ingredient():
    request_data = request.get_json()
    idToDelete = request_data['id']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    execute_query(conn, f"DELETE FROM recipeingredient WHERE ingredientid = {idToDelete}")

    execute_query(conn, f"DELETE FROM ingredient WHERE id = {idToDelete}")

    return jsonify({"message": "Ingredient deleted successfully"})


# Add recipe
@app.route('/api/recipe', methods=['POST'])
def add_recipe():
    data = request.get_json()
    name = data['name']
    instructions = data['instructions']

    query = f"INSERT INTO recipe (name, instructions) VALUES ('{name}', '{instructions}')"

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    execute_query(conn, query)

    return "Recipe added successfully"

# Display all recipes
@app.route('/api/recipe/all', methods=['GET'])
def get_all_recipes():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    query = "SELECT * FROM recipe"
    recipes = execute_read_query(conn, query)
    return jsonify(recipes) 

# View recipe with ingredients 
@app.route('/api/recipe', methods=['GET'])
def get_recipe_with_ingredients():
    if 'id' in request.args:
        recipe_id = int(request.args['id'])
    else:
        return "Error: No recipe ID provided"

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    query = f"""
        SELECT recipe.name, recipe.instructions, ingredient.ingredientname, recipeingredient.amount
        FROM recipe
        JOIN recipeingredient ON recipe.id = recipeingredient.recipeid
        JOIN ingredient ON recipeingredient.ingredientid = ingredient.id
        WHERE recipe.id = {recipe_id}
    """

    result = execute_read_query(conn, query)
    return jsonify(result)

# add ingredients for a recipe
@app.route('/api/recipeingredient', methods=['POST'])
def add_recipe_ingredient():
    data = request.get_json()
    recipeid = data['recipeid']
    ingredientid = data['ingredientid']
    amount = data['amount']

    query = f"INSERT INTO recipeingredient (recipeid, ingredientid, amount) VALUES ({recipeid}, {ingredientid}, {amount})"

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    execute_query(conn, query)

    return "Ingredient added to recipe"
                                         
# Cook recipe
# Cook recipe
@app.route('/api/recipe/cook', methods=['POST'])
def cook_recipe():
    data = request.get_json()
    recipe_id = data.get('recipeid')

    myCreds = creds.Creds()
    connection = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    cursor = connection.cursor(dictionary=True)

    # Fetch ingredients for the recipe
    cursor.execute("SELECT ingredientid, amount FROM recipeingredient WHERE recipeid = %s", (recipe_id,))
    ingredients = cursor.fetchall()

    # Check inventory for each ingredient
    for item in ingredients:
        cursor.execute("SELECT totalamount FROM ingredient WHERE id = %s", (item['ingredientid'],))
        inventory = cursor.fetchone()

        if inventory is None:
            return jsonify({"error": f"Ingredient ID {item['ingredientid']} not found"}), 404

        required = int(item['amount'])
        available = int(inventory['totalamount'])

        if available < required:
            return jsonify({"error": f"Not enough inventory for ingredient ID {item['ingredientid']}"}), 400

    # Subtract used amount from inventory or set to 0 if depleted
    for item in ingredients:
        cursor.execute("SELECT totalamount FROM ingredient WHERE id = %s", (item['ingredientid'],))
        inventory = cursor.fetchone()
        if inventory is None:
            continue

        remaining = int(inventory['totalamount']) - int(item['amount'])

        if remaining <= 0:
            # Instead of deleting, set amount to 0
            cursor.execute("UPDATE ingredient SET totalamount = 0 WHERE id = %s", (item['ingredientid'],))
        else:
            cursor.execute("UPDATE ingredient SET totalamount = %s WHERE id = %s", (remaining, item['ingredientid']))

    connection.commit()
    return jsonify({"message": "Recipe cooked successfully"}), 200



app.run()