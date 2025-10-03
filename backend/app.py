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

    query = "DELETE FROM ingredient WHERE id = %s" % idToDelete

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    execute_query(conn, query)

    return "🗑️ Ingredient deleted successfully"



app.run()