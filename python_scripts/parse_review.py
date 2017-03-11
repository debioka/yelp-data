# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 23:49:02 2017

@author: david
"""

from parsing_funs import set_type_dict, file_path
import mysql.connector
import json

cnx = mysql.connector.connect(user='david', password='Pw',
                              host='localhost')
cursor = cnx.cursor()
cursor.execute('USE yelp')

review_type = set_type_dict(file_path['review'])

with 