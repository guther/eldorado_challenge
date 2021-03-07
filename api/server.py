import json
from flask import Flask, make_response
from flask_cors import CORS
from src.utils import Utils
from src.orders import Orders
from src.products import Products
from src.costumers import Costumers


app = Flask(__name__)

CORS(app)

Utils.register(app, route_base='/utils/')
Orders.register(app, route_base='/sale/')
Products.register(app, route_base='/book/')
Costumers.register(app, route_base='/costumer/')


@app.route("/")
def hello():
    return "Hello, World!"


@app.errorhandler(404)
@app.errorhandler(405)
def not_found(error):
    # start with the correct headers and status code from the error
    response = error.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
