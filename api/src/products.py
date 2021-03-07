import simplejson as json
from src.utils import Utils
from flask import request, make_response, jsonify
from flask_classful import FlaskView
from src.db import Connection
from psycopg2.extras import NamedTupleCursor


class Products(FlaskView):

    def index(self):
        # list all
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        try:
            cursor.execute(
                "SELECT * FROM tb_products ORDER BY id;")
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": "Internal Server Error"
            }, 500)

        products = cursor.fetchall()
        data = []

        for product in products:
            data.append({
                "id": product.id,
                "title": product.product_name,
                "price": product.unit_price,
            })
        cursor.close()
        connection.con.close()
        return jsonify(data)

    def post(self):
        # add new
        new_product_data = request.json
        error, error_msg = product_data_validation(new_product_data)
        if not error:
            new_product_data = product_data_sanitization(new_product_data)
            new_product_data = {
                "id": None,
                "product_name": new_product_data["product_name"],
                "unit_price": new_product_data["unit_price"], }
            connection = Connection()
            cursor = connection.con.cursor()
            sql_string = "INSERT INTO tb_products(product_name, unit_price) VALUES (%s,%s) RETURNING id;"

            try:
                cursor.execute(
                    sql_string, (new_product_data["product_name"], new_product_data["unit_price"]))
            except Exception as err:
                connection.con.rollback()
                connection.print_psycopg2_exception(err)

                return ({
                    "code": 400,
                    "description": str(err)
                }, 400)

            connection.con.commit()
            new_product_data["id"] = cursor.fetchone()[0]
            cursor.close()
            connection.con.close()
            return new_product_data, 201
        return error_msg, 400

    def get(self, id):
        # get specific
        try:
            id = int(id)
        except ValueError as error:
            return json.dumps(error)

        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        sql_string = "SELECT * FROM tb_products WHERE id=%s;"
        try:
            cursor.execute(sql_string, (id,))
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": "Internal Server Error"
            }, 500)

        product = cursor.fetchone()

        cursor.close()
        connection.con.close()

        return jsonify(product) if product else {}


def product_data_sanitization(data):
    data["product_name"] = data["product_name"].strip()
    if type(data["unit_price"]) == str:
        data["unit_price"] = float(data["unit_price"].strip())
    return data


def product_data_validation(data):
    error = False
    error_msg = []

    # product_name
    if "product_name" not in data or (type(data["product_name"]) == str and not data["product_name"].strip()):
        error = True
        error_msg.append("The title of the book must not be empty.")
    elif(type(data["product_name"]) != str):
        error = True
        error_msg.append("The title of the book must be a string.")

    # unit_price
    n_error, n_error_msg = Utils.validation_field_float_greater_zero(
        "unit_price", data)
    error |= n_error
    error_msg += n_error_msg["error"]

    return error, {"error": error_msg}
