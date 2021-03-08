from src.utils import Utils
from flask import request, jsonify
from flask_classful import FlaskView
from src.db import Connection
from psycopg2.extras import NamedTupleCursor


class Orders(FlaskView):

    def index(self):
        # list all
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        try:
            cursor.execute(
                "SELECT * FROM tb_orders ORDER BY id;")
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": str(err)
            }, 500)

        orders = cursor.fetchall()
        data = []

        for order in orders:
            data.append({
                "id": order.id,
                "id_costumer": order.id_costumer,
                "discount": order.discount,
                "order_date": order.order_date,
            })
        cursor.close()
        connection.con.close()
        return jsonify(data)

    def __delete_order(self, id_order):
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        try:
            cursor.execute("DELETE FROM tb_orders WHERE id=%s;", (id_order,))
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": "Internal Server Error"
            }, 500)
        connection.con.commit()
        cursor.close()
        connection.con.close()

    def __get_product_prices(self, id_product_list):
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        sql_string = "SELECT id, unit_price FROM tb_products WHERE id in %(id_product_list)s;"
        try:
            cursor.execute(
                sql_string, {
                    "id_product_list": tuple(id_product_list)
                })
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": "Internal Server Error"
            }, 500)

        products = cursor.fetchall()
        data = {}

        for product in products:
            data[product.id] = product.unit_price

        cursor.close()
        connection.con.close()
        return data

    def __insert_order_products(self, new_sale_data):
        # get prices
        dict_unit_price = self.__get_product_prices(
            [product["id_product"] for product in new_sale_data["products"]])

        # add new
        connection = Connection()
        cursor = connection.con.cursor()
        sql_string = "INSERT INTO tb_order_details(id_order, id_product, unit_price, quantity) VALUES (%s, %s, %s, %s);"

        for product in new_sale_data["products"]:
            try:
                cursor.execute(sql_string, (new_sale_data["id"], product["id_product"],
                                            dict_unit_price[product["id_product"]], product["quantity"]))

            except Exception as error:
                connection.con.rollback()
                connection.print_psycopg2_exception(error)

                cursor.close()
                connection.con.close()

                self.__delete_order(new_sale_data["id"])

                return ({
                    "code": 400,
                    "description": str(error)
                }, 400)

        connection.con.commit()

        cursor.close()
        connection.con.close()

        return new_sale_data, 201

    def post(self):
        # add new
        new_sale_data = request.json
        error, error_msg = sale_data_validation(new_sale_data)
        if not error:
            new_sale_data = sale_data_sanitization(new_sale_data)
            new_sale_data = {
                "id": None,
                "id_costumer": new_sale_data["id_costumer"],
                "products": new_sale_data["products"], }
            connection = Connection()
            cursor = connection.con.cursor()
            sql_string = "INSERT INTO tb_orders(id_costumer) VALUES (%s) RETURNING id;"

            try:
                cursor.execute(sql_string, (new_sale_data["id_costumer"],))
            except Exception as err:
                connection.con.rollback()
                connection.print_psycopg2_exception(err)

                return ({
                    "code": 400,
                    "description": "Bad request"
                }, 400)

            connection.con.commit()
            new_sale_data["id"] = cursor.fetchone()[0]

            # percentage discount
            try:
                cursor.execute("SELECT order_discount(%s);",
                               (new_sale_data["id_costumer"],))
            except Exception as err:
                connection.con.rollback()
                connection.print_psycopg2_exception(err)
                return ({
                    "code": 500,
                    "description": str(err)
                }, 500)

            new_sale_data["discount_percentage"] = cursor.fetchone()[0]

            cursor.close()
            connection.con.close()

            # insert sale products
            return self.__insert_order_products(new_sale_data)
        return error_msg

    def get(self, id):
        # get specific
        try:
            id = int(id)
        except ValueError as error:
            return ({
                "code": 400,
                "description": str(error)
            }, 400)

        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        sql_string = "SELECT * FROM tb_orders WHERE id=%s;"
        try:
            cursor.execute(sql_string, (id,))
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": "Internal Server Error"
            }, 500)

        order = cursor.fetchone()

        cursor.close()
        connection.con.close()

        return jsonify(order) if order else {}


def sale_data_sanitization(data):
    data["id_costumer"] = int(data["id_costumer"])

    dict_products = {}

    for product in data["products"]:
        # id_product
        id_product = int(product["id_product"])
        # quantity
        quantity = int(product["quantity"])

        if id_product in dict_products:
            dict_products[id_product] += quantity
        else:
            dict_products[id_product] = quantity

    data["products"] = []

    for id_product in dict_products:
        data["products"].append({"id_product": id_product,
                                 "quantity": dict_products[id_product]})

    return data


def sale_data_validation(data):
    error = False
    error_msg = []

    # id_costumer
    n_error, n_error_msg = Utils.validation_field_int_greater_zero(
        "id_costumer", data)
    error |= n_error
    error_msg += n_error_msg["error"]

    # products
    if "products" not in data or (type(data["products"]) == str and not data["products"].strip()):
        error = True
        error_msg.append("products field must not be empty.")
    elif(type(data["products"]) != list):
        error = True
        error_msg.append("products field must be a array.")
    else:
        for product in data["products"]:
            # id_product
            n_error, n_error_msg = Utils.validation_field_int_greater_zero(
                "id_product", product)
            error |= n_error
            error_msg += n_error_msg["error"]

            # quantity
            n_error, n_error_msg = Utils.validation_field_int_greater_zero(
                "quantity", product)
            error |= n_error
            error_msg += n_error_msg["error"]

            if error:
                break

        # check constraint for 10 DIFFERENTS books per sale
        limit_per_sale = 10
        products_list = [product["id_product"] for product in data["products"]]
        if(len(products_list) > limit_per_sale):
            error = True
            error_msg.append(
                "The maximum number of products per sale is {}.".format(limit_per_sale))

    return error, {"error": error_msg}
