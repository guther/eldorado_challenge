import os
import sys
import psycopg2


class Connection:

    def __init__(self):
        psycopg2.extras.register_uuid()
        self.con = psycopg2.connect(
            host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])

    def print_psycopg2_exception(self, err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno

        # print the connect() error
        print("\npsycopg2 ERROR:", err, "on line number:", line_num)
        print("psycopg2 traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        if hasattr(err, "diag"):
            print("\nextensions.Diagnostics:", err.diag)

        # print the pgcode and pgerror exceptions
        if hasattr(err, "pgerror"):
            print("pgerror:", err.pgerror)
            print("pgcode:", err.pgcode, "\n")
