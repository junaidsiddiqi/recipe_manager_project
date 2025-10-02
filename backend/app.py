import flask
import creds
from sql import create_connection, execute_query, execute_read_query
from flask import jsonify, request

# Setting up the application
app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Show errors in browser

# Default home route
@app.route('/', methods=['GET'])
def home():
    return "<h1>WELCOME TO OUR RECIPE API!</h1>"