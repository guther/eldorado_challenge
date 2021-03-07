import json
import uuid
from flask import request, make_response, jsonify
from flask_classful import FlaskView
from src.utils import Utils
from src.db import Connection
from psycopg2.extras import NamedTupleCursor


class Costumers(FlaskView):

    excluded_methods = ["get_costumer"]

    def index(self):

        field = request.args.get('field')
        valid_fields = ["cpf"]

        if field is not None:
            if field in valid_fields:
                value = request.args.get('val')
                if field == "cpf":
                    value = value.replace(".", "").replace(
                        "-", "").replace("'", "")
                    where_clause = " AND cpf LIKE '{v}%' ".format(v=value)
                return self.get_costumer(where_clause)
            else:
                data = {"error": "field parameter with invalid value."}
                response = make_response(jsonify(data), 400,)
                response.headers["Content-Type"] = "application/json"

                return response
        else:
            # list all
            return self.get_costumer()

    def get_costumer(self, where_clause=""):
        # list all
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        try:
            cursor.execute("SELECT tbc.id, tbc.uuid, tbc.full_name, tbc.cpf, tbg.genre_name genre, TO_CHAR(tbc.birth_date, 'YYYY-MM-DD') birth_date, tbc.phone_number, tbc.email, tbc.address, tbc.postal_code, tbc.complement, tbci.city_name, tbs.state_name, order_discount(tbc.id) discount "
                           " FROM tb_costumers tbc, tb_genres tbg, tb_cities tbci, tb_states tbs "
                           " WHERE tbc.id_genre=tbg.id AND tbc.id_city=tbci.id AND tbci.id_state=tbs.id {where_clause} ORDER BY id; ".format(where_clause=where_clause))
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": str(err)
            }, 500)

        costumers = cursor.fetchall()
        data = []

        for costumer in costumers:
            data.append({
                "id": costumer.id,
                "uuid": costumer.uuid,
                "full_name": costumer.full_name,
                "cpf": costumer.cpf,
                "genre": costumer.genre,
                "birth_date": costumer.birth_date,
                "phone": costumer.phone_number,
                "email": costumer.email,
                "address": costumer.address,
                "postal_code": costumer.postal_code,
                "complement": costumer.complement,
                "city": costumer.city_name,
                "state": costumer.state_name,
                "discount": costumer.discount
            })

        cursor.close()
        connection.con.close()

        response = make_response(jsonify(data), 200,)
        response.headers["Content-Type"] = "application/json"

        return response

    def post(self):
        # add new
        new_costumer_data = request.json
        error, error_msg = costumer_data_validation(new_costumer_data)
        if not error:
            new_costumer_data = costumer_data_sanitization(new_costumer_data)
            print(new_costumer_data["postal_code"],
                  )
            new_costumer_data = {
                "id": None,
                "id_city": new_costumer_data["id_city"],
                "id_genre": new_costumer_data["id_genre"],
                "uuid": uuid.uuid4(),
                "cpf": new_costumer_data["cpf"],
                "full_name": new_costumer_data["full_name"],
                "birth_date": new_costumer_data["birth_date"],
                "phone_number": new_costumer_data["phone_number"],
                "email": new_costumer_data["email"],
                "address": new_costumer_data["address"],
                "postal_code": new_costumer_data["postal_code"] if "postal_code" in new_costumer_data else None,
                "complement": new_costumer_data["complement"] if "complement" in new_costumer_data else None, }
            connection = Connection()
            cursor = connection.con.cursor()
            sql_string = """
            INSERT INTO tb_costumers(id_city,
                                    id_genre,
                                    uuid,
                                    cpf,
                                    full_name,
                                    birth_date,
                                    phone_number,
                                    email,
                                    address,
                                    postal_code,
                                    complement)
            VALUES ( % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s) RETURNING id;
                        """
            try:
                cursor.execute(
                    sql_string,
                    (new_costumer_data["id_city"],
                     new_costumer_data["id_genre"],
                     new_costumer_data["uuid"],
                     new_costumer_data["cpf"],
                     new_costumer_data["full_name"],
                     new_costumer_data["birth_date"],
                     new_costumer_data["phone_number"],
                     new_costumer_data["email"],
                     new_costumer_data["address"],
                     new_costumer_data["postal_code"],
                     new_costumer_data["complement"],
                     ))
            except Exception as err:
                connection.con.rollback()
                connection.print_psycopg2_exception(err)

                return ({
                    "code": 400,
                    "description": str(err)
                }, 400)

            connection.con.commit()
            new_costumer_data["id"] = cursor.fetchone()[0]
            cursor.close()
            connection.con.close()
            return new_costumer_data, 201
        return error_msg, 400

    def get(self, id):
        # get specific
        id = int(id)
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        sql_string = "SELECT * FROM tb_costumers WHERE id=%s;"
        try:
            cursor.execute(sql_string, (id,))
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": "Internal Server Error"
            }, 500)

        costumer = cursor.fetchone()

        cursor.close()
        connection.con.close()

        return jsonify(costumer) if costumer is not None else {}


def costumer_data_sanitization(data):

    # id_city
    if type(data["id_city"]) == str:
        data["id_city"] = int(data["id_city"].strip())

    # id_genre
    if type(data["id_genre"]) == str:
        data["id_genre"] = int(data["id_genre"].strip())

    # cpf
    data["cpf"] = data["cpf"].replace(".", "").replace("-", "")

    # postal_code
    if "postal_code" in data:
        data["postal_code"] = data["postal_code"].replace(
            ".", "").replace("-", "")

    # full_name
    data["full_name"] = data["full_name"].strip()

    return data


def costumer_data_validation(data):
    error = False
    error_msg = []

    # id_city
    n_error, n_error_msg = Utils.validation_field_int_greater_zero(
        "id_city", data)
    error |= n_error
    error_msg += n_error_msg["error"]

    # id_genre
    n_error, n_error_msg = Utils.validation_field_int_greater_zero(
        "id_genre", data)
    error |= n_error
    error_msg += n_error_msg["error"]

    # cpf
    n_error, n_error_msg = Utils.validation_field_string("cpf", data)
    error |= n_error
    error_msg += n_error_msg["error"]
    if not Utils.validation_cpf(data["cpf"].replace(".", "").replace("-", "")):
        error = True
        error_msg.append("cpf informed is invalid.")

    # full_name
    n_error, n_error_msg = Utils.validation_field_string("full_name", data)
    error |= n_error
    error_msg += n_error_msg["error"]

    # birth_date
    n_error, n_error_msg = Utils.validation_field_string("birth_date", data)
    error |= n_error
    error_msg += n_error_msg["error"]
    if not Utils.validation_date(data["birth_date"]):
        error = True
        error_msg.append("birth_date is invalid. Use yyyy-mm-dd format.")

    # phone_number
    n_error, n_error_msg = Utils.validation_field_string("phone_number", data)
    error |= n_error
    error_msg += n_error_msg["error"]

    # email
    if not Utils.validation_email(data["email"]):
        error = True
        error_msg.append("email informed is invalid.")

    # address
    n_error, n_error_msg = Utils.validation_field_string("address", data)
    error |= n_error
    error_msg += n_error_msg["error"]

    return error, {"error": error_msg}
