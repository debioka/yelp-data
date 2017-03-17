# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 19:49:57 2017

@author: david
"""
from .parsing_funs import set_type_dict, file_path
import mysql.connector
import json

friends_type = {
    'friends': {'list type': 'char(22)',
                'options': 'FOREIGN KEY fk_friend_id (friend_id) REFRENCES users(user_id)',
                'type': 'list'},
    'user_id': {'options': 'FOREIGN KEY fk_user_id (user_id) REFRENCES users(user_id)',
                'type': 'char(22)'}}

cnx = mysql.connector.connect(user='david', password='Pw',
                              host='localhost')
cursor = cnx.cursor()
cursor.execute('USE yelp')

with open(file_path['user'], 'r') as file:
    for line in file:
        data = json.loads(line)
        for friend in data['friends']:
            cursor.execute('INSERT INTO friends ({}) VALUES ({});'.format(
                'user_id, friend_id', ', '.join(['"{}"'.format(x) for x in [data['user_id'], friend]])))