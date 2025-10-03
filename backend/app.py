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

app.run()