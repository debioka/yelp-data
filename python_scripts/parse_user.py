# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 16:41:45 2017

@author: david
"""
import sqlite3
import json



DB_NAME = 'yelp'

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE users ("
    "user_id char(22) NOT NULL PRIMARY KEY, "
    "name varchar(32) NOT NULL, "
    "review_count int(10) NOT NULL, "
    "yelping_since date NOT NULL, "
    "useful int(10) NOT NULL, "
    "funny int(10) NOT NULL, "
    "cool int(10) NOT NULL, "
    "fans int(10) NOT NULL, "
    "average_stars FLOAT(3,2), "
    "compliment_hot int(5) NOT NULL, "
    "compliment_more int(5) NOT NULL, "
    "compliment_profile int(5) NOT NULL, "
    "compliment_cute int(5) NOT NULL, "
    "compliment_list int(5) NOT NULL, "
    "compliment_note int(5) NOT NULL, "
    "compliment_plain int(5) NOT NULL, "
    "compliment_cool int(5) NOT NULL, "
    "compliment_funny int(5) NOT NULL, "
    "compliment_writer int(5) NOT NULL, "
    "compliment_photos int(5) NOT NULL, "
    "type varchar(20))")

TABLES['friends'] = """CREATE TABLE friends (
                           user_id varchar(32) NOT NULL,
                           friend_id varchar(32) NOT NULL,
                           PRIMARY KEY(user_id, friend_id))
                    """
TABLES['elite'] = """ CREATE TABLE elite (
                          user_id varchar(32) NOT NULL,
                          elite_year int(4) NOT NULL,
                          PRIMARY KEY(user_id, elite_year))
                  """

# creating tables

cnx = mysql.connector.connect(user='david', password='Pw',
                              host='localhost')
cursor = cnx.cursor()


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cnx.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for key, script in TABLES.items():
    try:
        print("Creating table {}: ".format(key), end='')
        cursor.execute(script)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

        #
        # loading json information for user table

        # Problem is that non int values must be str (enclosed in  ' ')
        # Also, best to reformat global variables as dict of collumn name and
        # data type

filename = ('/Users/david/Documents/Big Data/Yelp'
            '/yelp_academic_dataset_user.json')
script_temp = 'INSERT INTO {} ({}) VALUES ({});'
table = 'users'
exceptions = ['friends', 'elite']
string_vals = ['user_id', 'name', 'type', 'yelping_since']

cnx = mysql.connector.connect(user='david', password='Pw',
                              host='localhost')
cursor = cnx.cursor()
cursor.execute('USE yelp')
with open(filename, 'r', encoding="utf8") as f:
    for line in f:
        user = json.loads(line)
        keys = []
        values = []
        for key in user:
            if key not in exceptions:
                keys.append(str(key))
                if key in string_vals:
                    values.append('"{}"'.format(str(user[key])))
                else:
                    values.append(str(user[key]))
        cursor.execute(script_temp.format(table, ', '.join(keys),
                                          ' , '.join(values)))

cursor.close()
cnx.close()
