# General purpose mysql functions

from SECRET_DATA import user as USER, password as PASSWORD
import mysql.connector

def executeQueryAndCommit(query, host = 'localhost', username = USER, password = PASSWORD, port = 3306, database = 'doctor_management_system'):
    '''This function will open a connection to the database and commit the sql query it is passed. It will return the amount of rows that are affected/created'''
    with mysql.connector.connect(host = host, user = username, password = password, port = port, database = database) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            return cursor.rowcount

def executeQueryAndReturnResult(query, host = 'localhost', username = USER, password = PASSWORD, port = 3306, database = 'doctor_management_system'):
    '''This function will open a connection to the database and return the results in a tuple, (column_names, [list of tuples, each tuple is a row])'''
    with mysql.connector.connect(host=host, user=username, password=password, port=port, database=database) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.column_names, cursor.fetchall()