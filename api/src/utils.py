import re
import os
import json
from src.db import Connection
from flask import make_response, jsonify
from flask_classful import FlaskView, route
from psycopg2.extras import NamedTupleCursor


class Utils(FlaskView):

    excluded_methods = ["validation_field_int_greater_zero",
                        "validation_field_float_greater_zero",
                        "validation_field_string",
                        "validation_cpf",
                        "validation_email",
                        "validation_date"]

    @route('states', methods=['GET'])
    def states(self):
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        try:
            cursor.execute(
                "SELECT uf, state_name FROM tb_states ORDER BY state_name;")
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": err
            }, 500)

        states = cursor.fetchall()
        data = []

        for state in states:
            data.append({
                "uf": state.uf,
                "state_name": state.state_name,
            })

        cursor.close()
        connection.con.close()

        response = make_response(jsonify(data), 200,)
        response.headers["Content-Type"] = "application/json"
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response if data is not None else []

    @route('cities/<uf>', methods=['GET'])
    def cities(self, uf):
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        try:
            cursor.execute(
                "SELECT tc.id, city_name FROM tb_cities tc, tb_states ts WHERE tc.id_state=ts.id AND LOWER(ts.uf)=%s ORDER BY city_name;",
                (uf.lower(),))
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": err
            }, 500)

        cities = cursor.fetchall()
        data = []

        for city in cities:
            data.append({
                "id": city.id,
                "city_name": city.city_name,
            })

        cursor.close()
        connection.con.close()

        response = make_response(jsonify(data), 200,)
        response.headers["Content-Type"] = "application/json"
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response if data is not None else []

    @route('genres', methods=['GET'])
    def genres(self):
        connection = Connection()
        cursor = connection.con.cursor(cursor_factory=NamedTupleCursor)
        try:
            cursor.execute(
                "SELECT id, genre_name FROM tb_genres ORDER BY genre_name;")
        except Exception as err:
            connection.print_psycopg2_exception(err)
            return ({
                "code": 500,
                "description": err
            }, 500)

        genres = cursor.fetchall()
        data = []

        for genre in genres:
            data.append({
                "id": genre.id,
                "genre_name": genre.genre_name,
            })

        cursor.close()
        connection.con.close()

        response = make_response(jsonify(data), 200,)
        response.headers["Content-Type"] = "application/json"
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    def validation_field_int_greater_zero(field_name, obj):
        error = False
        error_msg = []
        if field_name not in obj or (type(obj[field_name]) == str and not obj[field_name].strip()):
            error = True
            error_msg.append("{} field must not be empty.".format(field_name))
        else:
            if type(obj[field_name]) == str or type(obj[field_name]) == float:
                try:
                    obj[field_name] = int(obj[field_name].strip()) if type(
                        obj[field_name]) == str else int(obj[field_name])
                except ValueError as error:
                    print("validation_field_int_greater_zero:", error)

            if type(obj[field_name]) != int:
                error = True
                error_msg.append("{} must be integer.".format(field_name))
            elif obj[field_name] <= 0:
                error = True
                error_msg.append(
                    "{} must be greater than zero.".format(field_name))
        return error, {"error": error_msg}

    def validation_field_float_greater_zero(field_name, obj):
        error = False
        error_msg = []
        if field_name not in obj or (type(obj[field_name]) == str and not obj[field_name].strip()):
            error = True
            error_msg.append("{} field must not be empty.".format(field_name))
        else:
            if type(obj[field_name]) == str or type(obj[field_name]) == int:
                try:
                    obj[field_name] = float(obj[field_name].strip()) if type(
                        obj[field_name]) == str else float(obj[field_name])
                except ValueError as error:
                    print("validation_field_float_greater_zero:", error)

            if type(obj[field_name]) != float:
                error = True
                error_msg.append("{} must be float.".format(field_name))
            elif obj[field_name] <= 0:
                error = True
                error_msg.append(
                    "{} must be greater than zero.".format(field_name))
        return error, {"error": error_msg}

    def validation_field_string(field_name, obj):
        error = False
        error_msg = []
        if field_name not in obj or (type(obj[field_name]) == str and not obj[field_name].strip()):
            error = True
            error_msg.append("{} field must not be empty.".format(field_name))
        elif(type(obj[field_name]) != str):
            error = True
            error_msg.append("{} must be string.".format(field_name))
        return error, {"error": error_msg}

    def validation_cpf(cpf):
        soma = 0
        if cpf == "00000000000" or len(cpf) != 11:
            return False

        for i in range(1, 10):
            try:
                soma = soma + int(cpf[i - 1: i]) * (11 - i)
            except ValueError as error:
                return False
        resto = (soma * 10) % 11

        if resto == 10 or resto == 11:
            resto = 0

        if resto != int(cpf[9:10]):
            return False

        soma = 0
        for i in range(1, 11):
            soma = soma + int(cpf[i - 1: i]) * (12 - i)
        resto = (soma * 10) % 11

        if resto == 10 or resto == 11:
            resto = 0
        return resto == int(cpf[10:11])

    def validation_email(email):
        p = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return bool(p.match(email))

    def validation_date(date_string):
        # yyyy-mm-dd
        p = re.compile(
            '\d{4}[\-](0?[1-9]|1[012])[\-](0?[1-9]|[12][0-9]|3[01])')
        if p.match(date_string):
            pdate = date_string.split('-')
            [yy, mm, dd] = [int(pdate[0]), int(pdate[1]), int(pdate[2])]
            list_of_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if mm == 2:
                lyear = ((not (yy % 4) and yy % 100) or not (yy % 400))
                if (not lyear and (dd > 28)) or (lyear and dd > 29):
                    return False
            elif dd > list_of_days[mm - 1]:
                return False
            return True
        return False
